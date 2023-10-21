
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


# There are a lot of Django Queries here
# https://docs.djangoproject.com/en/dev/topics/db/queries/





def entry(request):
    # If user is authenticated load profile
    if request.user.is_authenticated:
        current_user = User.objects.get(pk = request.user.id)
        print(f"############# current user => {current_user}")
        user_profile = User_Profile.objects.get(user_id_fk = current_user)
        profile_id = user_profile.user_profile_id
        user_name = current_user.username
        return HttpResponseRedirect(reverse("network:profile", kwargs={'user_id':current_user.pk, 'requested_newsfeed': 'homeposts'}))
    else:
        # load authentication options
        return render(request, "network/authenticate_options.html")



def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            current_user = User.objects.get(pk = request.user.id)
            return HttpResponseRedirect(reverse("network:profile", kwargs={'user_id':current_user.pk, 'requested_newsfeed': 'allposts'}))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:entry"))



def sanitize_user_input(user_input):
    # Remove any characters that could be used for directory traversal or other malicious purposes
    # For example, you can remove '..' and '/' characters
    sanitized_input = re.sub(r'\.\.|/', '', user_input)
    
    # You can add additional validation or sanitization logic as needed

    return sanitized_input


def create_user_profile(request):
    print (f"#### create_user_profile ####")
    
    # Define filesystem directory tree for the users uploads
    # At this point The user has been entered in the User table and has been logged in
    current_user = User.objects.get(pk = request.user.id)
    username = current_user.username   
       
    # its also important to remember where you have defined MEDIA_ROOT and MEDIA_URL for user uploads
    # MEDIA_ROOT is where the app will upload files
    # MEDIA_URL is the root url realtive to the project root directory. This is where it will look for files when you give it a pathname such as a username
    media_root = settings.MEDIA_ROOT
    media_url  = settings.MEDIA_URL
    print(f"MEDIA_ROOT => {media_root}") # /home/artillery/webdev-apps/courses/CS50/Project-4/network/user_profiles
    print(f"MEDIA_URL => {media_url}")   # /user_profiles/     
       
    # Create an instance in the User_Profile table and assign defaults where necessary
    try:
        
        folder = os.path.join(media_url,username)
        web = 'http://www.'
        mon = username
        cap = 'Hello world, my name is '+ username + ' and I just arrived'
        
        # user1.pic.save('abc.png', File(open('/tmp/pic.png', 'r')))

        new_user_profile = User_Profile(user_id_fk = current_user,
                                        user_profile_folder = folder,
                                        website = web,
                                        moniker = mon, 
                                        caption = cap)
        new_user_profile.save()
        
        # Load the Default Avatar into the avatar ImageField
        image_path = os.path.join(media_root, 'default', 'av.jpg')
        if os.path.exists(image_path):
            with open(image_path, 'rb') as image_file:
                avatar_file = File(image_file)
                image_name = f"{current_user.pk}_{current_user.username}__av.jpg"
                new_user_profile.avatar.save(image_name, avatar_file) 
        else:
            print(f"Default Background Image Path Does Not Exist. Tried -> {image_path}")
            error = "Default Background Image Path Does Not Exist. Tried ->" + image_path
            
        # Load The Default Background Image into the background_img ImageField
        image_path = os.path.join(media_root, 'default', 'bg.jpg')
        if os.path.exists(image_path):
            print(f"Default bg_img Path exists")
            
            # Snatizing is not really necessary here, its just for information
            # Sanitize the input to remove potentially dangerous characters
            safe_input = sanitize_user_input('bg.jpg')  
            # Check if the sanitized input is still safe
            if not safe_input:
                error = "Detected path traversal attempt" + image_path
                raise SuspiciousFileOperation("Detected path traversal attempt")
                

            image_path = os.path.join(settings.MEDIA_ROOT, 'default', safe_input)
            with open(image_path, 'rb') as image_file:
                bg_image_file = File(image_file)
                image_name = f"{current_user.pk}_{current_user.username}__bg_img.jpg"
                new_user_profile.background_img.save(image_name, bg_image_file)
        else:
            print(f"Default bg_img path Does Not Exist. Tried => {image_path}")
            error = "Default Background Image Path Does Not Exist. Tried ->" + {image_path}
            
    except IntegrityError:
        # delete the user profile directory area
        # delete User
        return render(request, "network/register.html", {
            "message": "Error creating User Profile.",
            'error': error,
        })
        
    return
    

