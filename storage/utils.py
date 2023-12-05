from typing import List
from enum import Enum
from django.conf import settings
import hashlib
import random
import string

class DataType(Enum):
    DIR = 'dir'
    DOC = 'doc'
    IMG = 'img'
    PDF = 'pdf'
    DEFAULT = 'default'




storage_types = {

    DataType.IMG: ["png", "jpg"],
    DataType.DOC: ['doc', 'docx'],

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


def create_path(user_id: str, object_path: str) -> str:
    return user_id + '/' + object_path


# shouldn't start with '/'
def split_path(path: str) -> List[str]:

    start = 0
    end = len(path)
    paths: List[str] = []
    full_path: str = ""
    flag = False
    if path[0] == '/':
        path = path[1:]
    while start != end:
        indx = path.find('/', start, end)
        indx = end if indx == -1 else indx
        full_path += path[start: indx + 1]
        paths.append(full_path)
        start = indx + 1
        if indx == end:
            break

    return paths


def get_extension(name: str) -> str:
    _name = name[::-1]
    indx = _name.find('.')
    return _name[0:indx + 1] if indx != -1 else ""

def get_parent_path(path: str):
    indx = path.rfind('/')
    if indx == len(path) -1:
        indx -= 1
        while path[indx] != '/' and indx > 0:
            indx -= 1

    return path[0:indx + 1] if indx > 0 else ""


def get_filename(path: str) -> str:
    if path[-1] == '/':
        raise Exception
    indx = path.rfind('/')
    return path[indx + 1: len(path)] if indx != -1 else path


def get_folder_name(path: str) -> str:
    if path[-1] != '/':
        raise Exception
    indx = path.rfind('/', 0, len(path) - 1)
    return path[indx + 1: len(path)] if indx != -1 else path

def get_root_directory(path: str):
    indx = path.find('/')
    if indx == -1:
        raise Exception
    return path[0:indx + 1]

def get_name_of_folder(path: str):
    path = path.replace('/', ' ')
    return path.strip()


def compose_path_w_slashes(path1: str, path2: str):
    if path1[-1] == '/' and path2[-1] == '/':
        return path1[0:-1] + path2
    else:
        return path1 + path2


def is_folder(path: str):
    return path[-1] == '/'


def generate_random_name(n: int):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=n))


def get_relative_path(path1: str, path2: str) -> str:
    if path2 not in path1:
        raise Exception
    indx = path1.find(path2)
    return path1[indx + len(path2):]


def split_path_each(path: str):
    start = 0
    end = len(path)
    paths: List[str] = []
    if path[0] == '/':
        path = path[1:]
    while start != end:
        indx = path.find('/', start, end)
        indx = end if indx == -1 else indx
        paths.append(path[start: indx + 1])
        start = indx + 1
        if indx == end:
            break

    return paths