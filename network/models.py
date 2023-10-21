from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q, Deferrable, UniqueConstraint
from django.conf import settings
import os


# Notes on Unary recursive Many-to-Many relationships
#
# https://docs.djangoproject.com/en/1.11/topics/db/examples/many_to_many/
# https://stackoverflow.com/questions/46268059/django-many-to-many-recursive-relationship
# 
# Literal Translation from ERD of Table Definitions for Many to Many Relationships
#
# class Follow(models.Model):
#   user_id_fk      = models.ForeignKey('User', on_delete=models.CASCADE)
#   follower_id_fk  = models.ForeignKey('User', on_delete=models.CASCADE)
#   
# class Subscribe(models.Model):
#    user_id_fk      = models.ForeignKey('User', on_delete=models.CASCADE)
#    follower_id_fk  = models.ForeignKey('User', on_delete=models.CASCADE)
#   
# class Mute(models.Model):
#    user_id_fk      = models.ForeignKey('User', on_delete=models.CASCADE)
#    follower_id_fk  = models.ForeignKey('User', on_delete=models.CASCADE)
#   
# class Block(models.Model):
#   user_id_fk      = models.ForeignKey('User', on_delete=models.CASCADE)
#   follower_id_fk  = models.ForeignKey('User', on_delete=models.CASCADE)
    
    
# Django Definitions of Many 2 Many Relationships
# Unary Recursive relationships between members of User
#
# normally, M2M-relations are symmetrical. 
# That means, that if you set User A as follower of User B, querysets will also return User B as follower of User A.
# You can avoid such behavior by adding symmetrical=False option to the field: 

class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    
    def __str__(self):
        return f"{self.pk}, {self.username}, {self.email}"

# Add a many-to-many self-referential relationship
# User.add_to_class('following', models.ManyToManyField('self', symmetrical=False, related_name='followers'))


class User_Profile(models.Model):
    # Define class methods

    def user_avatar_upload_path(instance, filename):

        print("############# user_avatar_upload_path ######################")
        # Get the user's destination_folder
        # instance is this instance
        # filename is the name of the file and is supplied by Django via the ImageField
        uname_instance = instance.user_id_fk
        uname = uname_instance
        print(f"############## uname => {uname}")
        a = os.path.join('avatar',filename)
        destination_folder = os.path.join(instance.user_profile_folder,a)

        # Construct the upload path. Use os.path.join to ensure the path is constructed correctly
        # eg, if destination_folder is 'user_1', and filename is 'avatar.jpg' => 'user_1/avatar.jpg'
        return os.path.join(destination_folder, filename)

    
    def get_username(self):
        return self.user_id_fk.username
    

    media_url = settings.MEDIA_URL
    
    # Note: these joins will create paths with a '/' in them such as 'default/av.jpg'
    # Django security may throw a 'path traversing' error when it encounters this because
    # it seems to flag anything containing '..' or '/' to prevent hacking attempts
    default_media_url  = os.path.join(media_url,'default')
    default_avatar      = os.path.join(default_media_url,'av.jpg')
    default_background  = os.path.join(default_media_url,'bg.jpg')
 
   # Define class Variables
    background_pics = 'backgrounds_pics'
    avatar_pics = 'avatar_pics'
    
    # Therefore the django uses the MEDIA_URL as the base path for the upload_to
    # Define Model Fields
    user_profile_id     = models.AutoField(primary_key=True, db_index=True)
    user_id_fk          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile')
    mutes_m2m           = models.ManyToManyField(User, related_name = 'user_profile_mutes_set' )
    user_profile_folder = models.CharField(null=True, blank=True,  max_length=150)
    website             = models.CharField(null=True,  blank=True, default=get_username, max_length=200)
    moniker             = models.CharField(null=True,  blank=True, max_length=45)
    caption             = models.CharField(null=True,  blank=True, max_length=125)

    background_img      = models.ImageField(null=True, blank=True,  upload_to=background_pics)
    avatar              = models.ImageField(null=True, blank=True,  upload_to=avatar_pics)

    def serialize(self):
        return {
            "user_profile_id": self.user_profile_id,
            "user_id": self.user_id_fk.pk,
            "username": self.user_id_fk.username,
            "website": self.website,
            "moniker": self.moniker,
            "caption": self.caption,
            "background_img_url": self.background_img.url,
            "avatar_url": self.avatar.url
        }

    # Define how class will be represented in Django Admin Screens
    def __str__(self):
        return f"user_profile_id = {self.user_profile_id}, user_id_fk = {self.user_id_fk}, profile_folder = {self.user_profile_folder}, website = {self.website}, bg_img = {self.background_img}, avatar = {self.avatar} ,moniker = {self.moniker}, caption = {self.caption} "
    

