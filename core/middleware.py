from django.utils import timezone
from .models import UserActivity

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before the view is called
        if request.user.is_authenticated and not self._should_skip_tracking(request):
            self._track_activity(request)

        response = self.get_response(request)
        return response

    def _should_skip_tracking(self, request):
        """Skip tracking for certain paths or AJAX requests"""
        skip_paths = ['/static/', '/media/', '/admin/']
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        return (
            request.path.startswith(tuple(skip_paths)) or
            is_ajax or
            request.content_type != 'text/html' or
            request.method != 'GET'
        )

    def _track_activity(self, request):
        """Record the page view activity"""
        UserActivity.record_activity(
            request=request,
            activity_type='page_view',
            page_title=self._get_page_title(request),
            metadata={
                'method': request.method,
                'path': request.path,
                'query_params': dict(request.GET),
            }
        )

    def _get_page_title(self, request):
        """Extract page title from the view's context if available"""
        # This will be set by a view if needed
        return request.META.get('HTTP_REFERER', '') or request.path
