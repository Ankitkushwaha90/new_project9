from django.db import models

class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='resources/', blank=True)
    download_url = models.URLField(blank=True)
    category = models.CharField(max_length=100, choices=[
        ('cheatsheet', 'Cheat Sheet'),
        ('template', 'Code Template'),
        ('guide', 'Guide/PDF'),
        ('external', 'External Link'),
    ])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
