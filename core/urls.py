from django.urls import path
from . import views
from .views_activity import mark_activity_read, mark_all_read, get_activities

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('api-login/', views.api_login, name='api_login'),
    path('recommendations/', views.recommendations, name='recommendations'),

    path('freelance/', views.freelance_listings, name='freelance_listings'),

    path('lab-setup/', views.lab_setup_view, name='lab_setup'),
    path('lab-setup/tools/', views.lab_tools_library, name='lab_tools'),
    path('lab-setup/wizard/', views.lab_wizard, name='lab_wizard'),
    
    # Activity API endpoints
    path('api/activities/mark-read/<int:activity_id>/', mark_activity_read, name='mark_activity_read'),
    path('api/activities/mark-all-read/', mark_all_read, name='mark_all_read'),
    path('api/activities/', get_activities, name='get_activities'),
]