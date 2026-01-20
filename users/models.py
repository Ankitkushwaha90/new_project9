from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    BRANCH_CHOICES = [
        ('cse', 'Computer Science'),
        ('it', 'Information Technology'),
        ('ece', 'Electronics & Communication'),
        ('eee', 'Electrical & Electronics'),
        ('mech', 'Mechanical'),
        ('civil', 'Civil'),
        ('ai_ml', 'AI & Machine Learning'),
        ('cyber_security', 'Cyber Security'),
        ('data_science', 'Data Science'),
        ('other', 'Other')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=15, blank=True)
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES, blank=True)
    github = models.URLField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    additional_info = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
