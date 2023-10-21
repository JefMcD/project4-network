

# Standard
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse
import re

# Authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Database
from datetime import datetime
from django.db import IntegrityError
from django.core.paginator import Paginator
from .models import *

# Javascript API
import json
from django.http import JsonResponse

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


@login_required
def follow_user(request, user_id):
    print("#### follow ####")
    print(f"user_is => {user_id}")
    current_user = User.objects.get(pk = request.user.id)
    user_to_follow = User.objects.get(pk = user_id)
    try:
        current_user.following.add(user_to_follow)
        current_user.save()
        return JsonResponse({"message": "User followed."}, status=201)
    
    except:
        return JsonResponse({"message": "Error following user."}, status=500)

@login_required
def unfollow_user(request, user_id):
    current_user = User.objects.get(pk = request.user.id)
    user_to_unfollow = User.objects.get(pk = user_id)
    try:
        current_user.following.remove(user_to_unfollow)
        current_user.save()
        return JsonResponse({"message": "User unfollowed."}, status=201)
    except:
        return JsonResponse({"message": "Error unfollowing user."}, status=500)
    

@csrf_exempt
@login_required
def get_user_profile(request, user_id=0):
    # Return profile contents
    if request.method == "GET":
        # check profile exists
        current_user = User.objects.get(pk = request.user.id)
        profile_exists = User_Profile.objects.filter(user_id_fk = current_user).exists()
        
        # Query for requested user profile
        if profile_exists:
            profile = User_Profile.objects.get(user_id_fk = current_user)
        else:
            return JsonResponse({"error": "Profile not found."}, status=404)
         
        return JsonResponse(profile.serialize(), status = 201)
    else:
        # profile request must be via GET
        return JsonResponse({"error": "GET request required."}, status=400)


@csrf_exempt
@login_required
def get_post_data(request, post_id):
    print(f"API: get_post_data()")
        # Query for requested post
    try:
        print(f"API: getting post")
        post_exists = User_Post.objects.filter(user_post_id = post_id).exists()
        if post_exists:
            print(f"API: post exists")
            post = User_Post.objects.get(user_post_id = post_id)
            print(f"API: post instance obtained")
        else:
            print(f"API: ERROR cant find post {post_id}")
            return JsonResponse({"error": "API: Cant find Post"}, status = 404)
    except User_Profile.DoesNotExist:
        print(f"API: Cant find post {post}")
        return JsonResponse({"error": "Profile not found."}, status=404)
    
    print(f"API: post => {post}")
    print(f"API: serializing and returning")
    serial = post.serialize()
    print(f"API: serialized... done. returning data {serial}")
    # Return profile contents
    if request.method == "GET":
        return JsonResponse(post.serialize(), status = 201)
    else:
        # profile request must be via GET
        return JsonResponse({"error": "GET request required."}, status=400)
    


@login_required
@csrf_exempt
def update_profile(request):
    print(f"#### update_profile ####")
    # Updating the profile is done via POST to produce data that is in the same format
    # as the standard Form objects request.POST and request.FILES
    
    if request.method == "POST":
         # Retrieving data from the FormData() sent in request
        # and is contained in a dictionary of key:value pairs 
        # 'get' is a dictionary method that will return the value for a specified key
        # https://www.w3schools.com/python/ref_dictionary_get.asp
          
        # Query the User_Profile instance for the logged in User
        current_user = User.objects.get(pk = request.user.id)
        
        # check profile exists
        profile_exists = User_Profile.objects.filter(user_id_fk = current_user)
        
        # Get instance of User_Profile
        if profile_exists:
            user_profile_instance = User_Profile.objects.get(user_id_fk = current_user)  
        else:
            return JsonResponse({"error": "User Profile doesnt exist"}, status=404) 
        
         
        # Update User Profile fields with new values
        try:
            # regular text fields are stored in request.POST
            moniker_data = request.POST.get('moniker')
            website_data = request.POST.get('website')
            caption_data = request.POST.get('caption')
            
            # media Files are handled differently. The are stored in request.FILES
            avatar_file = request.FILES.get('avatar_file')
            if avatar_file:
                # Update the avatar field in the model with the uploaded file
                user_profile_instance.avatar = avatar_file

            background_file = request.FILES.get('background_file')
            print(f"API: bg_file => {background_file}")
            print(f"API: type => {type(background_file)}")
            if background_file:
                # Update the avatar field in the model with the uploaded file
                user_profile_instance.background_img = background_file
            
            if moniker_data:
                user_profile_instance.moniker = moniker_data
            if website_data:
                user_profile_instance.website = website_data
            if caption_data:
                user_profile_instance.caption = caption_data
      
            user_profile_instance.save()     
             
            print(f"#### update success ####")
            return JsonResponse({"message": "User Profile successfully updated."}, status=201)
        except:
            print(f"#### update FAIL ####")
            return JsonResponse({"error": "Internal Server Error. Update Failed"}, status=500)   
    else:
        # ie request.method === 'GET' | 'PUT' | 'DELETE'
        return JsonResponse({"error": "Malformed Request. POST request required."}, status=400)



