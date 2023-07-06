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
from django.contrib.auth import views as authViews
app_name = 'users_app'

urlpatterns = [
    path('register/',RegisterView.as_view(),name="register"),
    path('',UserListView.as_view(),name="user_list"),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
    path('myprofile/',UserProfileView.as_view(),name='my-profile'),
    path('<int:pk>/',UserPostView.as_view(),name='user_posts'),
    path('update-profile/<slug:slug>/',UserProfileUpdateView.as_view(),name='update_profile'),
    path('password_change/',authViews.PasswordChangeView.as_view(),name='password_change'),
    path('password_change_done/',authViews.PasswordChangeDoneView.as_view(),name="password_change_done"),

] 
