from ast import Index
from audioop import reverse
from http.client import HTTPResponse
from msilib.schema import Class
from multiprocessing import context
from pipes import Template
from re import template
from turtle import title
from unicodedata import category, name
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.shortcuts import get_object_or_404
from .forms import CreateCommentForm, PostCreationForm, PostUpdateForm
from .models import post,category,Tag
from django.contrib.auth.decorators import login_required
from django.utils.decorators import  method_decorator
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db.models import F,Q
from django.views.generic.edit import FormMixin



class index(ListView):
    template_name = "index.html"
    model = post
    context_object_name = 'post'
    paginate_by = 3

    def get_context_data(self,*,object_list=None, **kwargs):
        context = super(index, self).get_context_data(**kwargs)
        context['slider_post'] = post.objects.all().filter(slider_post=True)
        return context

@method_decorator(login_required(login_url='http://127.0.0.1:8000/users/login/'),name="dispatch")
class postdetail(DetailView,FormMixin):
    template_name = 'detail.html'
    model = post
    context_object_name= 'single'
    form_class = CreateCommentForm

    def get(self, request,*args,**kwargs):
        self.hit = post.objects.filter(id=self.kwargs['pk']).update(hit=F('hit')+1)
        return super(postdetail,self).get(request,*args,**kwargs)
    
    def get_context_data(self,*,object_list=None, **kwargs):
        context = super(postdetail, self).get_context_data(**kwargs)
        context['previous'] = post.objects.filter(id__lt=self.kwargs['pk']).order_by('-pk').first()
        context['next'] = post.objects.filter(id__gt=self.kwargs['pk']).order_by('pk').first()
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        if form.is_valid():
            form.instance.post = self.object
            form.save()
            return super(postdetail,self).form_valid(form)
        else:
            return super(postdetail,self).form_invalid(form)

    def post(self,*args,**kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_valid(form)

    def get_success_url(self):
        return reverse('detail',kwargs={"pk":self.object.pk,"slug":self.object.slug})


@method_decorator(login_required(login_url='http://127.0.0.1:8000/users/login/'),name="dispatch")
class categorydetail(ListView):    
    model = post
    template_name = 'category_detail.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        self.category = get_object_or_404(category,pk=self.kwargs['pk'])
        return post.objects.filter(category=self.category).order_by('-id')

    def get_context_data(self,*,object_list=None,**kwargs):
        context = super(categorydetail,self).get_context_data(**kwargs)
        self.category = get_object_or_404(category,pk=self.kwargs['pk'])
        context['category']=self.category
        return context

@method_decorator(login_required(login_url='http://127.0.0.1:8000/users/login/'),name="dispatch")
class TagDetail(ListView):
    model = post
    template_name = 'tag_detail.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        self.tag = get_object_or_404(Tag,slug=self.kwargs['slug'])
        return post.objects.filter(tag=self.tag).order_by('id')

    def get_context_data(self,**kwargs):
        context=super(TagDetail,self).get_context_data(**kwargs)
        self.tag = get_object_or_404(Tag,slug=self.kwargs['slug'])
        context['tag']=self.tag
        return context

@method_decorator(login_required(login_url='http://127.0.0.1:8000/users/login/'),name="dispatch")
class CreatePostView(CreateView):
    template_name = 'create_post.html'
    form_class = PostCreationForm
    model = post

    def get_success_url(self):
        return reverse('detail',kwargs = {"pk":self.object.pk,"slug":self.object.slug})    

    def form_valid(self,form):
        form.instance.user = self.request.user
        form.save()
        form.instance.tag.clear()

        tags = self.request.POST.get("tag").split(",")

        for tag in tags:
            current_tag = Tag.objects.filter(slug=slugify(tag))
            if current_tag.count()<1:
                create_tag = Tag.objects.create(title=tag)
                form.instance.tag.add(create_tag)
            else:
                existed_tag = Tag.objects.get(slug=slugify(tag)) 
                form.instance.tag.add(existed_tag)
            return super(CreatePostView,self).form_valid(form)

@method_decorator(login_required(login_url='/login'),name="dispatch")
class UpdatePostView(UpdateView):
    model = post
    template_name = 'post-update.html'
    form_class = PostUpdateForm

    def get_success_url(self):
        return reverse('detail',kwargs = {"pk":self.object.pk,"slug":self.object.slug})

    def form_valid(self,form):
        form.instance.user = self.request.user
        form.instance.tag.clear()

        tags = self.request.POST.get("tag").split(",")

        for tag in tags:
            current_tag = Tag.objects.filter(slug=slugify(tag))
            if current_tag.count()<1:
                create_tag = Tag.objects.create(title=tag)
                form.instance.tag.add(create_tag)
            else:
                existed_tag = Tag.objects.get(slug=slugify(tag)) 
                form.instance.tag.add(existed_tag)
            return super(UpdatePostView,self).form_valid(form)
        
    def get(self,request,*args,**kwargs):
        self.object = self.get_object()

        if self.object.user != request.user:
            return HttpResponseRedirect('/')
        return super(UpdatePostView, self).get(request,*args,**kwargs)

class DeletePostView(DeleteView):
    model = post
    success_url = '/'
    template_name = 'delete.html'

    def delete(self, request, *args,**kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseRedirect(self.success_url)

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect('/')            
        return super(DeletePostView,self).get(request,*args,**kwargs)

class SearchView(ListView):
    model = post
    template_name = 'search.html'
    paginate_by = 5
    context_object_name = "posts"

    def get_queryset(self):
        query = self.request.GET.get("q")

        if query:
            return post.objects.filter(Q(title__icontains=query) | 
                                       Q(content__icontains=query) | 
                                       Q(tag__title__icontains=query)                                      
                                        ).order_by('id').distinct()
        return post.objects.all().order_by('id')                                