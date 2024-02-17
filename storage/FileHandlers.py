from django.core.files.uploadhandler import MemoryFileUploadHandler, TemporaryFileUploadHandler


class CustomMemoryFileUploadHandler(MemoryFileUploadHandler):

    def new_file(self, *args, **kwargs):
        args = (args[0], args[1].replace('/', '|').replace('\\', '|')) + args[2:]
        super().new_file(*args, **kwargs)


class CustomTemporaryFileUploadHandler(TemporaryFileUploadHandler):

    def new_file(self, *args, **kwargs):
        args = (args[0], args[1].replace('/', '|').replace('\\', '|')) + args[2:]
        super().new_file(*args, **kwargs)
