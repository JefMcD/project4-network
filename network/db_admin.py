


# Standard
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from .create_profiles import install_user_profiles


# Maths
import random

# Authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Database
from django.db import IntegrityError
from datetime import date
from .models import *

# File Handling
from django.core.files.storage import default_storage
from django.core.exceptions import SuspiciousFileOperation
import re
import os

# Define Users to Create
user_set = ['pepe', 'turkle', 'sheela', 'bowfren', 'looda', 'smol', 'sparra', 'zoe']   
network_users = [
        {'username':'pepe', 'email': 'pepe@mail.com', 'password': 'passw0rd'},
        {'username':'turkle', 'email': 'turkle@mail.com', 'password': 'passw0rd'},
        {'username':'sheela', 'email': 'sheela@mail.com', 'password': 'passw0rd'},
        {'username':'bowfren', 'email': 'bowfren@mail.com', 'password': 'passw0rd'},
        {'username':'looda', 'email': 'looda@mail.com', 'password': 'passw0rd'},
        {'username':'smol', 'email': 'smol@mail.com', 'password': 'passw0rd'},
        {'username':'sparra', 'email': 'sparra@mail.com', 'password': 'passw0rd'},
        {'username':'zoe', 'email': 'zoe@mail.com', 'password': 'passw0rd'},   
    ]



def db_admin(request):
    return render(request, 'network/db_admin.html')


def reset_su(request):
    new_su_user = User.objects.create_user({'username':'chief', 'email': 'chief@mail.com', 'password': 'passw0rd', 'is_superuser':True})
    new_su_user.save()
    
    return render(request, 'network/db_admin.html', {'message':'Superuser Reset'})

def pop_users():

    # Delete All Curent Users 
    for name in user_set:
        try:
            User.objects.get(username=name).delete() 
        except:
            pass
    
    # Create The New Users
    for user in network_users:
        new_user = User.objects.create_user(user['username'], user['email'], user['password'])
        new_user.save()

    install_user_profiles(network_users)
    
    return
        
def insert_users(request):
    pop_users()
    return render(request,'network/db_admin.html', {'message':'Users Created'})
        
def delete_all(request):
    # User.objects.all().delete()
    # Delete all but the chief su
    for user in network_users:
        user_name = user['username']
        print(f"delete_all() username => {user_name}")
        try:
            User.objects.get(username = user_name).delete()
        except:
            print(f"user {user_name} Does not exist")
       
    # remove manually entered user artVoo     
    try:
        User.objects.get(username = 'artVoo').delete()
    except:
        print(f"user artVoo Does not exist")
    try:
        User.objects.get(username = 'jef').delete()
    except:
        print(f"user jef Does not exist")
    User_Post.objects.all().delete()
    User_Profile.objects.all().delete()
    Engagement_m2m.objects.all().delete()

    return render(request, 'network/db_admin.html', {'message':'All Data Deleted'})


def insert_text_posts(request):
    # Open File Containing Quotes
    quote_file = os.path.join(settings.MEDIA_ROOT,'books','allegory_of_the_cave.txt' )
    if os.path.exists(quote_file):
        print(f"File Exists: '{quote_file}'")
        fd = open(quote_file, "r")
    else:
        error = f"File '{quote_file}' doesn't exist"
        print(error)
        return render(request, 'network/db_admin.html', {'message':error})
    
    # generate random number between 1 and 22 (there are 22 quotes)
    n = random.randint(1,22)
    print(n)
    fd.close()

    # Open the file for reading
    with open(quote_file, 'r') as file:
        paragraphs = []  # To store paragraphs beginning with '*quote*'
        current_paragraph = []  # To store lines of the current paragraph
        
        # Read the file line by line
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            
            # Check if the line starts with '*quote*'
            if line.startswith('*quote*'):
                # If it's not the first paragraph, store the previous paragraph
                if current_paragraph:
                    paragraphs.append('\n'.join(current_paragraph))
                current_paragraph = []  # Start a new paragraph
            else:
                current_paragraph.append(line)  # Add the line to the current paragraph
        
        # Store the last paragraph (if any)
        if current_paragraph:
            paragraphs.append('\n'.join(current_paragraph))
        
        
        # Randomly choose a user and make a random post 200 times
        num_posts = 0
        while num_posts < 200:
            # Choos random user
            random_user = random.choice(user_set)
            current_user = User.objects.get(username = random_user)  
            
            # Choose a random paragraph    
            random_paragraph = random.choice(paragraphs)
            
            # Extract title and message
            lines = random_paragraph.split('\n', 1)
            if len(lines) >= 2:
                post_title = lines[0].replace('*quote*', '').strip()
                post_message = lines[1].strip()
            else:
                post_title = ''
                post_message = random_paragraph.replace('*quote*', '').strip()
                
            # Create New Instance of text Post
            new_post = User_Post(user_id_fk = current_user,
                                    title = post_title,
                                    message = post_message 
                                    )
            new_post.save()
            num_posts += 1
            
            # Print the results
            print("Random User")
            print(current_user.username)
            print("Random Paragraph:")
            print(random_paragraph)
            print("\nTitle:")
            print(post_title)
            print("\nMessage:")
            print(post_message)
                
    return render(request, 'network/db_admin.html', {'message':'User Text Posts Added'})



def inactive(request):
    return render(request, 'network/db_admin.html', {'message':'Button Inactive'})
