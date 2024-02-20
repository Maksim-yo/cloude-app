from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
import storage.views as views

app_name = 'storage'

urlpatterns = [
    path("", views.index, name="root"),
    path("folders/<str:folder_hash>/", views.folder_view, name="folders"),
    path("folders/<str:folder_parent_hash>", views.folder_create, name="folder_create"),
    path("folders/delete/<str:folder_hash>", views.folder_delete, name="folder_delete"),
    path("folders/download/<str:folder_hash>/", views.folder_download, name="folder_download"),
    path("folders/rename/<str:folder_hash>/", views.folder_rename, name="folder_rename"),
    path("folders/upload/<str:folder_parent_hash>/", views.folder_upload, name="folder_upload"),
    path("files/download/<str:file_hash>/", views.file_download, name="file_download"),
    path("files/rename/<str:file_hash>/", views.file_rename, name="file_rename"),
    path("files/upload/<str:folder_parent_hash>/", views.file_upload, name="file_upload"),
    path("files/delete/<str:file_hash>", views.file_delete, name="file_delete"),
    path("folders/<str:current_folder_hash>/search", views.search, name="search"),
    path("__debug__/", include("debug_toolbar.urls")),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
