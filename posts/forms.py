from dataclasses import field
from logging import PlaceHolder
from pyexpat import model
from tkinter import Widget
from xml.etree.ElementTree import Comment
from .models import *
from django import forms
from django.forms import TextInput, ModelForm, DateTimeInput,Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout,Fieldset
from crispy_bootstrap5.bootstrap5 import Field
from captcha.fields import ReCaptchaField

class PostCreationForm(forms.ModelForm):

    class Meta:
        model = post
        # Widgets = {
        #     'title':forms.TextInput(attrs={'class':'single-input','placeholder':'Enter your title'}) 
        # }

        widgets = {
            'title': TextInput(attrs={'class': 'single-input','placeholder':'Enter your title'}),
            # 'category': forms.Textarea(attrs={'class': 'single-input'}),
            'content': forms.Textarea(attrs={'class': 'single-input mt-10','placeholder':'Enter your content'}),
            # 'image': forms.ClearableFileInput(attrs={'class': 'single-input '})
        }

        fields = ['title',
        'category',
        'content',
        'image']

class PostUpdateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(PostUpdateForm, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method='post'
        self.helper.field_class='mt-10'
        self.helper.layout = Layout(
            # 'title','category','content','image','tag'
            Field('title', css_class="single-input",placeholder="yours title"),
            Field('category', css_class="single-input"),
            Field('content', css_class="single-input",placeholder="yours content"),
            Field('image', css_class="single-input"),            
            Field('tag', css_class="single-input",placeholder="yours tag",value=self.instance.post_tag()),
        )
        self.helper.add_input(Submit('submit','Update',css_class="generic-btn success circle"))

    tag = forms.CharField()
    class Meta:
        model=post
        fields = ['title',
        'category',
        'content',
        'image']
        
class CreateCommentForm(forms.ModelForm):

    captcha = ReCaptchaField()

    def __init__(self,*args,**kwargs):
        super(CreateCommentForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method="post"
        self.helper.layout = Layout(
            Field('name',css_class='form-control',Placeholder="Your name"),
            Field('email',css_class='form-control',placeholder="Your E-mail"),
            Field('content',css_class='form-control mb-10',placeholder='Your content'),
            Field('captcha'),
        )

        self.helper.add_input(Submit('submit','Post comment',css_class='primary-btn submit_btn'))

    class Meta:
        model = comment
        fields = ['name','email','content']