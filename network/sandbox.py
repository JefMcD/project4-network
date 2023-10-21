
# Standard
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
import re

# Authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Database
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *

# File Handling
from django.core.files.storage import default_storage
from django.core.exceptions import SuspiciousFileOperation
import os

# Forms
from django.views.decorators.csrf import csrf_exempt
from .forms import *

# Image Handling
from PIL import Image
from django.core.files import File
from django.core.files.images import ImageFile



def many2many(request):
    
    try:
        pepe_user = User.objects.get(user_post_set__title = 'My Post')
        pepe_user_profile = User_Post.objects.get(title = 'Pepe Post')
    except:
        print("No post")
    
    my_username = User.objects.get(username = "looda").username
    looda_posts = User_Post.objects.filter(user_id_fk__username="looda")
    
    pepe_username =  pepe_user.username

    post_exists = False
    result = ""
    context = {
        'my_username': my_username,
        'result': result,
        'pepe_username': pepe_username,

    }
    return render(request, 'network/sandbox.html',context)


def gen_qs(request):
    
    message = "hello"
    context = {
        "message": message,
    }
    
    return render(request, 'network/sandbox_query_functions.html',context)