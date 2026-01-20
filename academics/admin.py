# academics/admin.py
from django.contrib import admin
from .models import Course, Subject, Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("title", "course")
    list_filter = ("course",)
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "subject")
    list_filter = ("subject__course", "subject")
    search_fields = ("title", "content")