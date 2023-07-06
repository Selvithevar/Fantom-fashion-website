from pyexpat import model
from django.contrib import admin
from .models import post,category,Tag,comment
# Register your models here.
class Adminpost(admin.ModelAdmin):
    list_filter = ['publishing_date']
    list_display = ['title','publishing_date']
    search_fields = ['title','content']

    class Meta:
        model = post

class Admincomment(admin.ModelAdmin):
    list_filter = ('publishing_date',)
    search_fields = ('name','email','content','post__title')

    class Meta:
        model = comment

admin.site.register(post,Adminpost)
admin.site.register(category)
admin.site.register(Tag)
admin.site.register(comment,Admincomment)
