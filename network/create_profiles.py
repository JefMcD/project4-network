import os
from django.conf import settings
from django.core.files import File
from .models import *



def set_instance_img(user_id, model_field, directory, userimage):
    user_instance = User.objects.get(pk = user_id)
    user_name = user_instance.username
    
    user_profile_instance = User_Profile.objects.get(user_id_fk = user_instance)
    
    # '/' isnt used in the pathnames to try to avoid triggering the Djangp path travelling error
    image_path =  os.path.join(settings.MEDIA_ROOT, 'testing_profile_pics', directory, userimage)
    if os.path.exists(image_path):
        with open(image_path, 'rb') as image_file:
            # Cast the opened file to the File() class
            # It then has all the associated methods and variables of this class
            new_image_file = File(image_file)

            # Define the filename the image will have on the filesystem
            new_image_name = f"{user_id}_{user_name}__{userimage}"

            # Save the image to the model field
            if model_field == 'avatar':
                user_profile_instance.avatar.save(new_image_name, new_image_file)
            else:
                user_profile_instance.background_img.save(new_image_name, new_image_file)
            
    else:
        # image_path doesnt exist
        print(f"Default bg_img path Does Not Exist. Tried => {image_path}")

    return





def install_pepe():
    # Create A New Instance of User_Profile
    
    user_pepe = User.objects.get(username = 'pepe')
    print(f"Defining User Profile for Pepe => {user_pepe}")
    user_profile_instance = User_Profile(user_id_fk = user_pepe,
                                         user_profile_folder = 'user_profiles/pepe',
                                         website = 'pepes web',
                                         moniker = 'Pepe',
                                         caption = 'I no freese in these ')
    
    print(f"Saving User Profile")
    user_profile_instance.save()
    print(f"User profile saved for Pepe => {user_profile_instance}")
    
    print(f"installing background_im")
    directory = 'background'
    userimage = '10.jpg'
    model_field = 'background_img'
    set_instance_img(user_pepe.pk, model_field, directory, userimage)
    
    print(f"installing avatar")
    directory = 'avatar'
    userimage = 'pepe2.jpg'
    model_field = 'avatar'
    set_instance_img(user_pepe.pk, model_field, directory, userimage)
    
    return

def install_sheela():
    # Create A New Instance of User_Profile
    
    new_user = User.objects.get(username = 'sheela')
    user_profile_instance = User_Profile(user_id_fk = new_user,
                                         user_profile_folder = 'user_profiles/sheela', 
                                         website = 'FAFO',
                                         moniker = 'Pah',
                                         caption = 'Dont tread on me')
    user_profile_instance.save()

    
    # Install background
    directory = 'background'
    userimage = '55.jpg'
    model_field = 'background_img'
    set_instance_img(new_user.pk, model_field, directory, userimage) 
    
    #Install avatar
    directory = 'avatar'
    userimage = 'dragon.jpg'
    model_field = 'avatar'
    set_instance_img(new_user.pk, model_field, directory, userimage)
    
    return

def install_zoe():
    # Create A New Instance of User_Profile
    
    new_user = User.objects.get(username = 'zoe')
    user_profile_instance = User_Profile(user_id_fk = new_user,
                                         user_profile_folder = 'user_profiles/zoe', 
                                         website = 'Find me',
                                         moniker = 'Whoosh!',
                                         caption = 'Where oh where oh where?')
    user_profile_instance.save()
 
    
    # Install background
    directory = 'background2'
    userimage = 'fish.jpg'
    model_field = 'background_img'
    set_instance_img(new_user.pk, model_field, directory, userimage)
       
    #Install avatar
    directory = 'avatar'
    userimage = 'zoe.jpg'
    model_field = 'avatar'
    set_instance_img(new_user.pk, model_field, directory, userimage)
    
    return

