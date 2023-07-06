"""fantom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from .views import *
# from .apps import PostsConfig

# app_name = PostsConfig.name

urlpatterns = [
    path('',index.as_view(),name="index"),
    path('detail/<int:pk>/<slug:slug>',postdetail.as_view(),name='detail'),
    path('post-update/<int:pk>/<slug:slug>',UpdatePostView.as_view(),name='post-update'),
    path('post-delete/<int:pk>/<slug:slug>',DeletePostView.as_view(),name='post-delete'),
    path('category/<int:pk>/<slug:slug>',categorydetail.as_view(),name='category_detail'),
    path('tag/<slug:slug>',TagDetail.as_view(),name='tag_detail'),
    path('post_create/',CreatePostView.as_view(),name='create_post'),
    path('search/',SearchView.as_view(),name='search'),



] 