def register(request):
    print(f"#### register ####")      
        
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        
        #Django validation checks username is unique

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        
        if password != confirmation:    
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })
            
        # Check if email address is already in use
        email_address_is_taken = User.objects.filter(email = request.POST['email'])
        if email_address_is_taken:
                context_dictionary = {"message": "email already being used."}
                return render(request, "network/register.html", context_dictionary)
            
        # TODO Confirm and Validate Registration by email/phone

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

        except IntegrityError:
            # remove the user profile directory area
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
            
        login(request, user)
        create_user_profile(request)
        return HttpResponseRedirect(reverse('network:profile', kwargs={'user_id': user.pk, 'requested_newsfeed':'allposts'}))
    else:
        return render(request, "network/register.html")
    
def page_404(request, message):
    pass
    
@login_required   
def profile(request, user_id, requested_newsfeed):
    print(f"##### profile #####")
    ## current_user - The currently logged in user
    ## requested_profile - The User that the profile belongs to

    # establish who active user is
    current_user_instance = User.objects.get(pk = request.user.id)

    # establish who the profile belongs to
    try:
        requested_profile_instance = User.objects.get(pk = user_id)
        print(f"profile_user {requested_profile_instance}")
    except:
        print(f"Cant fint Profile {user_id}")
        error_message = f"Can't find page for user {user_id}"
        return render(request, "network/page_404.html", {'error_message': error_message})
      
    # get User_Profile instance from User_Profile
    user_profile_instance = User_Profile.objects.get(user_id_fk = requested_profile_instance)
    
    # get cuurent_users User_Profile
    current_users_User_Profile = User_Profile.objects.get(user_id_fk = current_user_instance.pk)
    
    # Either the Profile is being viewed by the Owner or another User
    # Display appropriate available functionality depending on who is viewing the profile

    # establish If this is the Home Profile
    print(f"curent user => {current_user_instance.pk}")
    print(f"profile_user = {requested_profile_instance.pk}")
    
    if current_user_instance.pk == requested_profile_instance.pk:
        user_is_home = True
    else:
        user_is_home = False
        
    if user_is_home:
        # Active Logged in User is viewing their own profile
        # Initialise the Edit Profile Form
        edit_profile_message = "Let folks know what you've been up to lately"
        # Initialise an Edit Form and Populate with data from the instance
        edit_profile_form = Edit_User_Profile_Form()
        following_status = False
    else:
        # Active Logged in User is viewing someone elses profile
        edit_profile_message = "ANother users profile"
        edit_profile_form = ""
        
        # establish if current_user is following the profile_user
        # followed = User.objects.get(following = requested_profile_instance)
        is_being_followed = requested_profile_instance in current_user_instance.following.all()
        if is_being_followed:

            following_status = True
        else:
            following_status = False
            
    following = requested_profile_instance.following.all().count()
    followers = requested_profile_instance.followers.all().count()
    
    # Get Newsfeed Posts
    if requested_newsfeed == 'homeposts':
        #postfeed = User_Post.objects.filter(user_id_fk = requested_profile_instance).order_by('-date')
        pass
    elif requested_newsfeed == 'allposts':
        #postfeed = User_Post.objects.all().order_by('-date')
        pass
    else:
            # 'frensposts'
            #
            # SQL would be something like this
            #
            #    SELECT *
            #    FROM USER_POST
            #    WHERE user_id_fk IN(
            #       SELECT following
            #       FROM User
            #       WHERE pk = current_user.pk
            #    )
            #
            #
            # Actual SQL Statement to get User with user_id==25's followers posts. 
            # Inner Subquery to get a users followers. Then an outer query to get all the posts from them
            #
            #   SELECT NUP.user_id_fk_id, NUP.user_post_id, NUP.title
            #   FROM network_user_post AS NUP, network_user AS NU, network_user_following AS NUF
            #   WHERE NUP.user_id_fk_id IN (
            # 	    SELECT NUF.to_user_id
            # 	    FROM network_user AS NU2, network_user_following AS NUF2 
            # 	    WHERE NU2.id = NUF2.from_user_id AND NU2.id = 25
            #   );
            #
            # Django Can execute the raw query thusly; Just drop the query in one big ling string and use thw raw() method
            # postfeed_raw = User_Post.objects.raw("SELECT NUP.user_id_fk_id, NUP.user_post_id, NUP.title FROM network_user_post AS NUP, network_user AS NU, network_user_following AS NUF WHERE NUP.user_id_fk_id IN ( SELECT NUF.to_user_id FROM network_user AS NU, network_user_following AS NUF  WHERE NU.id = NUF.from_user_id AND NU.id = 25);")

        user_followers = current_user_instance.following.all()
        #postfeed = User_Post.objects.filter(user_id_fk__in = user_followers)
        
    # paginator = Paginator(postfeed, 10)
    # page_obj = paginator.get_page(1)
    

    # Send Blank New Post Form
    new_post_form = New_Post_Form()
    media_inputs = New_Post_Media_Form()
    
    
    
    


    return render(request, "network/profile.html",{
                    'message': "v",
                    'edit_profile_message': edit_profile_message,
                    
                    'profile': user_profile_instance,
                    'profile_user_id': user_id,
                    'profile_username': requested_profile_instance.username,
                    
                    'current_user': current_users_User_Profile,
                    'current_username': current_user_instance.username,
                    'current_user_id': current_user_instance.pk,
                    
                    'following_status': following_status,
                    'followers': followers,
                    'following': following,
                    'home_status': user_is_home,
                    
                    'edit_user_profile_form': edit_profile_form,
                    'new_post_form': new_post_form,
                    'media_inputs':media_inputs,
                    
                    # 'postfeed': page_obj,
                    'postfeed_name': requested_newsfeed,
                    'page_num': 0,
                    
                    # Test

    })
    
    
    
    
    

    
