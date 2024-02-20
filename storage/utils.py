from typing import List
from enum import Enum
from django.conf import settings
import hashlib
import random
import string
from pathlib import PurePath
import os

from storage.exceptions import IllegalArgumentException


class DataType(Enum):
    DIR = 'dir'
    DOC = 'doc'
    IMG = 'img'
    PDF = 'pdf'
    DEFAULT = 'default'


storage_types = {

    DataType.IMG: ["png", "jpg"],
    DataType.DOC: ['doc', 'docx'],
    DataType.PDF: ['pdf']

}


def get_data_type(name: str) -> DataType:
    ext = get_extension(name)
    for key, value in storage_types.items():
        for val in value:
            if ext == val:
                return key
    return DataType.DEFAULT


def get_view_default_img(name: str, is_dir: bool):
    if is_dir:
        return settings.DEFAULT_VIEW_STORAGE_ITEMS_IMG[DataType.DIR.value]
    return settings.DEFAULT_VIEW_STORAGE_ITEMS_IMG[get_data_type(name).value]


def path_hash(path: str) -> str:
    return hashlib.md5(path.encode('utf-8')).hexdigest()[:6]


def get_extension(name: str) -> str:
    indx = name.rfind('.')
    return name[indx+1:len(name)] if indx != -1 else ""


def get_filename(path: str) -> str:
    if path[-1] == '/':
        raise IllegalArgumentException("Path should point to file, not directory")
    indx = path.rfind('/')
    return path[indx + 1: len(path)] if indx != -1 else path


# return name with '/' at the end
def get_folder_name(path: str) -> str:
    if path[-1] != '/':
        raise IllegalArgumentException("Path should point to directory, not file")
    indx = path.rfind('/', 0, len(path) - 1)
    return path[indx + 1: len(path)] if indx != -1 else path


def get_object_name(object: str):
    name = object.replace('/', '')
    return name.strip()


def get_name_of_folder(path: str):
    path = path.replace('/', '')
    return path.strip()


def get_root_directory(path: str):
    indx = path.find('/')
    if indx == -1:
        raise IllegalArgumentException("Path should point to directory, not file")

    return path[0:indx + 1]


def is_folder(path: str):
    return path[-1] == '/'


def generate_random_name(n: int):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=n))


def get_relative_path(source: str, path_relative: str) -> str:
    path = PurePath(source)
    try:
        relative_path = str(path.relative_to(path_relative)).replace(os.sep, '/')
        return ("" if relative_path == '.' else relative_path) + ('/' if source[-1] == '/' else '')
    except:
        return ""


def split_path(path: str) -> List[str]:

    start = 0
    end = len(path)
    paths: List[str] = []
    if path[0] == '/':
        start += 1
    while start != end:
        indx = path.find('/', start, end)
        indx = end if indx == -1 else indx
        paths.append(path[start: indx + 1])
        start = indx + 1
        if indx == end:
            break

    return paths
