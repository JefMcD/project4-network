from django import forms
from .models import User_Profile



class New_Post_Form(forms.Form):

    title  = forms.CharField(label='', required=True, max_length=45,
                                widget=forms.TextInput(
                                    attrs={
                                        'placeholder': 'Post Title',
                                        'class': 'post-input',
                                        'id': 'post-title',
                                        'size': 10
                                    }
                                ))
    
    message   = forms.CharField(label='',  required=False, max_length=500,
                                widget=forms.Textarea(
                                    attrs={
                                        'placeholder': 'Message Body',
                                        'class':'post-textarea-input',
                                        'id': 'post-message',
                                    }
                                ))  
    
class New_Post_Media_Form(forms.Form):  
    image_file    = forms.ImageField(label='', required = False, 
                                widget=forms.ClearableFileInput(
                                    attrs={
                                    'class': 'edit-profile-input choose-file-btn',
                                    'id': 'post-image',
                                    }
                                ))







# Creating Actual Forms seems to be more straightforward for styling and control
# but is more troublesome when it comes to transferring the uploaded images into the database/filesystem
# modelForms will take care of that and map them directly but require all fields be submitted
# and is Hellish to get working to update ImageFields with new images
class Edit_User_Profile_Form(forms.Form):
    
    background_img      = forms.ImageField(label='Backdrop', required = False, 
                                          widget=forms.ClearableFileInput(
                                              attrs={
                                                'class': 'edit-profile-input',
                                                'id': 'edit-profile-background-img',
                                              }
                                            ))
    
    avatar              = forms.ImageField(label='Avatar', required = False, 
                                          widget=forms.ClearableFileInput(
                                              attrs={
                                                'class': 'edit-profile-input choose-file-btn',
                                                'id': 'edit-profile-avatar',
                                              }
                                            ))
    
    moniker             = forms.CharField(label='A.K.A', required=False, max_length=45,
                                          widget=forms.TextInput(
                                              attrs={
                                                  'class': 'edit-profile-input',
                                                  'id': 'edit-profile-moniker',
                                                  'size': 10
                                              }
                                          ))
    
    website             = forms.CharField(label='Website', initial='http://www.', required=False, max_length=200,
                                         widget=forms.TextInput(
                                             attrs={
                                                 'class':'edit-profile-input',
                                                 'id': 'edit-profile-website',
                                                 'size': 25,
                                             }
                                         ))
    

    caption             = forms.CharField(label = 'Blurb', required=False, max_length=200,
                                         widget=forms.TextInput(
                                             attrs={
                                                 'class':'edit-profile-input',
                                                 'id': 'edit-profile-caption',
                                                 'size': 25,
                                             }
                                         ))
    
    












# Creating models Forms
# https://www.geeksforgeeks.org/django-modelform-create-form-from-models/
# Styling the ModelForm
# https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#overriding-the-default-fields

# Django ModelForms are designed to be completed in FULL
# They dont appear to work if you want to only update One field
# for example, if you only want to change your profile avatar and nothing else
# The seem designed to handle a one time submission scenario adn arnt suited to this task
## Time to RollYerOwn brutha. This is left just for inframational #CodeHoarding
class Edit_User_Profile_ModelForm(forms.ModelForm):
    class Meta:
        model = User_Profile
        # fields = "__all__" # Sets all fields of the form to be used
        fields = ['background_img', 'avatar', 'moniker', 'website','caption']
        #exclude = ['user_profile_id', 'user_id_fk', 'user_profile_folder']

        labels = {  'background_img': 'Main Pic',
                    'avatar': 'Avatar',
                    'moniker': 'A.K.A',
                    'website': 'Website',
                    'caption': 'ABout Me'
        }
        
        widgets = {
            'background_img': forms.ClearableFileInput(
                attrs={'class': 'edit-profile-input',
                        'id': 'edit-profile-background_img'}
            ),
            
            'avatar': forms.ClearableFileInput(
                attrs={'class': 'edit-profile-input',
                        'id': 'edit-profile-avatar'}
            ),
                      
            'moniker': forms.TextInput(
                attrs={'class': 'edit-profile-input',
                        'id': 'edit-profile-moniker',
                        'max_length': 20}
            ),
                     
            'website': forms.TextInput(
                attrs={'class': 'edit-profile-input',
                        'id': 'edit-profile-website',
                        'max_length': 20}
            ),
            
            'caption': forms.TextInput(
                attrs={'class': 'edit-profile-input',
                        'id': 'edit-profile-caption',
                        'max_length': 20, }
            )           
        }
        
            
    # https://stackoverflow.com/questions/16205908/django-modelform-not-required-field
    def __init__(self, *args, **kwargs):
        super(Edit_User_Profile_ModelForm, self).__init__(*args, **kwargs)
        self.fields['background_img'].required = False
        self.fields['avatar'].required = False
        self.fields['moniker'].required = False
        self.fields['website'].required = False
        self.fields['caption'].required = False      
           

