from django.contrib import admin
#Importing Models
from .models import Post, Category

#Blog Post and Category will be accesible from admin area
admin.site.register(Post)
admin.site.register(Category)