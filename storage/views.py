import mimetypes
from typing import List

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseNotFound
from storage.forms import FileForm, FolderForm
from storage.utils import get_filename,  get_view_default_img
from storage.services.dto.ObjectDTO import ObjectDTO
from storage.services.dto.FileDTO import FileDTO
import storage.config as config


@login_required
def index(request):
    folder = config.folder_service.get_root_folder(request.user.id)
    return folder_view(request, folder.hash)


@login_required
def folder_view(request, folder_hash: str):

    items: List[ObjectDTO] = config.folder_service.get_items(request.user.id, folder_hash)
    item: ObjectDTO = config.folder_service.get_folder(request.user.id, folder_hash)
    folder_parents: List[ObjectDTO] = config.folder_service.folder_parents(request.user.id, folder_hash)
    search_bar_paths = [(parent.name, parent.hash) for parent in folder_parents]
    search_bar_paths.reverse()
    temp = list(search_bar_paths[0])
    temp[0] = "Хранилище"
    search_bar_paths[0] = tuple(temp)
    items_with_img = [(item, get_view_default_img(item.name, item.is_dir)) for item in items]
    file_form = FileForm()
    folder_form = FolderForm()
    return render(request, "storage/folder.html",
                  {
                   "current_folder_hash": folder_hash,
                   "items": items_with_img,
                   "form_folder": folder_form,
                   "form_file": file_form,
                   'paths': search_bar_paths,
                   })


@require_http_methods(["GET"])
@login_required
def file_download(request, file_hash: str):
    file_dto = config.file_service.download_file(request.user.id, file_hash)
    content_type = mimetypes.guess_type(file_dto.path)[0]
    content_type = 'text/plain' if not content_type else content_type
    response = HttpResponse(file_dto.data, content_type=content_type)
    response.headers['Content-Disposition'] = f'attachment; filename="{file_dto.path}"'.encode('utf-8')
    return response


@require_http_methods(["POST"])
@login_required
def file_upload(request, folder_parent_hash: str):
    form = FileForm(request.POST, request.FILES)
    if form.is_valid():

        file = request.FILES['file']
        config.file_service.save_file(request.user.id, file.name, folder_parent_hash, file.read())
    return redirect("folders", folder_parent_hash)


@require_http_methods(['POST'])
@login_required
def folder_upload(request, folder_parent_hash: str):
    form = FolderForm(request.POST, request.FILES)

    files = request.FILES.getlist('folder', None)        # TODO: reimplementing uploading algorithm
    files_raw = [FileDTO(path=file.name, data=file.read()) for file in files]
    try:
        config.folder_service.save_folder(request.user.id, folder_parent_hash, files_raw)
        return redirect("folders", folder_parent_hash)
    except Exception as e:
        print(e)


@require_http_methods(['POST'])
@login_required
def folder_create(request, folder_parent_hash: str):
    folder_name = request.POST.get('folder_name') + '/'
    try:
        config.folder_service.save_empty_folder(request.user.id, folder_parent_hash, folder_name)
        return redirect("folders", folder_parent_hash)
    except Exception as e:
        print(e)


@login_required
def folder_download(request, folder_hash: str):
    try:
        data = config.folder_service.download_folder(request.user.id, folder_hash)
        response = HttpResponse(data)
        response['Content-Type'] = 'application/x-zip-compressed'
        response['Content-Disposition'] = 'attachment; filename=album.zip'
        return response
    except Exception as e:
         pass


@login_required
def folder_delete(request, folder_hash: str):
    try:
        parent = config.folder_service.folder_parent(request.user.id, folder_hash)
        config.folder_service.delete_folder(request.user.id, folder_hash)
        return redirect('folders', parent.hash)
    except:
        pass


@login_required
def file_delete(request, file_hash: str):
    try:
        parent = config.folder_service.folder_parent(request.user.id, file_hash)
        config.file_service.delete_file(request.user.id, file_hash)
        return redirect('folders', parent.hash)
    except:
        pass

@login_required
def folder_rename(request, folder_hash: str):
    folder_name = request.POST.get('new_folder_name') + '/'
    parent = config.folder_service.folder_parent(request.user.id, folder_hash)
    try:
        config.folder_service.rename_folder(request.user.id, folder_hash, folder_name)
        return redirect('folders', parent.hash)
    except:
        pass


@require_http_methods(['POST'])
@login_required
def search(request, current_folder_hash: str):
    try:
        current_folder: ObjectDTO = config.folder_service.get_folder(request.user.id, folder_hash)
        query = request.POST.get('search')
        items = config.search_service.search(request.user.id, query)
        items_with_img = [(item, get_view_default_img(item.name, item.is_dir)) for item in items]
        return render(request, 'storage/search.html',
                     {'items': items_with_img})
    except Exception as e:
        pass


# TODO: move
def folder_create_root(user_id: int, folder_name: str):
    config.folder_service.save_root_folder(user_id, folder_name)
