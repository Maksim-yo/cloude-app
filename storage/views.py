import mimetypes
import logging
from typing import List

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from storage.FileHandlers import CustomMemoryFileUploadHandler, CustomTemporaryFileUploadHandler
from storage.forms import FileForm, FolderForm
from storage.utils import get_filename,  get_view_default_img
from storage.services.dto.ObjectDTO import ObjectDTO
from storage.services.dto.FileDTO import FileDTO
import storage.config as config

BASE_STORAGE_NAME = "Хранилище"


@login_required
def index(request):
    folder = config.folder_service.get_root_folder(request.user.id)
    return folder_view(request, folder.hash)


@login_required
def folder_view(request, folder_hash: str):

    try:
        items: List[ObjectDTO] = config.folder_service.get_items(request.user.id, folder_hash)
        folder_parents: List[ObjectDTO] = config.folder_service.folder_parents(request.user.id, folder_hash)
        search_bar_paths = [[parent.name, parent.hash] for parent in folder_parents]
        search_bar_paths.reverse()
        search_bar_paths[0][0] = BASE_STORAGE_NAME
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
    except Exception as e:
        logging.error(e)


@require_http_methods(["GET"])
@login_required
def file_download(request, file_hash: str):
    try:
        file_dto = config.file_service.download_file(request.user.id, file_hash)
        content_type = mimetypes.guess_type(file_dto.path)[0]
        content_type = 'text/plain' if not content_type else content_type
        response = HttpResponse(file_dto.data, content_type=content_type)
        response.headers['Content-Disposition'] = f'attachment; filename="{file_dto.path}"'.encode('utf-8')
        return response
    except Exception as e:
        logging.error(e)


@require_http_methods(["POST"])
@login_required
def file_upload(request, folder_parent_hash: str):
    try:
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            config.file_service.save_file(request.user.id, file.name, folder_parent_hash, file.read())
        return redirect("folders", folder_parent_hash)
    except Exception as e:
        logging.error(e)


@require_http_methods(["POST"])
@login_required
@csrf_exempt
def folder_upload(request, folder_parent_hash: str):
    try:
        request.upload_handlers = [CustomMemoryFileUploadHandler(request), CustomTemporaryFileUploadHandler(request)]
        return _folder_upload(request, folder_parent_hash)
    except Exception as e:
        logging.error(e)


@login_required
@csrf_protect
def _folder_upload(request, folder_parent_hash: str):

    def folder_repair_path(path: str):
        return path.replace('|', '/')

    files = request.FILES.getlist('folder', None)        # TODO: reimplementing uploading algorithm
    files_raw = [FileDTO(path=folder_repair_path(file.name), data=file.read()) for file in files]
    try:
        config.folder_service.save_folder(request.user.id, folder_parent_hash, files_raw)
        return redirect("folders", folder_parent_hash)
    except Exception as e:
        logging.error(e)


@require_http_methods(['POST'])
@login_required
def folder_create(request, folder_parent_hash: str):
    folder_name = request.POST.get('folder_name') + '/'
    try:
        config.folder_service.save_empty_folder(request.user.id, folder_parent_hash, folder_name)
        return redirect("folders", folder_parent_hash)
    except Exception as e:
        logging.error(e)


@login_required
def folder_download(request, folder_hash: str):
    try:
        data = config.folder_service.download_folder(request.user.id, folder_hash)
        response = HttpResponse(data)
        response['Content-Type'] = 'application/x-zip-compressed'
        response['Content-Disposition'] = 'attachment; filename=album.zip'
        return response
    except Exception as e:
        logging.error(e)


@login_required
def folder_delete(request, folder_hash: str):
    try:
        parent = config.folder_service.folder_parent(request.user.id, folder_hash)
        config.folder_service.delete_folder(request.user.id, folder_hash)
        return redirect('folders', parent.hash)
    except Exception as e:
        logging.error(e)


@login_required
def file_delete(request, file_hash: str):
    try:
        parent = config.folder_service.folder_parent(request.user.id, file_hash)
        config.file_service.delete_file(request.user.id, file_hash)
        return redirect('folders', parent.hash)
    except Exception as e:
        logging.error(e)


@login_required
def folder_rename(request, folder_hash: str):
    folder_name = request.POST.get('new_folder_name') + '/'
    parent = config.folder_service.folder_parent(request.user.id, folder_hash)
    try:
        config.folder_service.rename_folder(request.user.id, folder_hash, folder_name)
        return redirect('folders', parent.hash)
    except Exception as e:
        logging.error(e)


@require_http_methods(['POST'])
@login_required
def search(request, current_folder_hash: str):
    try:
        query = request.POST.get('search')
        items = config.search_service.search(request.user.id, current_folder_hash, query)
        items_with_img = [(item, get_view_default_img(item.name, item.is_dir)) for item in items]
        return render(request, 'storage/search.html',
                     {'items': items_with_img})
    except Exception as e:
        logging.error(e)


config.init_config()
