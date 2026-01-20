from .models import UserActivity

def user_activity(request):
    """Adds user's recent activity to the template context"""
    if not request.user.is_authenticated:
        return {}
        
    recent_activities = UserActivity.objects.filter(
        user=request.user
    ).select_related('user').order_by('-timestamp')[:5]
    
    return {
        'recent_activities': recent_activities
    }
