from django.urls import path
from . import views

app_name = 'blog'   # ✅ This defines the namespace

urlpatterns = [
    path('', views.home, name='home'),  # Added trailing slash
    path('post/<int:id>/', views.post_detail, name='post_detail'),
]