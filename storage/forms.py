from django import forms


class FileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(
        attrs={'form': "form_upload_file", 'class':"invisible-input", 'onchange':"document.form_upload_file.submit()"}))


class FolderForm(forms.Form):
    folder = forms.FileField(widget=forms.FileInput(
        attrs={'form': "form_upload_folder", 'class': "invisible-input",
               'onchange': "document.form_upload_folder.submit()", 'webkitdirectory': '', 'directory': '','multiple': ''}))
