"""dapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from blog.views import *
from blog import views
from .views import *

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name="home"),
    path('blog_post_new/', blog_post_create_view, name="createblog"),
    path('contact/', contact_page, name="contact"),
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name="logout"),
    ####### API URLS #########

    path('api/blog', views.BlogPost_list),
    path('api/blog/<int:id>',views.BlogPost_detail_view),
    path('api/blog/register',views.registerView),

    path('api/blog/userproperties',views.user_properties_view),
    path('api/blog/userproperties/edit',views.user_properties_update_view),

    path('api/blog/login', obtain_auth_token),
    path('api/blog/pagination', APIBlogListView.as_view()),
    path('api/blog/searching', APISearchView.as_view()),




    path('blog_post/', include('blog.urls')),
]
