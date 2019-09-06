from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('set_nickname/', views.set_nickname, name='set_nickname'),
    path('logout/', views.logout, name='logout'),
    path('chat/', views.chat, name='chat'),
    path('post/', views.post_message, name='post'),
]