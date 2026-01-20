from django.db import models
from django.utils import timezone

class Contact(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(default=timezone.now)
    is_resolved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.subject} - {self.email}"
    
    class Meta:
        ordering = ['-created_at']

class UserActivity(models.Model):
    """
    Tracks user interactions with the platform
    """
    ACTIVITY_TYPES = [
        ('page_view', 'Page View'),
        ('course_view', 'Course View'),
        ('course_progress', 'Course Progress'),
        ('resource_download', 'Resource Downloaded'),
        ('forum_post', 'Forum Post'),
        ('forum_reply', 'Forum Reply'),
        ('achievement', 'Achievement Unlocked'),
        ('search', 'Search'),
        ('enroll', 'Course Enrollment'),
        ('complete', 'Course Completion'),
        ('certificate', 'Certificate Earned'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    page_url = models.URLField()
    page_title = models.CharField(max_length=200)
    metadata = models.JSONField(default=dict, blank=True)  # Store additional data like course_id, search_query, etc.
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium')
    is_important = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    related_content_type = models.ForeignKey(
        'contenttypes.ContentType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # For tracking progress if applicable
    progress = models.PositiveSmallIntegerField(null=True, blank=True)  # 0-100%

    class Meta:
        verbose_name_plural = 'User Activities'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'activity_type']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()} - {self.page_title}"
        
    @property
    def priority_class(self):
        return {
            'low': 'bg-blue-100 text-blue-800',
            'medium': 'bg-yellow-100 text-yellow-800',
            'high': 'bg-red-100 text-red-800',
        }.get(self.priority, 'bg-gray-100 text-gray-800')
        
    @property
    def icon(self):
        icons = {
            'course_view': 'eye',
            'course_progress': 'trending-up',
            'resource_download': 'download',
            'forum_post': 'message-square',
            'forum_reply': 'message-circle',
            'achievement': 'award',
            'search': 'search',
            'enroll': 'user-plus',
            'complete': 'check-circle',
            'certificate': 'file-text',
        }
        return icons.get(self.activity_type, 'activity')
        
    def mark_as_read(self):
        self.is_read = True
        self.save(update_fields=['is_read'])

    @classmethod
    def record_activity(cls, request, activity_type, **kwargs):
        """
        Helper method to record user activity
        """
        if not request.user.is_authenticated:
            return None
            
        return cls.objects.create(
            user=request.user,
            activity_type=activity_type,
            page_url=request.build_absolute_uri(),
            page_title=kwargs.get('page_title', ''),
            metadata=kwargs.get('metadata', {}),
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            referrer=request.META.get('HTTP_REFERER', '')
        )
