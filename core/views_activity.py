from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
import json

from .models import UserActivity

@login_required
@require_http_methods(["POST"])
def mark_activity_read(request, activity_id):
    try:
        activity = UserActivity.objects.get(id=activity_id, user=request.user)
        activity.mark_as_read()
        return JsonResponse({'status': 'success'})
    except UserActivity.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Activity not found'}, status=404)

@login_required
@require_http_methods(["POST"])
def mark_all_read(request):
    UserActivity.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})

@login_required
def get_activities(request):
    # Get filter parameters
    filter_type = request.GET.get('type', 'all')
    days = int(request.GET.get('days', 7))
    
    # Base queryset
    activities = UserActivity.objects.filter(user=request.user)
    
    # Apply date filter
    if days > 0:
        date_threshold = timezone.now() - timedelta(days=days)
        activities = activities.filter(timestamp__gte=date_threshold)
    
    # Apply type filter
    if filter_type != 'all':
        activities = activities.filter(activity_type=filter_type)
    
    # Order and limit
    activities = activities.order_by('-timestamp')[:50]
    
    # Prepare response data
    data = [{
        'id': activity.id,
        'type': activity.activity_type,
        'title': activity.page_title,
        'timestamp': activity.timestamp.isoformat(),
        'is_read': activity.is_read,
        'is_important': activity.is_important,
        'progress': activity.progress,
        'metadata': activity.metadata,
        'priority': activity.priority,
        'priority_class': activity.priority_class,
        'icon': activity.icon,
    } for activity in activities]
    
    return JsonResponse({'activities': data})
