from django import forms

# TODO: THIS IS A SIMPLE FORM SO ITS NOT LINKED TO A DATABASE YET

class FileUploadForm(forms.Form):
    file = forms.FileField()
