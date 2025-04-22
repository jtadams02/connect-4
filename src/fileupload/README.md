FILE UPLOAD

Django app for uploading files to the web application.

Only a few files were edited from the auto-generated files from Django, if a file isn't listed, it doesn't effect execution directly

# forms.py

Minimal form class for use in views.py . Can be updated but will work as is.


# views.py

This is the main portion of this app that contains most of the logic surronding the file uploads

Contains only one function, current version only uploads to media folder

Commented out portion inside function is used for uploading to google cloud. This is functional but will require setting parameters for your own google cloud accounts / deployment.


# urls.py

Sets the url structure for the app.

# media/uploads

Directory in which uploaded media (python connect4 agents) are uploaded and stored in