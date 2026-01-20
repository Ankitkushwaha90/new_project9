# academics/models.py
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Course(models.Model):
    """Top level – e.g. “B.Sc. Physics”, “M.Sc. Chemistry”"""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    overview = models.TextField(
        blank=True,
        help_text="Short description of the course (Markdown + LaTeX allowed)."
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("academics:course_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


# class Subject(models.Model):
#     """Middle level – Physics, Chemistry, Mathematics inside a course"""
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subjects")
#     title = models.CharField(max_length=200)
#     slug = models.SlugField(max_length=220, blank=True)

#     class Meta:
#         unique_together = ("course", "title")
#         ordering = ["title"]

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.title)
#         super().save(*args, **kwargs)

#     def get_absolute_url(self):
#         return reverse(
#             "academics:course_detail",
#             kwargs={"slug": self.course.slug}
#         ) + f"#subject-{self.pk}"

#     def __str__(self):
#         return f"{self.course} – {self.title}"

class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subjects")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, blank=True)
    
    # Add this field for manual/custom ordering
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        unique_together = ("course", "title")
        ordering = ["order", "title"]   # Primary: manual order, fallback: title
        # If you want strict manual order within a course only:
        # ordering = ["course", "order", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "academics:course_detail",
            kwargs={"slug": self.course.slug}
        ) + f"#subject-{self.pk}"

    def __str__(self):
        return f"{self.course} – {self.title}"


# class Module(models.Model):
#     """Bottom level – individual topic with MDX formulas"""
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="modules")
#     title = models.CharField(max_length=250)
#     slug = models.SlugField(max_length=270, blank=True)
#     content = models.TextField(
#         help_text="Write in Markdown + LaTeX: $$…$$ (block) or $…$ (inline)"
#     )
#     thumbnail = models.ImageField(upload_to="module_thumbs/", blank=True, null=True)

#     # content = models.TextField(
#     #     help_text="Raw MDX: Use $$…$$ for block math, $…$ for inline. NO HTML."
#     # )

#     class Meta:
#         unique_together = ("subject", "title")
#         ordering = ["title"]

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.title)
#         super().save(*args, **kwargs)

#     def get_absolute_url(self):
#         return reverse(
#             "academics:module_detail",
#             kwargs={"course_slug": self.subject.course.slug, "module_slug": self.slug},
#         )

#     def __str__(self):
#         return f"{self.subject} → {self.title}"

class Module(models.Model):
    """Bottom level – individual topic with MDX formulas"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=270, blank=True)
    content = models.TextField(
        help_text="Write in Markdown + LaTeX: $$…$$ (block) or $…$ (inline)"
    )
    thumbnail = models.ImageField(upload_to="module_thumbs/", blank=True, null=True)

    # NEW: Explicit ordering field
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        unique_together = ("subject", "title")
        # Order first by manual 'order', then by title as fallback
        ordering = ["order", "title"]
        # Or if you want strict per-subject ordering:
        # ordering = ["subject", "order", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "academics:module_detail",
            kwargs={
                "course_slug": self.subject.course.slug,
                "module_slug": self.slug
            },
        )

    def __str__(self):
        return f"{self.subject} → {self.title}"