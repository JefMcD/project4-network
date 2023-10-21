
# Setup & Install on Ubuntu 22.04.2

## Setup Python Virtual Environment

Install virtual environment in folder .venv in the project folder  

```
$ cd /Project-4
$ python3 -m venv .venv
```
add .venv and .venv/\*.* to .gitignore

## Start virtual environment

```
$ source .venv/bin/activate
```


## install necessary packages

```
(.venv)$ pip3 install django
(.venv)$ pip3 install python-decouple
(.venv)$ pip3 install whitenoise
```
or they can be installed via the requirements.txt file
```
(.venv) $ pip3 install -r requirements.txt
```

## Creating Django Project and App

```
(.venv)$ cd ../Project-4/
(.venv)$ django-admin startproject Project4
(.venv)$ cd Project4
(.venv)$ python4 manage.py startapp network 
```

## Configure App Name
Open urls.py and add the line
```
app_name = 'network' 
```
This is then used in all urls to namespace them


## Configure DEFAULT_AUTO_FIELD

Open Apps.py  
Edit the AppConfig thusly
```
from django.apps import AppConfig

class MailConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'network'
```
or open settings.py and define it thusly
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```


## Configure Whitenoise
Required only on production
See Production Setup

## Configure python-decouple
Create .env file in root directory ( the one with manage.py)
add definitions for sensitive data such as passwords and keys thusly;
```
SECRET_KEY = 'whateverthesecretkeyhappenstobe'
```
Then open settings.py and add the lines
```
from decouple import config
SECRET_KEY = config('SECRET_KEY')
```
repeat for all sensitive data and then open .gitignore (also in root directory)
add the line
```
.env
```
So it wont be included in the codebase and publicly visible


# Install Django Debug Toolbar

```
(.venv)$ pip3 install django-debug-toolbar
```

Open settings.py  

add 'debug_toolbar' to the INSTALLED_APPS list:
```
INSTALLED_APPS = [
   # ...
   'debug_toolbar',
   # ...
]
```

Configure Middleware: Still in your settings.py, add the DebugToolbarMiddleware to the MIDDLEWARE list. Place it as early as possible so that it can capture and display relevant debug information:

```
MIDDLEWARE = [
   'debug_toolbar.middleware.DebugToolbarMiddleware',
   # ...
]
```

Configure Internal IPs: You'll need to specify internal IP addresses that can access the debug toolbar. Add the following to your settings.py:
```
INTERNAL_IPS = [
   # '127.0.0.1',  # example IP, add your own IPs here
   # ...
]
```

URL Configuration: To enable the debug toolbar, you need to add its URL configuration to your project's urls.py. 
Open the urls.py file that is in the project folder ( the one containing the settings.py file)
Import the toolbar's functions at the top of the file and then include the toolbar URLs:

```
from django.urls import include
from . import settings

# ...

if settings.DEBUG:
   import debug_toolbar
   urlpatterns = [
       path('__debug__/', include(debug_toolbar.urls)),
       # ...
   ] + urlpatterns
```


## Make Migrations

Always include the app name when making migrations

```
(.venv)$ python3 manage.py makemigrations network
(.venv)$ python3 manage.py migrate
(.venv)$ python3 manage.py runserver
```








   
