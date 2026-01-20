# academics/views.py
from django.views.generic import ListView, DetailView
from .models import Course, Subject, Module


class CourseListView(ListView):
    model = Course
    template_name = "academics/courses_list.html"
    context_object_name = "courses"


class CourseDetailView(DetailView):
    model = Course
    template_name = "academics/course_details.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Pre-load subjects + their modules to avoid N+1 queries
        ctx["subjects"] = (
            self.object.subjects
            .prefetch_related("modules")
            .all()
        )
        return ctx


# class ModuleDetailView(DetailView):
#     model = Module
#     template_name = "academics/module_details.html"
#     context_object_name = "module"
#     slug_url_kwarg = "module_slug"
#     pk_url_kwarg = None

#     def get_queryset(self):
#         return Module.objects.filter(
#             subject__course__slug=self.kwargs["course_slug"]
#         )



# academics/views.py
# from django.views.generic import DetailView
# from django.shortcuts import get_object_or_404
# from .models import Module, Course
# import markdown
# from markdown.extensions import Extension
# import re


# --------------------------------------------------------------
# 1. Tiny MDX → HTML converter (Markdown + LaTeX delimiters)
# --------------------------------------------------------------
# class MDXExtension(Extension):
#     """
#     Allows $$…$$ and $…$ inside normal Markdown.
#     KaTeX will render them client-side.
#     """
#     def extendMarkdown(self, md):
#         # Nothing to pre-process – we just keep the delimiters intact
#         pass


# def render_mdx(content: str) -> str:
#     """
#     Convert MDX (Markdown + LaTeX) → safe HTML.
#     Keeps $$…$$ and $…$ untouched for KaTeX auto-render.
#     """
#     # Use markdown with extra extensions
#     html = markdown.markdown(
#         content,
#         extensions=[
#             'fenced_code',
#             'tables',
#             'toc',
#             'nl2br',
#             MDXExtension(),
#         ],
#         output_format='html5'
#     )
#     return html


# # --------------------------------------------------------------
# # 2. DetailView with MDX rendering
# # --------------------------------------------------------------
# class ModuleDetailView(DetailView):
#     model = Module
#     template_name = "academics/module_details.html"
#     context_object_name = "module"
#     slug_url_kwarg = "module_slug"
#     pk_url_kwarg = None   # we don't use PK

#     def get_queryset(self):
#         """
#         Filter by course slug → prevents URL guessing.
#         """
#         return Module.objects.filter(
#             subject__course__slug=self.kwargs["course_slug"]
#         ).select_related('subject', 'subject__course')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # --------------------------------------------------
#         # Convert raw MDX → HTML (safe for |safe)
#         # --------------------------------------------------
#         context['module_html'] = render_mdx(self.object.content)
#         return context




        

# academics/views.py
import markdown
from django.views.generic import DetailView
from .models import Module

try:
    from markdown_katex import KatexExtension
except Exception:
    class KatexExtension(markdown.extensions.Extension):
        def extendMarkdown(self, md):
            pass


class ModuleDetailView(DetailView):
    model = Module
    template_name = "academics/module_details.html"
    context_object_name = "module"
    slug_url_kwarg = "module_slug"
    pk_url_kwarg = None

    def get_queryset(self):
        return Module.objects.filter(
            subject__course__slug=self.kwargs["course_slug"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # --- 1. Get raw Markdown from Module (change 'content' if needed) ---
        raw_text = getattr(self.object, "content", "") or ""

        # --- 2. Render Markdown with your exact extensions ---
        content_html = markdown.markdown(
            raw_text,
            extensions=[
                'nl2br',
                'fenced_code',
                'codehilite',
                'toc',
                'tables',
                KatexExtension(),
            ],
            extension_configs={
                'codehilite': {
                    'linenums': False,
                    'guess_lang': False,
                }
            }
        )

        # --- 3. Front-matter with SAFE field access ---
        subject_obj = self.object.subject

        # CHANGE THIS LINE to match your Subject model's field
        subject_name = getattr(subject_obj, "title", "Unknown Subject")  # fallback

        course_name = getattr(self.object.subject.course, "name", "Unknown Course")

        front_matter = f"""---
title: {self.object.title}
course: {course_name}
subject: {subject_name}
---
"""

        # --- 4. Add delimiter (`---`) ---
        final_mdx = front_matter.rstrip() + "\n---\n" + content_html.strip()
        context["module_mdx"] = final_mdx
        return context