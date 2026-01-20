from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
import markdown
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Course, Module, Content
from .serializers import CourseSerializer, ModuleSerializer, ContentSerializer

# views.py

# def courses_list(request):
#     """View function to display all courses in a card-based layout."""
#     courses = Course.objects.all().order_by('-created_at')
#     return render(request, 'courses/courses_list.html', {'courses': courses})
# from django.db.models import Q

# def courses_list(request):
#     """View function to display all courses with optional search."""
#     courses = Course.objects.all().order_by('-created_at')
    
#     # === Search functionality ===
#     query = request.GET.get('q', '').strip()
#     if query:
#         courses = courses.filter(
#             Q(title__icontains=query) | 
#             Q(description__icontains=query)
#         )

#     # Optional: keep the search term in context so we can refill the input
#     context = {
#         'courses': courses,
#         'search_query': query,   # for keeping the input value
#     }
#     return render(request, 'courses/courses_list.html', context)

# from django.shortcuts import render
# from django.db.models import Q
# from .models import Course

# def courses_list(request):
#     courses = Course.objects.all().order_by('-created_at')
#     query = request.GET.get('q', '').strip()

#     if query:
#         courses = courses.filter(title__icontains=query)  # ONLY TITLE SEARCH

#     context = {
#         'courses': courses,
#         'search_query': query
#     }

#     # HTMX partial render
#     if request.headers.get('HX-Request'):
#         return render(request, 'courses/_course_grid.html', context)

#     return render(request, 'courses/courses_list.html', context)


def courses_list(request):
    courses = Course.objects.all().order_by('-created_at')
    query = request.GET.get('q', '').strip()

    if query:
        courses = courses.filter(title__icontains=query)

    context = {'courses': courses}

    if request.headers.get('HX-Request'):
        return render(request, 'courses/_course_grid.html', context)

    return render(request, 'courses/courses_list.html', context | {'courses': courses})




def course_detail(request, slug):
    """View function to display a single course with its modules and content."""
    course = get_object_or_404(Course, slug=slug)
    modules = course.modules.all().order_by('order')
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules
    })

# courses/views.py
from django.shortcuts import get_object_or_404, render
from django.utils.safestring import mark_safe
import markdown
from markdown_katex import KatexExtension
from .models import Module


def module_detail(request, course_slug, module_id):
    module = get_object_or_404(
        Module,
        id=module_id,
        course__slug=course_slug
    )

    content = getattr(module, 'content', None)
    content_html = None

    if content and getattr(content, 'content', None):
        raw_text = content.content

        content_html = markdown.markdown(
            raw_text,
            extensions=[
                'nl2br',
                'fenced_code',
                'codehilite',
                'toc',
                'tables',
                KatexExtension(),          # <-- no args!
            ],
            extension_configs={'codehilite': {'linenums': False}}
        )
        content_html = mark_safe(content_html)

    context = {
        'module': module,
        'content': content,
        'content_html': content_html,
    }

    return render(request, 'courses/module_detail.html', context)







# courses/views.py
# from django.shortcuts import get_object_or_404, render
# from django.utils.safestring import mark_safe
# import markdown
# from markdown_katex import KatexExtension
# from .models import Module