def install_turkle():
    # Create A New Instance of User_Profile
    
    new_user = User.objects.get(username = 'turkle')
    user_profile_instance = User_Profile(user_id_fk = new_user,
                                         user_profile_folder = 'user_profiles/turkle', 
                                         website = 'Turkle-Rocks.com',
                                         moniker = 'Not so fast that Im slow',
                                         caption = 'Fisjing if ya get ma drift')
    user_profile_instance.save()
    
    # Install background
    directory = 'background2'
    userimage = 'money.jpg'
    model_field = 'background_img'
    set_instance_img(new_user.pk, model_field, directory, userimage)
       
    #Install avatar
    directory = 'avatar'
    userimage = 'turk.jpg'
    model_field = 'avatar'
    set_instance_img(new_user.pk, model_field, directory, userimage)
    
    return


def install_bowfren():
    # Create A New Instance of User_Profile
    
    new_user = User.objects.get(username = 'bowfren')
    user_profile_instance = User_Profile(user_id_fk = new_user,
                                         user_profile_folder = 'user_profiles/bowfren', 
                                         website = 'mouse-wheels.com',
                                         moniker = 'Bazzzza',
                                         caption = 'Here for SHort Time Not Hard Time')
    user_profile_instance.save()
    
    # Install background
    directory = 'background2'
    userimage = 'beams.jpg'
    model_field = 'background_img'
    set_instance_img(new_user.pk, model_field, directory, userimage)
       
    #Install avatar
    directory = 'avatar'
    userimage = 'munk.jpg'
    model_field = 'avatar'
    set_instance_img(new_user.pk, model_field, directory, userimage)
    
    return

 
def install_looda():
    # Create A New Instance of User_Profile
    
    new_user = User.objects.get(username = 'looda')
    user_profile_instance = User_Profile(user_id_fk = new_user,
                                         user_profile_folder = 'user_profiles/looda', 
                                         website = 'RaaaWWR.com' ,
                                         moniker = 'Ludicrus Rex',
                                         caption = 'Far of travel and wiide of view')
    user_profile_instance.save()
    
    # Install background
    directory = 'background2'
    userimage = 'balls.jpg'
    model_field = 'background_img'
    set_instance_img(new_user.pk, model_field, directory, userimage)
    
    #Install avatar
    directory = 'avatar'
    userimage = 'boosh.jpg'
    model_field = 'avatar'
    set_instance_img(new_user.pk, model_field, directory, userimage)
    
    return

def install_sparra():
    # Create A New Instance of User_Profile
    
    new_user = User.objects.get(username = 'sparra')
    user_profile_instance = User_Profile(user_id_fk = new_user,
                                         user_profile_folder = 'user_profiles/sparra', 
                                         website = 'sparra is riziin.com',
                                         moniker = 'Sparra',
                                         caption = 'You can safely ignore me')
    user_profile_instance.save()
    
    # Install background
    directory = 'background2'
    userimage = 'birds.jpg'
    model_field = 'background_img'
    set_instance_img(new_user.pk, model_field, directory, userimage)
       
    #Install avatar
    directory = 'avatar'
    userimage = 'tit2.jpg'
    model_field = 'avatar'
    set_instance_img(new_user.pk, model_field, directory, userimage)
    
    return


def install_smol():
    # Create A New Instance of User_Profile
    
    new_user = User.objects.get(username = 'smol')
    user_profile_instance = User_Profile(user_id_fk = new_user,
                                         user_profile_folder = 'user_profiles/smol', 
                                         website = 'VST for All',
                                         moniker = 'Smol',
                                         caption = 'AMbient Vibes ABound')
    user_profile_instance.save()
    
    # Install background
    directory = 'background'
    userimage = '75.jpg'
    model_field = 'background_img'
    set_instance_img(new_user.pk, model_field, directory, userimage)
       
    #Install avatar
    directory = 'avatar'
    userimage = 'gee.jpg'
    model_field = 'avatar'
    set_instance_img(new_user.pk, model_field, directory, userimage)
    
    return


   