@login_required   
def edit_profile(request):
    print(f"#### edit_profile ####")

    # Initialise Variables
    message = "Let folks know what you've been up to lately"
    current_user = User.objects.get(pk = request.user.id)
    user_profile_instance = User_Profile.objects.get(user_id_fk = current_user)
    # Initialise an Edit Form and Populate with data from the instance
    form = Edit_User_Profile_Form(initial={
        'background_img' : user_profile_instance.background_img.url,
        'avatar': user_profile_instance.avatar.url,
        'moniker': user_profile_instance.moniker,
        'website': user_profile_instance.website,
        'caption': user_profile_instance.caption
    })
    
    if request.method == 'POST':
        form = Edit_User_Profile_Form(request.POST, request.FILES)
        if form.is_valid():
            
            if 'background_img' in request.FILES:
                # rename the file to namespace it to the current user
                bg = request.FILES['background_img']
                bg.name = f"{current_user.pk}_{current_user.username}__{request.FILES['background_img'].name}"
                user_profile_instance.background_img = request.FILES['background_img']
                
            if 'avatar' in request.FILES:
                # rename the file to namespace it to the current user
                av = request.FILES['avatar']
                av.name = f"{current_user.pk}_{current_user.username}__{request.FILES['avatar'].name}"
                user_profile_instance.avatar = request.FILES['avatar']
                
            user_profile_instance.moniker = form.cleaned_data['moniker']
            user_profile_instance.website = form.cleaned_data['website']
            user_profile_instance.caption = form.cleaned_data['caption']
            user_profile_instance.save()
            
            return HttpResponseRedirect(reverse("network:profile", kwargs={'user_id':current_user.pk, 'requested_newsfeed':'homeposts'}))
        else:
            message = 'Please Correct Errors'
    else:
        # Provide Form with current User Profile to the User
        # find the user profile and populate the form with current data
        # Get the User_Profile instance from the database
        

        # Populate the form with data from the instance
        form = Edit_User_Profile_Form(initial={
            'background_img' : user_profile_instance.background_img.url,
            'avatar': user_profile_instance.avatar.url,
            'moniker': user_profile_instance.moniker,
            'website': user_profile_instance.website,
            'caption': user_profile_instance.caption
        })
    
    return render(request, "network/edit_profile.html",{
                'profile': user_profile_instance,
                'edit_user_profile_form': form,
                'message': message,
    })
    