def remove_post(request):
    pass










@csrf_exempt
@login_required
def handle_post(request, post_option = 'create', post_id = 0 ):
    print(f"#### PI: handle_post ####")
    
    if request.method == 'POST':
        # establish current_user
        current_user = User.objects.get(pk = request.user.id)
        # retrieve JSON Object   

        print(f"API: Getting Form Data from Request")
        # Get contents of request FormData() JSON
        request_title = request.POST.get('title')
        request_message = request.POST.get('message')
        print(f"API: message => {request_message}")
        request_image_file = request.FILES.get('image_file')         
            
        
        if post_option == 'create':
            # process new post
            print(f"API: creating post")
            try:
                print(f"API: Creating New Instance")             
                # create a new instance of User_Post
                newpost_instance = User_Post(
                                        user_id_fk = current_user,
                                        title = '',
                                        message = '',
                                        image_file = '',
                                        # engagement m2m = added when user updukes a post
                                        # date = default
                )
            except Exception as error:
                error = f"API: ERROR creating User_Post instance. {error}"
                return JsonResponse({"error": error}, status = 500)
        elif post_option == 'edit':
            # get post instance for edit
            # request.method == 'PUT' finds the data in request.data rather than request.POST

            print(f"API: Editing Existing Post")
            try:
                print(f"API: Checking post exists")
                post_exists = User_Post.objects.filter(user_post_id = post_id).exists()
                if post_exists:
                    print(f"API: Post exists. Getting Instance")
                    newpost_instance = User_Post.objects.get(user_post_id = post_id)
                else:
                    print(f"API: Doesnt Exist")
                    error = f"API: ERROR User_Post {post_id} Doesnt exist "
                    return JsonResponse({"error": error}, status = 404)
            except Exception as error:
                error = f"API: ERROR querying User_Post instance for post_id {post_id}. {error}"
                return JsonResponse({"error": error}, status = 500)  
           
        elif post_option == 'remove':
            pass
        else:
            pass
    else:
        error = f"API: Bad request. Must be POST got {request.method}. {error}"
        return JsonResponse({"error": error}, status = 401)         

    print(f"Assigning Title")  
    # Assign Values from FormData to the User_Post model
    try:
        if request_title:
            print(f"title: {request_title}")
            newpost_instance.title = request_title
            
        print(f"Assigning message")  
        if request_message:
            print(f"message: {request_message}")
            # request_message = "hello world " 
            newpost_instance.message = request_message
        
        print(f"Assigning Image")             
        if request_image_file:
            print(f"image: {request_image_file.name}")
            newpost_instance.image_file = request_image_file

        print(f"Saving") 
        try:
            newpost_instance.save()
        except Exception as error:
            error = f"API: Error saving User_Post. {error}"
            return JsonResponse({"error": error}, status = 500) 
                  
        ############### Rendering Single User_Post to Html ####################
        #################################################
        print(f"Create Page Obj") 
        # Create paginator instance with a single item per page
        paginator = Paginator([newpost_instance], 1)
        
        # Create a Page Object for this post
        page_obj = paginator.get_page(1)
            
        print(f"Calling render") 
        # render post into html block
        post_html = render_page_obj_as_html(request, page_obj, 1, 'homeposts')
        
        print(f"Returning") 
        return JsonResponse({"html_post_set": post_html,
                            "message": "API: Post Success."
                            }
                            , status=201)
    except Exception as e:
            error = f"API: Create Post Failed {e}"
            return JsonResponse({"message": error}, status=500)
        
    return JsonResponse({"message": "Im only here for the banter"})
















