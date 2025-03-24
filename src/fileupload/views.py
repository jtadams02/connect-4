# Create your views here.
from django.shortcuts import render, redirect
from .forms import FileUploadForm
import os
from django.conf import settings

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import UploadedFile

import logging

from google.cloud import storage

logger = logging.getLogger(__name__)


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']

            if not uploaded_file.name.endswith('.py'):
                error_message = "Only Python files (.py) are allowed."
                return render(request, 'fileupload/upload.html', {'form': form, 'error': error_message})
            
            try:
                # Define the upload path
                upload_path = f"uploads/{uploaded_file.name}"

                # Initialize the Google Cloud Storage client
                client = storage.Client()
                bucket = client.bucket(settings.GS_BUCKET_NAME)  # Using the bucket from settings

                # Create a blob (object) in the bucket with the defined path
                blob = bucket.blob(upload_path)

                # Upload the file content to the blob
                blob.upload_from_file(uploaded_file, content_type=uploaded_file.content_type)

                # Construct file URL
                file_url = f"https://storage.googleapis.com/{settings.GS_BUCKET_NAME}/{upload_path}"

                # Save file metadata to PostgreSQL database
                UploadedFile.objects.create(
                    file_name=uploaded_file.name,
                    file_url=file_url
                )

                logger.info(f"File {uploaded_file.name} uploaded successfully to {upload_path}")

                return redirect('/')
            except Exception as e:
                logger.error(f"Upload error: {e}")
                return render(request, 'fileupload/upload.html', {'form': form, 'error': str(e)})

    else:
        form = FileUploadForm()

    return render(request, 'fileupload/upload.html', {'form': form})


#def file_list(request):
#    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads') # Get upload directory
#    files = [] # initilize file list
#
#    if os.path.exists(upload_dir):
#        files = os.listdir(upload_dir)
#
#    return render(request, 'fileupload/list.html', {'files': files}) # Render page with file list
