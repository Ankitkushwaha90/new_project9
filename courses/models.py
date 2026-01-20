from django.db import models
from django.utils.text import slugify

class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        if self.course:
            return f"{self.course.title} - {self.title}"
        return self.title

# models.py
class Content(models.Model):
    LANGUAGE_CHOICES = [
        ('python', 'Python'), ('javascript', 'JavaScript'), ('java', 'Java'),
        ('c', 'C'), ('cpp', 'C++'), ('csharp', 'C#'), ('go', 'Go'),
        ('ruby', 'Ruby'), ('php', 'PHP'), ('swift', 'Swift'), ('kotlin', 'Kotlin'),
        ('typescript', 'TypeScript'), ('html', 'HTML'), ('css', 'CSS'),
        ('sql', 'SQL'), ('bash', 'Bash/Shell'), ('json', 'JSON'),
        ('yaml', 'YAML'), ('markdown', 'Markdown'), ('text', 'Plain Text'),
    ]

    module = models.OneToOneField(
        Module,
        related_name='content',  # → module.content gives the Content
        on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField(default=0, db_index=True)

    main_title = models.CharField(max_length=200)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    content = models.TextField()  # Markdown
    code = models.TextField(blank=True, null=True)
    code_language = models.CharField(
        max_length=20,
        choices=LANGUAGE_CHOICES,
        default='python',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Content'
        verbose_name_plural = 'Contents'
        # Use manual order, not creation time
        ordering = ['order']

    def __str__(self):
        return f"{self.module}: {self.main_title}"