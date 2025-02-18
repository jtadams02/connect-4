# Create your views here.
from django.shortcuts import render, redirect
from .forms import FileUploadForm
import os
from django.conf import settings

def upload_file(request):
    if request.method == 'POST': # If the upload button has been pressed
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads', uploaded_file.name)

            with open(upload_path, 'wb+') as f: # Save the file to media directory
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            return redirect('file_list')  # Redirect to file list after upload
    else:
        form = FileUploadForm() # Do nothing

    return render(request, 'fileupload/upload.html', {'form': form})

def file_list(request):
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads') # Get upload directory
    files = [] # initilize file list

    if os.path.exists(upload_dir):
        files = os.listdir(upload_dir)

    return render(request, 'fileupload/list.html', {'files': files}) # Render page with file list