@csrf_exempt
@login_required
def upduke_post(request, post_id):
    print(f"####### upduke_post ########")
    if(request.method == 'PUT'):
        print(f"API: request method = PUT")

        post_instance = User_Post.objects.get(pk = post_id)
        current_user = User.objects.get(pk = request.user.id)

        # Check if the user has already engaged with this post
        
        # ie If enagagement instance exists for this user with this post
        # update the upduke
        # else create engagement instance and return
        
        print(f"API: querying Engagement")
 
        engagement_exists = Engagement_m2m.objects.filter(user=current_user, user_post=post_instance).exists()
        print(f"API: engagement_exists = {engagement_exists}")
        if (engagement_exists):
            # Prior engagement exists
            post_engagement = Engagement_m2m.objects.get(user=current_user, user_post=post_instance)
            
            # If upduke = 1 set it to 0 and vice-versa
            # Update the Post Upduke count
            if (post_engagement.upduke == 0):
                post_engagement.upduke = 1
            else:
                post_engagement.upduke = 0
        else:
            # New Post Upduke
            post_engagement = Engagement_m2m(user = current_user, 
                                             user_post = post_instance, 
                                             upduke = 1,
                                             date = datetime.now())

        post_engagement.save()
        print(f"API: post: {post_instance.user_post_id} upduke = 1 ")
        print(f"API: post_engagement => : {post_engagement}")           
        # Get Total Number Of updukes for the Post
        total_up = Engagement_m2m.objects.filter(user_post_id = post_id, upduke = 1).count()
        print(f"total_up => {total_up}")
            
        return JsonResponse({"total_updukes": total_up}, status = 201)
    elif (request.method == 'GET'):
        print(f"API: request method = GET")
    else:
        print(f"API: request method = Bad Request")
        return JsonResponse({"message": "API: Bad Request. PUT required"}, status = 400)
    
    
    
def serialize_user_posts(user_posts):
    # Serialize the Paginated User_Post objects into a list of dictionaries
    #
    # This will return a JSON object containing a dictionary with a single key:value inside it called 'user_posts':serialized_dat
    #
    # The serialized_data is created using a list comprehension where the for loop iterates over the supplied user_posts object 
    # and assigning each one to post. The values of the attributes in the post are then assigned to key value pairs of a dictionary
    #
    # The end result is an array containing a list of dictionarys with each one containing the attributes for a post.
    #
    # This is then wrapped in another dictionary to be sent as a JSonRespoonse
    #
    # To access it the javascript will look for the key 'user_posts
    # It can then access an array of dictionary objects which hold each post as below
    #
    # List Comprehension
    # https://www.w3schools.com/python/python_lists_comprehension.asp
    serialized_data = [
        {
            "user_post_id": post.user_post_id,
            "user_id_fk": post.user_id_fk.id,
            "title": post.title,
            "message": post.message,
            "image_url": post.image_file.url if post.image_file else None,
            "date": post.date,
        }
        for post in user_posts
    ]
    
    print(f"serialized_data => {serialized_data}")
    return {"user_posts": serialized_data}



