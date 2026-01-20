from django.db import models
from django.contrib.auth.models import User

class ForumPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100, choices=[
        ('general', 'General Discussion'),
        ('databases', 'Databases'),
        ('fullstack', 'Full Stack Web Development'),
        ('cloud', 'Cloud Computing'),
        ('datascience', 'Data Science'),
        ('mlai', 'Machine Learning/AI'),
        ('iot', 'IoT Devices'),
        ('cybersecurity', 'Cybersecurity'),
        ('help', 'Help & Support'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Reply(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reply by {self.user.username} on {self.post.title}"
