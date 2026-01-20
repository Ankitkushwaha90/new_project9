# academics/urls.py
from django.urls import path
from . import views

app_name = "academics"

urlpatterns = [
    # 1. All courses
    path("", views.CourseListView.as_view(), name="course_list"),

    # 2. Course → shows its subjects + list of modules under each subject
    path("<slug:slug>/", views.CourseDetailView.as_view(), name="course_detail"),

    # 3. Specific module inside a course
    path(
        "<slug:course_slug>/module/<slug:module_slug>/",
        views.ModuleDetailView.as_view(),
        name="module_detail",
    ),
]