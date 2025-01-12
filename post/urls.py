from django.urls import path
from . views import *
urlpatterns = [
    path('home/',home,name='home'),
    path('create-post/',create_post,name='create-post'),
    path('explore-users/',explore_users,name='explore-users'),
    path('like-post/<int:post_id>/', like_post, name='like-post'),
]