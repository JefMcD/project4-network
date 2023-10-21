

from django.urls import include, path
from . import views, api, db_admin, sandbox

app_name = 'network'
urlpatterns = [
    # views paths
    path("", views.entry, name="entry"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>/<str:requested_newsfeed>", views.profile, name='profile'),
    # path("all_posts", views.all_posts, name="all_posts"),

    # Javascript API paths
    path('get_user_profile', api.get_user_profile, name='get_user_profile'),
    path('update_profile', api.update_profile, name='update_profile'),  
    path('follow/<int:user_id>', api.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>', api.unfollow_user, name='unfollow_user'), 
    path('handle_post', api.handle_post, name='create_post'),  
    path('handle_post/<str:post_option>/<int:post_id>', api.handle_post, name='edit_post'),  
    path('remove_post/<int:post_id', api.remove_post, name='remove_post'),
    path('get_newsfeed_page/<int:user_id>/<str:postfeed>/<int:requested_page>', api.get_newsfeed_page, name = 'get_newsfeed_page'),
    path('upduke_post/<int:post_id>', api.upduke_post, name='upduke_post'),
    path('get_post_data/<int:post_id>', api.get_post_data, name = 'get_post_data'),
    
    # db_admin paths
    path('db_admin', db_admin.db_admin, name='db_admin'),
    path('insert_users', db_admin.insert_users, name='insert_users'),
    path('reset_su', db_admin.reset_su, name='reset_su'),
    path('inactive', db_admin.inactive, name='inactive'),
    path('delete_all', db_admin.delete_all, name='delete_all'),
    path('insert_text_posts', db_admin.insert_text_posts, name='insert_text_posts'),
    
    # sandbox
    path('many2many', sandbox.many2many, name='many2many'),
    path('gen_qs', sandbox.gen_qs, name='gen_qs'),
    
    #default
    path("index", views.entry, name='index'),
        
]



