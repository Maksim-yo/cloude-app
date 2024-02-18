from django.test import TestCase

from storage.utils import *


class UtilsTest(TestCase):

    def test_get_extension(self):
        filename1 = "hello.txt"
        filename2 = "hello.txt.zip"
        extension1 = get_extension(filename1)
        extension2 = get_extension(filename2)
        self.assertEqual(extension1, 'txt')
        self.assertEqual(extension2, 'zip')

    def test_get_filename(self):
        path = "hello/test"
        file_name = get_filename(path)
        self.assertEqual(file_name, 'test')

    def test_get_folder_name(self):
        path = "hello/test/"
        folder_name = get_folder_name(path)
        self.assertEqual(folder_name, 'test/')

    def test_split_path(self):
        path1 = "test/path/hello/to"
        path2 = "test/path/hello/to/"
        path3 = "/"
        res1 = split_path(path1)
        res2 = split_path(path2)
        res3 = split_path(path3)
        self.assertEqual(len(res1), 4)
        self.assertEqual(res1[0], 'test/')
        self.assertEqual(res1[1], 'path/')
        self.assertEqual(res1[2], 'hello/')
        self.assertEqual(res1[3], 'to')
        self.assertEqual(len(res2), 4)
        self.assertEqual(res2[-1], 'to/')
        self.assertEqual(len(res3), 0)

    def test_get_relative_path(self):
        base_path = "test/hello/hello2"
        path1 = "test/hello/hello2/testing12"
        path2 = "test"
        path3 = "/"
        relative_path1 = get_relative_path(path1, base_path)
        relative_path2 = get_relative_path(base_path, path1)
        relative_path3 = get_relative_path(base_path, path2)
        relative_path4 = get_relative_path(base_path, path3)

        self.assertEqual(relative_path1, 'testing12')
        self.assertEqual(relative_path2, '')
        self.assertRegex(relative_path3, 'hello/hello2')
        self.assertEqual(relative_path4, "")

