from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('<str:slug>/', blog_post_details_view),
    path('', blog_post_list_view, name="Blogpost"),
    path('<str:slug>/edit/', blog_post_update_view, name="Blogpost_update"),
    path('<str:slug>/delete/', blog_post_delete_view, name="Blogpost_delete"),
    
    
]
