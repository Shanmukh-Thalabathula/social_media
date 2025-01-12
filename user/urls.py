from django.urls import path
from .views import user_login, user_logout, user_register, user_profile, edit_user_profile, follow, unfollow

urlpatterns = [
    path('', user_login, name='user-login'),
    path('user-logout/', user_logout, name='user-logout'),
    path('user-register/', user_register, name='user-register'),
    path('user-profile/<str:username>/',user_profile,name='user-profile'),
    path('edit-user-profile/',edit_user_profile,name='edit-user-profile'),
    path('follow/<str:username>/',follow,name='follow'),
    path('unfollow/<str:username>/',unfollow,name='unfollow'),
]