def render_page_obj_as_html(request, page_obj, page_num, postfeed):
    # Recieves the page_obj containing the page of ten posts
    # renders the page through the post_obj2.html template into plain html 
    # This will produce a set of 10 HTML Blocks that can be returned to Javascript via the JsonResponsethat that Javascript can drop into the DOM
    print(f"API: Render ... ")
    
    current_user = User.objects.get(pk = request.user.id)
    
    html_post_set = []
    for post in page_obj:
        print(f" ############# API: looping... ###############")
        # get the total updukes for the post
        
        print(f"API: gettinh poster ... ")
        poster = post.user_id_fk # instance of User
        
        print(f"API: gettinh total ... ")
        total_updukes = Engagement_m2m.objects.filter(user_post_id = post, upduke = 1).count()
        
        print(f"API: setting post upduke star status")
        user_engagement_exists = Engagement_m2m.objects.filter(user_post = post, user = current_user).exists()
        print(f"API: exists check done")
        if user_engagement_exists:
            print("exists")
        else:
            print('doesnt exist')
            
        if user_engagement_exists:
            print(f"API: exists check retuned {user_engagement_exists}")

            engagement_instance =  Engagement_m2m.objects.get(user_post = post, user = current_user)
            upd = engagement_instance.upduke
          
            print(f"API: upd => {upd}")
            if upd == 1:
                upduke_star_status = 'on'
            else:
                upduke_star_status = 'off'
        else:
            upduke_star_status = 'off'
                 
        # Determine if the Post was made by the Current User
        if poster == current_user:
            post_is_by_current_user = True
        else:
           post_is_by_current_user = False

        
        context = {
                'post': post,
                'page_num': page_num,
                'postfeed': postfeed,
                'total_updukes': total_updukes,
                'upduke_star_status': upduke_star_status,
                'post_is_by_current_user': post_is_by_current_user,
        }
        print(f"API: render ... ")
        # Rendering the content returns binary data not string
        html_binary_block = render(request, 'network/post_obj.html', context).content


        print(f"API: render done ... ")
        # decode the returned content from binary back into html string data
        html_post = html_binary_block.decode()
        

        # Add the post to the html_post_set
        html_post_set.append(html_post)
        print(f"######### Finished Render ###########")
      
    return html_post_set



def get_post_html(request):
    pass

def serialize_html_block(page_html):
    return {'user_posts': page_html}



def get_newsfeed_page(request,user_id, postfeed, requested_page):
    print(f"API: get_newsfeed_page. Entry")
    profile_user = User.objects.get(pk = user_id)
    current_user = User.objects.get(pk = request.user.id)
    if request.method == "GET":
        print(f"API: get_newsfeed_page GET")
        # Query database
        if postfeed == 'homeposts':
            post_set = User_Post.objects.filter(user_id_fk = user_id).order_by('-date')
        elif postfeed == 'allposts':
            post_set = User_Post.objects.all().order_by('-date')
        else:
            # frens posts
            user_followers = current_user.following.all()
            post_set = User_Post.objects.filter(user_id_fk__in = user_followers).order_by('-date')
        print(f"API: got post_set{post_set}")
        pagination = Paginator(post_set, 10)
        total_pages = pagination.num_pages
        if requested_page <= total_pages:
            page_obj = pagination.get_page(requested_page)
        else: # requested_page > total_pages
            if requested_page - total_pages == 1:
                # If requested_page is one more than total pages, signal the Javascript Clinet to display the 'Scroll End Message'
                return JsonResponse({'message': 'API: Scroll End'}, status = 200)
            else:
                return JsonResponse({'message': 'Requested Page Beyond Maximum allowed'}, status=400)
        print(f"API: pagination{page_obj}")  
        # Render the requested page as Html and return  
        print(f"API: starting render")
        page_html = render_page_obj_as_html(request, page_obj, requested_page, postfeed)
        print(f"API: render complete")
        
        return JsonResponse({'html_post_set': page_html, 
                             'message': 'API: Page request Rendered Successfully'}, status=201)
    else:
        return JsonResponse({"message": "API: Bad request. GET required"}, status=400)




        '''
        or checking exceptions example
        try:
            profile = User_Profile.objects.get(user_id_fk = current_user)
        except User_Profile.DoesNotExist:
            return JsonResponse({"error": "Profile not found."}, status=404)
         '''