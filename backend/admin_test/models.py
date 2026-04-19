from django.db import models
from django.utils.text import slugify


class Author(models.Model):
    """Blog author model."""

    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Category(models.Model):
    """Blog post category."""

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Blog post tag."""

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    """Blog post model."""

    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    excerpt = models.TextField(blank=True, default="")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Many-to-many relationships
    categories = models.ManyToManyField(Category, related_name="posts", blank=True)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    """Blog post comment."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author.name} on {self.post.title}"


class EventSchedule(models.Model):
    """Event schedule model with date, time, and choice fields."""

    EVENT_TYPE_CHOICES = [
        ("conference", "Conference"),
        ("workshop", "Workshop"),
        ("webinar", "Webinar"),
        ("meeting", "Meeting"),
        ("training", "Training"),
    ]

    title = models.CharField(max_length=300)
    event_type = models.CharField(
        max_length=20, choices=EVENT_TYPE_CHOICES, default="meeting"
    )
    event_date = models.DateField()
    event_time = models.TimeField()
    location = models.CharField(max_length=300)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Event Schedule"
        verbose_name_plural = "Event Schedules"
        ordering = ["event_date", "event_time"]

    def __str__(self):
        return f"{self.title} - {self.event_date} at {self.event_time}"


class Poll(models.Model):
    """Poll model with radio button choice field."""

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("closed", "Closed"),
        ("archived", "Archived"),
    ]

    title = models.CharField(max_length=300)
    question = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    allow_multiple_votes = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Poll"
        verbose_name_plural = "Polls"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class EventLog(models.Model):
    """Event log model with date and time fields."""

    LOG_LEVEL_CHOICES = [
        ("debug", "Debug"),
        ("info", "Info"),
        ("warning", "Warning"),
        ("error", "Error"),
        ("critical", "Critical"),
    ]

    event_name = models.CharField(max_length=300)
    log_level = models.CharField(
        max_length=20, choices=LOG_LEVEL_CHOICES, default="info"
    )
    log_date = models.DateField()
    log_time = models.TimeField()
    message = models.TextField()
    user = models.CharField(max_length=200, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Event Log"
        verbose_name_plural = "Event Logs"
        ordering = ["-log_date", "-log_time"]

    def __str__(self):
        return f"{self.event_name} - {self.log_date} {self.log_time}"