def install_user_profiles(network_users):
    # install_fs_user_area(network_users)
        
    # Define the User_Profile Model Fields for each user
    # user_profile_id     = models.AutoField(primary_key=True, db_index=True)
    # user_id_fk          = models.ForeignKey('User', on_delete=models.CASCADE)
    # user_profile_folder = models.CharField(max_length=150)
    # website             = models.CharField(null=True,  blank=True,  max_length=200)
    # background_img      = models.ImageField(null=True, blank=True,  upload_to=folder2)
    # avatar              = models.ImageField(null=True, blank=True,  upload_to=folder2)
    # moniker             = models.CharField(null=True,  blank=True, max_length=45)
    # caption             = models.CharField(null=True,  blank=True, max_length=125)
    
    install_pepe()
    install_sheela()
    install_turkle()
    install_sparra()
    install_bowfren()
    install_looda()
    install_smol()
    install_zoe()
    
    return
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
'''
def install_fs_user_area(network_users):
    
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
    
    
    # Install upload directories for user and Define filesystem directory tree for the users uploads
    # User profile folder for their uploads => BASE_DIR/user_profiles/{username}
    # base_dir = /home/artillery/webdev-apps/courses/CS50/Project-4/network
    
    base_dir = settings.BASE_DIR
    user_profiles_folder = os.path.join(base_dir,'user_profiles')
    media_root = settings.MEDIA_ROOT
    media_url  = settings.MEDIA_URL

    for user in network_users:  
        # so user  == something like {'username':'pepe', 'email': 'pepe@mail.com', 'password': 'passw0rd'},
        network_username = user['username'] 
        current_user = User.objects.get(username = network_username)
        username = current_user.username
    
        user_folder = os.path.join(user_profiles_folder, username)
        if os.path.exists(user_folder):
            print(f"user profile area already exists => {username}")
        else:
            os.mkdir(user_folder)
   
        # Create the following subfolders in the user folder area
        profile_subfolders = ['avatar', 'backgrounds', 'music', 'video', 'images', 'tools', 'docs']
        for subfolder in profile_subfolders:
            new_folder = os.path.join(user_folder, subfolder)
            if os.path.exists(new_folder):
                print(f"user profile subfolder already exists => {new_folder}")
            else:
                os.mkdir(new_folder)
        
    return
'''






'''
def install_pepe_v0():
    user_pepe = User.objects.get(username = 'pepe')
    user_id_121 = user_pepe,
    user_profile_fk = user_pepe
    user_profile_folder = 'user_profiles/pepe', 
    website = 'pepe.com'
    moniker = 'Comin At ya'
    caption = 'I no freese'



    #create ImageField object for background_img
    # https://stackoverflow.com/questions/4258605/django-manually-create-imagefield-in-model-from-existing-file-on-server
    from django.core.files import File

    av_img_path = os.path.join(settings.MEDIA_ROOT, 'testing_profile_pics', 'avatar', 'pepe2.jpg')
    bg_img_path =  os.path.join(settings.MEDIA_ROOT, 'testing_profile_pics', 'background', '10.jpg')
    # image_model.image_field('path', File().read())
    bg_img = 'profile_pics/1.jpg'

    from django.core.files.images import ImageFile
    #user_profile_instance = User_Profile.objects.create()                                                                
    #user_profile_instance.background_img = ImageFile(open(bg_img, "rb"))      
    user_profile_instance = User_Profile(   user_id_fk = user_pepe,
                                            user_id_121 = user_pepe,
                                            user_profile_folder = 'user_profiles/pepe', 
                                            website = 'pepe.com',
                                            moniker = 'Comin At ya',
                                            caption = 'I no freese',
                                            background_img = ImageFile(open(bg_img, "rb")),
                                            avatar = ImageFile(open(bg_img, "rb")),
                                        )
    
    user_profile_instance.save()
'''