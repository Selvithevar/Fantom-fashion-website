from re import template
from telnetlib import LOGOUT
from venv import create
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView,UpdateView,ListView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.messages.views import SuccessMessageMixin

from users_app.models import UserProfile
from posts.models import post

from .forms import RegisterForm,UserProfileForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import  method_decorator
from django.urls import reverse


# Create your views here.
class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'

class UserLoginView(LoginView):
    template_name = "login.html"

class UserLogoutView(LogoutView):
    template_name = "logout.html"

# @method_decorator(login_required(login_url='/login'),name="dispatch")
# class UserProfileUpdateView(UpdateView):
   
@method_decorator(login_required(login_url='login/'),name="dispatch")
class UserProfileUpdateView(SuccessMessageMixin,UpdateView):
    model = UserProfile
    template_name = 'profile-update.html'
    form_class = UserProfileForm
    success_message = "Your Profile Has Been Updated!!!"


    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(UserProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('users_app:update_profile',kwargs={'slug':self.object.slug})
    
    
    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect('/')
        
        return super(UserProfileUpdateView, self).get(request,*args,**kwargs)

@method_decorator(login_required(login_url='login/'),name='dispatch')
class UserProfileView(ListView):
    template_name = 'my-profile.html'
    model= post
    context_object_name = 'userposts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(UserProfileView,self).get_context_data(**kwargs)
        context['userprofile']=UserProfile.objects.get(user=self.request.user)
        return context

    def get_queryset(self):
        return post.objects.filter(user=self.request.user).order_by('-id')

class UserPostView(ListView):
    template_name = 'user-post.html'
    model = post
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return post.objects.filter(user=self.kwargs['pk'])

class UserListView(ListView):
    template_name = 'user-list.html'
    model = UserProfile
    context_object_name = 'profiles'
    paginate_by = 5

    def get_context_data(self,**kwargs):
        context= super(UserListView,self).get_context_data(**kwargs)
        return context