class User_Post(models.Model):
    
    user_img_posts = 'user_img_posts'
    
    user_post_id   = models.AutoField(primary_key=True,db_index=True) # Primay Key
    user_id_fk     = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_post_set') # The user who made the post
    title          = models.CharField(null=True, blank=True, max_length=150) # Title of the Post
    message        = models.CharField(null=True, blank=True, max_length=512,) # Message Body of the Post. 
    
    # Many2Many field over-riding the default Django through table
    # https://www.sankalpjonna.com/learn-django/the-right-way-to-use-a-manytomanyfield-in-django 
    # https://docs.djangoproject.com/en/3.1/topics/db/models/#many-to-many-relationships
    # https://docs.djangoproject.com/en/3.1/topics/db/models/#extra-fields-on-many-to-many-relationships
    # https://docs.djangoproject.com/en/3.1/ref/models/constraints/#django.db.models.UniqueConstraint
    engagement     = models.ManyToManyField(User, through='Engagement_m2m', related_name='user_post_engagement_set') # Set of Users who have engaged with th epost
    
    image_file     = models.ImageField(null=True, blank=True,  upload_to=user_img_posts, default=None) # Image file uploaded with the post
    date           = models.DateTimeField(auto_now_add=True) # Date the Post was made
        
        
    def serialize(self):
        data = {
            "user_post_id": self.user_post_id,
            "user_id_fk": self.user_id_fk.pk,
            "title": self.title,
            "message": self.message,
            "date": self.date,
        }
        if self.image_file:
            data["image_file_url"] = self.image_file.url
        else:
            data["image_file_url"] = None
            
        return data

    # Define how class will be represented in Django Admin Screens 
    def __str__(self):
        return f"user_post_id: {self.user_post_id}, user_id_fk: {self.user_id_fk}, title: {self.title}, message: {self.message}, image_file: {self.image_file.name}, engagement: {self.engagement}, date: {self.date}"


class Engagement_m2m(models.Model):
    user            = models.ForeignKey(User,on_delete=models.CASCADE, related_name='engagement_m2m_user_set')
    user_post       = models.ForeignKey(User_Post,on_delete=models.CASCADE, related_name='engagement_m2m_post_set')
    upduke          = models.IntegerField(null=False, default = 0)
    date            = models.DateTimeField(auto_now_add=True) 
    
    UniqueConstraint(fields = ['user', 'user_post'], name = 'engagement_primary_key')



"""
class many_2_many_unary_relationship(models.Model):
    # This is just for information on how these are defined
    follows_m2m = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
    subscribes_to_m2m = models.ManyToManyField('self', related_name='subscribed_to_by', symmetrical=False)
    mutes_m2m = models.ManyToManyField('self',  related_name='muted_by', symmetrical=False)
    blocks_m2m = models.ManyToManyField('self', related_name='blocked_by', symmetrical=False)
""" 










































'''
class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

class User_Profile(models.Model):
    avatar_pics = 'avatar_pics'
    
    user_profile_id     = models.AutoField(primary_key=True, db_index=True)
    user_id_fk          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile_set')
    mutes               = models.ManyToManyField(User, related_name='user_profile_mutes_set')
    moniker             = models.CharField(null=True,  blank=True, max_length=45)
    avatar              = models.ImageField(null=True, blank=True,  upload_to=avatar_pics)

class User_Post(models.Model):
    
    user_img_posts = 'user_img_posts'
    
    user_post_id   = models.AutoField(primary_key=True,db_index=True)
    user_id_fk     = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_post_set')
    title          = models.CharField(null=True, blank=True, max_length=150)
    message        = models.CharField(null=True, blank=True, max_length=512)

    engagement     = models.ManyToManyField(User, through='Engagement_m2m', related_name='user_post_engagement_set')
    
    image_file     = models.ImageField(null=True, blank=True,  upload_to=user_img_posts)
    date           = models.DateTimeField(auto_now_add=True)
        

class Engagement_m2m(models.Model):
    user            = models.ForeignKey(User,on_delete=models.CASCADE, related_name='engagement_user_set')
    user_post       = models.ForeignKey(User_Post,on_delete=models.CASCADE, related_name='engagement_post_set')
    upduke          = models.IntegerField(default=0)
    date            = models.DateTimeField(auto_now_add=True) 
    
    UniqueConstraint(fields = ['user', 'user_post'], name = 'engagement_primary_key')
    

'''

