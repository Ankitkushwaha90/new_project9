from django.shortcuts import render, get_object_or_404
from .models import BlogPost

import markdown

def home(request):
    posts = BlogPost.objects.all().order_by('-created')
    return render(request, 'home.html', {'posts': posts})

# def post_detail(request, id):
#     post = get_object_or_404(BlogPost, id=id)

#     content_html = markdown.markdown(
#         post.content,
#         extensions=[
#             'fenced_code',    # ``` code blocks
#             'tables',         # markdown tables
#             'nl2br'           # line break auto
#         ]
#     )

#     return render(request, 'post_detail.html', {
#         'post': post,
#         'content_html': content_html
#     })




# views.py

# def post_detail(request, id):
#     post = get_object_or_404(BlogPost, id=id)
#     content_html = markdown.markdown(
#         post.content,
#         extensions=[
#             'tables',
#             'fenced_code',
#             'nl2br',
#             KatexExtension()
#         ]
#     )
#     return render(request, 'blog/post_detail.html', {
#         'post': post,
#         'content_html': content_html
#     })


# blog/views.py
from django.shortcuts import render, get_object_or_404
import markdown
from markdown_katex.extension import KatexExtension
import re

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



