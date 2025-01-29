# How to access virtual environment

First setup the virtual environment by going into the root directory, and running the following 
```console
> py -3.13 -m venv .env
```
*(You may need to install the lastest version of python, ensure to install it to path)*

 Once the env is generated, you need to activate it, to do so on Windows use the following command:
 ```console
> .env\Scripts\activate.bat
```

Now the virtualenv is activated, install the requirements using this:
```console
> pip install -r requirements.txt
```

All dependencies should be installed, to test the server switch to the ```src/``` directory and run the following:
```console
> python manage.py runserver
```