# def module_detail(request, course_slug, module_id):
#     # Fetch module with course slug validation
#     module = get_object_or_404(
#         Module,
#         id=module_id,
#         course__slug=course_slug
    # )

    # Get related content object
    # content_obj = getattr(module, 'content', None)
    # content_html = None

    # if content_obj and hasattr(content_obj, 'content') and content_obj.content:
        # raw_text = content_obj.content

        # # Render Markdown with KaTeX, code highlighting, tables, etc.
        # content_html = markdown.markdown(
        #     raw_text,
        #     extensions=[
        #         'nl2br',           # Convert newlines to <br>
        #         'fenced_code',     # ``` code blocks
        #         'codehilite',      # Syntax highlighting
        #         'toc',             # Table of contents
        #         'tables',          # GitHub-style tables
        #         KatexExtension(),  # Math rendering with KaTeX
        #     ],
        #     extension_configs={
        #         'codehilite': {
        #             'linenums': False,
        #             'guess_lang': False,
        #         }
        #     }
        # )
        # # Mark as safe since it's admin-controlled content
        # content_html = mark_safe(content_html)

    # Optional: Get previous and next modules for navigation
    # modules = module.course.modules.all().order_by('order')
    # prev_module = modules.filter(order__lt=module.order).last() if hasattr(module, 'order') else None
    # next_module = modules.filter(order__gt=module.order).first() if hasattr(module, 'order') else None

    # context = {
    #     'module': module,
    #     'content': content_obj,        # Original content object (for fields like title, code, etc.)
    #     # 'content_html': content_html,  # Rendered Markdown HTML
    #     # 'prev_module': prev_module,
    #     # 'next_module': next_module,
    # }

    # return render(request, 'courses/module_detail.html', context)


# courses/views.py
# from django.shortcuts import get_object_or_404, render
# from django.utils.safestring import mark_safe
# import markdown
# from markdown_katex import KatexExtension
# from .models import Module


# def module_detail(request, course_slug, module_id):
#     module = get_object_or_404(
#         Module,
#         id=module_id,
#         course__slug=course_slug
#     )

#     # --- Render content_a (existing) ---
#     content_a = getattr(module, 'content_a', None)
#     content_a_html = None

#     if content_a and getattr(content_a, 'content', None):
#         raw_text = content_a.content

#         content_a_html = markdown.markdown(
#             raw_text,
#             extensions=[
#                 'nl2br',
#                 'fenced_code',
#                 'codehilite',
#                 'toc',
#                 'tables',
#                 KatexExtension(),
#             ],
#             extension_configs={'codehilite': {'linenums': False}}
#         )
#         content_a_html = mark_safe(content_a_html)

#     # --- NEW: Render content (if exists) ---
    
#     content_obj = getattr(module, 'content', None)
#     content_html = None

#     if content_obj:
#         raw_text = getattr(content_obj, 'content', '') or getattr(content_obj, 'body', '') or str(content_obj)

#         content_html = markdown.markdown(
#             raw_text,
#             extensions=[
#                 'nl2br',
#                 'fenced_code',
#                 'codehilite',
#                 'toc',
#                 'tables',
#                 KatexExtension(),
#             ],
#             extension_configs={'codehilite': {'linenums': False}}
#         )
#         content_html = mark_safe(content_html)

#     # --- Context ---
#     context = {
#         'module': module,
#         'content_a': content_a,
#         'content_a_html': content_a_html,
#         'content': content_obj,           # original object
#         'content_html': content_html,     # rendered Markdown
#     }

#     return render(request, 'courses/module_detail.html', context)









# courses/views.py
# from django.shortcuts import get_object_or_404, render
# from django.utils.safestring import mark_safe
# import markdown
# from markdown_katex import KatexExtension
# from .models import Module


# def _render_markdown(text):
#     if not text:
#         return None

#     return mark_safe(markdown.markdown(
#         text,
#         extensions=[
#             'nl2br',
#             'fenced_code',
#             'codehilite',
#             'toc',
#             'tables',
#             KatexExtension(
#                 # delimiters=[
#                 #     {'left': '$$', 'right': '$$', 'display': True},
#                 #     {'left': '\\[', 'right': '\\]', 'display': True},
#                 #     {'left': '$', 'right': '$', 'display': False},
#                 #     {'left': '\\(', 'right': '\\)', 'display': False},
#                 # ]
#             ),
#         ],
#         extension_configs={'codehilite': {'linenums': False}}
#     ))


