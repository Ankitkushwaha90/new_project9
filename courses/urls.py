from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [

    #search bar
    path('courses/', views.courses_list, name='courses_list'),
    # or if you're using app_name
    path('', views.courses_list, name='courses_list'),

    # HTML views
    path('', views.courses_list, name='courses_list'),
    # Move try-content route before the course detail route
    path('try-content/', views.try_content, name='try_content'),
    path('<slug:slug>/', views.course_detail, name='course_detail'),
    path('<slug:course_slug>/modules/<int:module_id>/', views.module_detail, name='module_detail'),
    
    path('blog/', views.home, name='home'),  # Added trailing slash
    path('post/<int:id>/', views.post_detail, name='post_detail'),

    # API endpoints
    path('api/courses/', views.CourseListCreateView.as_view(), name='api-courses-list'),
    path('api/courses/<slug:slug>/', views.CourseDetailView.as_view(), name='api-course-detail'),
    path('api/courses/<int:course_id>/modules/', views.ModuleListCreateView.as_view(), name='api-module-list'),
    path('api/courses/<int:course_id>/modules/<int:pk>/', views.ModuleDetailView.as_view(), name='api-module-detail'),
    path('api/modules/<int:module_id>/contents/', views.ContentListCreateView.as_view(), name='api-content-list'),
    path('api/modules/<int:module_id>/contents/<int:pk>/', views.ContentDetailView.as_view(), name='api-content-detail'),
]
