import uuid

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
    log_datetime = models.DateTimeField(blank=True, null=True)  # DateTimeField
    scheduled_date = models.DateField(blank=True, null=True)  # Another DateField
    scheduled_time = models.TimeField(blank=True, null=True)  # Another TimeField
    start_datetime = models.DateTimeField(blank=True, null=True)  # Start datetime
    end_datetime = models.DateTimeField(blank=True, null=True)  # End datetime
    duration = models.DurationField(blank=True, null=True)  # Duration field
    message = models.TextField()
    user = models.CharField(max_length=200, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Another auto-updating datetime

    class Meta:
        verbose_name = "Event Log"
        verbose_name_plural = "Event Logs"
        ordering = ["-log_date", "-log_time"]

    def __str__(self):
        return f"{self.event_name} - {self.log_date} {self.log_time}"


class NumberTestModel(models.Model):
    """Model for testing numeric field widgets."""

    title = models.CharField(max_length=200)
    integer_field = models.IntegerField(default=0)
    positive_integer = models.PositiveIntegerField(default=1)
    big_integer = models.BigIntegerField(default=0)
    small_integer = models.SmallIntegerField(default=0)
    decimal_field = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    float_field = models.FloatField(default=0.0)

    class Meta:
        verbose_name = "Number Test"
        verbose_name_plural = "Number Tests"
        ordering = ["-id"]

    def __str__(self):
        return self.title


class BooleanTestModel(models.Model):
    """Model for testing boolean field widgets."""

    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    is_verified = models.BooleanField(null=True, blank=True)
    requires_approval = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Boolean Test"
        verbose_name_plural = "Boolean Tests"
        ordering = ["-id"]

    def __str__(self):
        return self.title


class URLEmailFileModel(models.Model):
    """Model for testing URL, email, and file field widgets."""

    title = models.CharField(max_length=200)
    email = models.EmailField()
    website_url = models.URLField(blank=True, default="")
    backup_email = models.EmailField(blank=True, default="")
    document = models.FileField(upload_to="documents/", blank=True, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)

    class Meta:
        verbose_name = "URL Email File Test"
        verbose_name_plural = "URL Email File Tests"
        ordering = ["-id"]

    def __str__(self):
        return self.title


class ChoiceTestModel(models.Model):
    """Model for testing various choice and selection widgets."""

    PRIORITY_CHOICES = [
        ("low", "Low Priority"),
        ("medium", "Medium Priority"),
        ("high", "High Priority"),
        ("critical", "Critical Priority"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    title = models.CharField(max_length=200)
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default="medium"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    difficulty = models.CharField(
        max_length=20,
        choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")],
        default="medium",
    )

    class Meta:
        verbose_name = "Choice Test"
        verbose_name_plural = "Choice Tests"
        ordering = ["-id"]

    def __str__(self):
        return self.title


class DateTimeComprehensiveModel(models.Model):
    """Comprehensive model for testing all date and time field types."""

    title = models.CharField(max_length=200)
    date_field = models.DateField()
    time_field = models.TimeField()
    datetime_field = models.DateTimeField()
    auto_now_field = models.DateTimeField(auto_now=True)
    auto_now_add_field = models.DateTimeField(auto_now_add=True)
    optional_date = models.DateField(blank=True, null=True)
    optional_time = models.TimeField(blank=True, null=True)
    optional_datetime = models.DateTimeField(blank=True, null=True)
    duration_field = models.DurationField(blank=True, null=True)

    class Meta:
        verbose_name = "DateTime Comprehensive Test"
        verbose_name_plural = "DateTime Comprehensive Tests"
        ordering = ["-id"]

    def __str__(self):
        return self.title


class IdentifierModel(models.Model):
    """Model for testing UUID, slug, and other identifier fields."""

    title = models.CharField(max_length=200)
    uuid_field = models.UUIDField(default=uuid.uuid4, editable=False)
    slug_field = models.SlugField(unique=True)
    code = models.CharField(max_length=50, unique=True)
    identifier = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Identifier Test"
        verbose_name_plural = "Identifier Tests"
        ordering = ["-id"]

    def __str__(self):
        return self.title


class TextFieldsModel(models.Model):
    """Model for testing various text field types."""

    title = models.CharField(max_length=200)
    description = models.TextField()
    short_text = models.CharField(max_length=50)
    medium_text = models.CharField(max_length=500)
    long_text = models.TextField(blank=True, default="")
    richtext_content = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "Text Fields Test"
        verbose_name_plural = "Text Fields Tests"
        ordering = ["-id"]

    def __str__(self):
        return self.title


class RelationshipTestModel(models.Model):
    """Model for testing relationship field types."""

    title = models.CharField(max_length=200)
    # ForeignKey to Author from existing model
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="relationship_tests"
    )
    # ManyToMany to Category from existing model
    categories = models.ManyToManyField(
        Category, related_name="relationship_tests", blank=True
    )
    # ManyToMany to Tag from existing model
    tags = models.ManyToManyField(Tag, related_name="relationship_tests", blank=True)

    class Meta:
        verbose_name = "Relationship Test"
        verbose_name_plural = "Relationship Tests"
        ordering = ["-id"]

    def __str__(self):
        return self.title