# def module_detail(request, course_slug, module_id):
    module = get_object_or_404(Module, id=module_id, course__slug=course_slug)

    content_a = getattr(module, 'content_a', None)
    content_obj = getattr(module, 'content', None)

    content_a_html = _render_markdown(getattr(content_a, 'content', '')) if content_a else None
    content_html = _render_markdown(
        getattr(content_obj, 'content', '') or
        getattr(content_obj, 'body', '') or
        str(content_obj)
    ) if content_obj else None

    context = {
        'module': module,
        'content_a_html': content_a_html,
        'content_html': content_html,
    }
    return render(request, 'courses/module_detail.html', context)


# courses/views.py
# from django.shortcuts import get_object_or_404, render
# from django.utils.safestring import mark_safe
# import markdown
# from markdown_katex import KatexExtension
# from .models import Module


# def module_detail(request, course_slug, module_id):
#     module = get_object_or_404(
#         Module,
#         id=module_id,
#         course__slug=course_slug
#     )

#     # === Render content_a ===
#     content_a = getattr(module, 'content_a', None)
#     content_a_html = None

#     if content_a and getattr(content_a, 'content', None):
#         raw_text = content_a.content
#         content_a_html = _render_markdown(raw_text)

#     # === Render content ===
#     content_obj = getattr(module, 'content', None)
#     content_html = None

#     if content_obj:
#         raw_text = getattr(content_obj, 'content', '') or getattr(content_obj, 'body', '') or str(content_obj)
#         content_html = _render_markdown(raw_text)

#     context = {
#         'module': module,
#         'content_a': content_a,
#         'content_a_html': content_a_html,
#         'content': content_obj,
#         'content_html': content_html,
#     }

#     return render(request, 'courses/module_detail.html', context)


# # === Helper: Shared Markdown + KaTeX Renderer ===
# def _render_markdown(text):
#     if not text:
#         return None

#     html = markdown.markdown(
#         text,
#         extensions=[
#             'nl2br',
#             'fenced_code',
#             'codehilite',
#             'toc',
#             'tables',
#             KatexExtension(
#                 insert_fonts_css=True,
#                 # Critical: Support \[ \], $$, $$ delimiters
#                 # delimiters=[
#                 #     {'left': '$$', 'right': '$$', 'display': True},
#                 #     {'left': '\\[', 'right': '\\]', 'display': True},
#                 #     {'left': '$', 'right': '$', 'display': False},
#                 #     {'left': '\\(', 'right': '\\)', 'display': False},
#                 # ],
#                 # throw_on_error=False,
#                 # strict=False
#             ),
#         ],
#         extension_configs={
#             'codehilite': {'linenums': False}
#         }
#     )
#     return mark_safe(html)










# # courses/views.py
# from django.shortcuts import get_object_or_404, render
# from django.utils.safestring import mark_safe
# import markdown
# from markdown_katex import KatexExtension
# from .models import Module
# from .markdown_extensions import KatexExtension


# def module_detail(request, course_slug, module_id):
#     # 1. Get the module
#     module = get_object_or_404(
#         Module,
#         id=module_id,
#         course__slug=course_slug
#     )

#     # 2. Get related content (e.g., OneToOneField)
#     content = getattr(module, 'content', None)

#     # 3. Render Markdown + KaTeX → overwrite content.content with HTML
#     if content and content.content:
#         raw_markdown = content.content  # Raw text from DB

#         # Convert Markdown + LaTeX → HTML + KaTeX
#         rendered_html = markdown.markdown(
#             raw_markdown,
#             extensions=[
#                 'nl2br',
#                 'fenced_code',
#                 'codehilite',
#                 'toc',
#                 'tables',
#                 KatexExtension(),  # ← Renders $$...$$ and $...$
#             ],
#             extension_configs={
#                 'codehilite': {'linenums': False}
#             }
#         )

#         # Overwrite the raw field with rendered HTML
#         content.content = mark_safe(rendered_html)

#         # Optional: Save to DB (only if you want rendered HTML persisted)
#         # content.save(update_fields=['content'])

