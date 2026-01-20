from django.contrib import admin
from .models import Course, Module, Content


class ContentInline(admin.StackedInline):
    model = Content
    extra = 1
    fields = ('main_title', 'title', 'content', 'code', 'code_language')
    show_change_link = True
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['code_language'].widget
        widget.attrs['style'] = 'width: 200px;'  # Make the code language dropdown wider
        return formset


class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1
    fields = ('title', 'description', 'order')
    show_change_link = True


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at', 'updated_at')
    list_filter = ('course',)
    inlines = [ContentInline]

    search_fields = [
        'title',
        # 'description',
        'content__title',         # ← This is correct now
        # 'content__description',   # if Content model has description
        # 'content__text',        # if it's Text model
        # 'content__video__url',  # if you want to search inside video URLs, etc.
    ]
    # THIS IS THE ONLY LINE YOU NEED TO ADD ↓↓↓
    # search_fields = ['title', 'description', 'contents__title', 'contents__description']
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            # Only process Module instances for ordering
            if isinstance(instance, Module):
                if not hasattr(instance, 'order') or instance.order is None:
                    # Set a default order if not set
                    last_order = Module.objects.filter(course=instance.course).order_by('-order').first()
                    instance.order = last_order.order + 1 if last_order else 1
            instance.save()
        formset.save_m2m()


        


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['id', 'main_title', 'module', 'created_at']
    list_filter = ('module__course', 'module')
    
    def save_model(self, request, obj, form, change):
        # If this is a new content and module doesn't have an order, set it
        if not change and obj.module and (not hasattr(obj.module, 'order') or obj.module.order is None):
            last_module = Module.objects.filter(course=obj.module.course).order_by('-order').first()
            obj.module.order = last_module.order + 1 if last_module else 1
            obj.module.save()
        super().save_model(request, obj, form, change)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['code_language'].widget.attrs['style'] = 'width: 200px;'
        return form
