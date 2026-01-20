from django.contrib import admin
from .models import BlogPost

# Register your models here.

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'updated')
    list_filter = ('created', 'updated', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
