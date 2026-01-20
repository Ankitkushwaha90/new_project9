from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

urlpatterns = [


    path('academics/', include('academics.urls')),

    # path('admin/', admin.site.urls),
    # path('', include('academics.urls', namespace='academics')),

    
    path("admin/", admin.site.urls),

    path('', include('core.urls')),

    path('users/', include('users.urls')),

    path('courses/', include('courses.urls')),

    path('blog/', include('blog.urls')),

    path('forum/', include('forum.urls')),

    path('resources/', include('resources.urls')),

    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    
    path('accounts/logout/', LogoutView.as_view(template_name='registration/logged_out.html', next_page=reverse_lazy('home')), name='logout'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('accounts/password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add browser reload URL only in development
if settings.DEBUG:
    urlpatterns += [
        path('__reload__/', include('django_browser_reload.urls')),
    ]