#     # 4. Pass to template
#     context = {
#         'module': module,
#         'content': content,  # content.content is now rendered HTML
#     }

#     return render(request, 'courses/module_detail.html', context)





# views.py
# from django.shortcuts import render, get_object_or_404
# from django.utils.safestring import mark_safe
# from markdown import markdown
# from markdown.extensions.toc import TocExtension
# from markdown.extensions.codehilite import CodeHiliteExtension
# from markdown.extensions.tables import TableExtension
# from markdown.extensions.fenced_code import FencedCodeExtension
# from markdown.extensions.nl2br import Nl2BrExtension

# # <-- your custom Katex extension (no args) -->
# from .markdown_extensions import KatexExtension   # adjust import path

# def module_detail(request, course_slug, module_id):
#     module = get_object_or_404(
#         Module,
#         id=module_id,
#         course__slug=course_slug
#     )

#     content = getattr(module, 'content', None)
#     content_html = None

#     if content and getattr(content, 'content', None):
#         raw_text = content.content

#         # ONE markdown pass → HTML with Katex rendered
#         content_html = markdown(
#             raw_text,
#             extensions=[
#                 Nl2BrExtension(),
#                 FencedCodeExtension(),
#                 CodeHiliteExtension(linenums=False),
#                 TocExtension(),
#                 TableExtension(),
#                 KatexExtension(),          # <-- no args, as required
#             ],
#         )
#         content_html = mark_safe(content_html)

#     context = {
#         'module': module,
#         'content': content,          # still available if needed
#         'content_html': content_html,
#     }

#     return render(request, 'courses/module_detail.html', context)














def home(request):
    posts = BlogPost.objects.all().order_by('-created')
    return render(request, 'blog/home.html', {'posts': posts})


def clean_mdx(content):
    """Fix common MDX issues before rendering"""
    # Remove trailing \ before $$
    content = re.sub(r'\$\$\\', '$$', content)
    # Ensure proper line breaks between equations
    content = re.sub(r'\$\$\s*\$\$', '$$\n\n$$', content)
    # Fix extra spaces in $$
    content = re.sub(r'\$\s+\$', '$$', content)
    return content.strip()

def post_detail(request, id):
    post = get_object_or_404(BlogPost, id=id)
    
    # Clean + render
    cleaned = clean_mdx(post.content)
    content_html = markdown.markdown(
        cleaned,
        extensions=[
            'tables',
            'fenced_code',
            'nl2br',
            'toc',
            KatexExtension()
        ]
    )

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'content_html': content_html
    })



def try_content(request):
    contents = Content.objects.all()

    for c in contents:
        if c.content:
            c.content = markdown.markdown(
                c.content,
                extensions=['fenced_code', 'tables', 'nl2br']
            )

    return render(request, 'try_content.html', {'contents': contents})
   
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'slug'

class ModuleListCreateView(generics.ListCreateAPIView):
    serializer_class = ModuleSerializer

    def get_queryset(self):
        return Module.objects.filter(course_id=self.kwargs['course_id'])

    def perform_create(self, serializer):
        course = Course.objects.get(id=self.kwargs['course_id'])
        serializer.save(course=course)

class ModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ModuleSerializer

    def get_queryset(self):
        return Module.objects.filter(
            course_id=self.kwargs['course_id'],
            id=self.kwargs['pk']
        )

class ContentListCreateView(generics.ListCreateAPIView):
    serializer_class = ContentSerializer

    def get_queryset(self):
        return Content.objects.filter(module_id=self.kwargs['module_id'])

    def perform_create(self, serializer):
        module = Module.objects.get(id=self.kwargs['module_id'])
        serializer.save(module=module)

class ContentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContentSerializer

    def get_queryset(self):
        return Content.objects.filter(
            module_id=self.kwargs['module_id'],
            id=self.kwargs['pk']
        )
