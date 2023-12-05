import os
import minio
import sys
import logging
from storage.minio.MinioRepository import MinioRepository
from storage.minio.MinioPathFactory import MinioObjectFactory
from storage.services.FileService import FileService
from storage.services.FolderService import FolderService
from storage.services.dao.StorageDAO import StorageDAO
from storage.services.SearchService import SearchService

file_repository = None
file_service = None
folder_service = None
search_service = None


def init_config():

    try:
        minio_endpoint = os.environ.get('MINIO_ENDPOINT', 'localhost') + ":9000"
        minio_access_key = os.environ.get('MINIO_ACCESS_KEY')
        minio_secret_key = os.environ.get('MINIO_SECRET_KEY')
        client = minio.Minio(minio_endpoint, minio_access_key, minio_secret_key, secure=False)
        logging.debug("Checking storage connectection")
        if not client.bucket_exists('nonexistingbucket'):
            logging.debug("Object storage connected")
        global file_repository
        global file_service
        global folder_service
        global search_service
        file_repository = MinioRepository(client)
        path_factory = MinioObjectFactory()
        storage = StorageDAO(path_factory)
        search_service = SearchService(storage)
        file_service = FileService(file_repository, storage, path_factory)
        folder_service = FolderService(file_repository, storage, path_factory)
    except Exception as error:
        print(error)
        print(minio_secret_key)
        logging.critical("Object storage not reachable")
        sys.exit()

