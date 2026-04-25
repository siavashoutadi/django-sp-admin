import factory
from django.utils.text import slugify
from faker import Faker

from admin_test.models import (
    Author,
    BooleanTestModel,
    Category,
    ChoiceTestModel,
    Comment,
    DateTimeComprehensiveModel,
    EventLog,
    EventSchedule,
    IdentifierModel,
    NumberTestModel,
    Poll,
    Post,
    RelationshipTestModel,
    Tag,
    TextFieldsModel,
    URLEmailFileModel,
)

# --- New Model Factories ---


class NumberTestModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NumberTestModel

    title = factory.Faker("sentence", nb_words=2)
    integer_field = factory.Faker("random_int", min=-100, max=100)
    positive_integer = factory.Faker("random_int", min=0, max=100)
    big_integer = factory.Faker("random_int", min=0, max=999999)
    small_integer = factory.Faker("random_int", min=-32768, max=32767)
    decimal_field = factory.Faker(
        "pydecimal", left_digits=5, right_digits=2, positive=True
    )
    float_field = factory.Faker("pyfloat", left_digits=3, right_digits=2, positive=True)


class BooleanTestModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BooleanTestModel

    title = factory.Faker("sentence", nb_words=2)
    is_active = factory.Faker("boolean")
    is_published = factory.Faker("boolean")
    is_verified = factory.Faker("boolean")
    requires_approval = factory.Faker("boolean")
    is_archived = factory.Faker("boolean")


class URLEmailFileModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = URLEmailFileModel

    title = factory.Faker("sentence", nb_words=2)
    email = factory.Faker("email")
    website_url = factory.Faker("url")
    backup_email = factory.Faker("email")
    document = factory.django.FileField(filename="test.pdf")
    image = factory.django.ImageField(color="blue")
    thumbnail = factory.django.ImageField(color="red")


class ChoiceTestModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChoiceTestModel

    title = factory.Faker("sentence", nb_words=2)
    priority = factory.Faker(
        "random_element", elements=["low", "medium", "high", "critical"]
    )
    status = factory.Faker(
        "random_element", elements=["pending", "in_progress", "completed", "cancelled"]
    )
    difficulty = factory.Faker("random_element", elements=["easy", "medium", "hard"])


class DateTimeComprehensiveModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DateTimeComprehensiveModel

    title = factory.Faker("sentence", nb_words=2)
    date_field = factory.Faker("date_object")
    time_field = factory.Faker("time_object")
    datetime_field = factory.Faker("date_time_this_year")
    auto_now_field = factory.Faker("date_time_this_year")
    auto_now_add_field = factory.Faker("date_time_this_year")
    optional_date = factory.Faker("date_object")
    optional_time = factory.Faker("time_object")
    optional_datetime = factory.Faker("date_time_this_year")
    duration_field = factory.Faker("time_delta")


class IdentifierModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IdentifierModel

    title = factory.Faker("sentence", nb_words=2)
    uuid_field = factory.Faker("uuid4")
    slug_field = factory.LazyAttribute(lambda obj: slugify(obj.title))
    code = factory.Faker("bothify", text="???-#####")
    identifier = factory.Faker("ean", length=13)


class TextFieldsModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TextFieldsModel

    title = factory.Faker("sentence", nb_words=2)
    description = factory.Faker("paragraph")
    short_text = factory.Faker("word")
    medium_text = factory.Faker("sentence", nb_words=10)
    long_text = factory.Faker("paragraph", nb_sentences=5)
    richtext_content = factory.Faker("text", max_nb_chars=200)


class RelationshipTestModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RelationshipTestModel

    title = factory.Faker("sentence", nb_words=2)
    author = factory.LazyFunction(lambda: Author.objects.first() or AuthorFactory())


fake = Faker()


class AuthorFactory(factory.django.DjangoModelFactory):
    """Factory for creating Author objects."""

    class Meta:
        model = Author

    name = factory.Faker("name")
    email = factory.Faker("email")
    bio = factory.Faker("paragraph", nb_sentences=3)


class CategoryFactory(factory.django.DjangoModelFactory):
    """Factory for creating Category objects."""

    class Meta:
        model = Category

    name = factory.Faker("words", nb=2, ext_word_list=None)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name)[:50])
    description = factory.Faker("paragraph", nb_sentences=2)


class TagFactory(factory.django.DjangoModelFactory):
    """Factory for creating Tag objects."""

    class Meta:
        model = Tag

    name = factory.Faker("word")
    slug = factory.LazyAttribute(lambda obj: obj.name.replace(" ", "-").lower())


class PostFactory(factory.django.DjangoModelFactory):
    """Factory for creating Post objects."""

    class Meta:
        model = Post

    title = factory.Faker("sentence", nb_words=8)
    slug = factory.LazyAttribute(lambda obj: obj.title.lower().replace(" ", "-")[:50])
    author = factory.SubFactory(AuthorFactory)
    content = factory.Faker("paragraph", nb_sentences=10)
    excerpt = factory.Faker("paragraph", nb_sentences=3)
    is_published = factory.Faker("boolean", chance_of_getting_true=90)
    created_at = factory.Faker("date_time_this_year", tzinfo=None)
    updated_at = factory.Faker("date_time_this_year", tzinfo=None)

    @factory.post_generation
    def categories(obj, create, extracted, **kwargs):
        """Add random categories to the post."""
        if not create:
            return
        if extracted:
            for category in extracted:
                obj.categories.add(category)
        else:
            # Add 1-3 random categories
            categories = Category.objects.order_by("?")[: fake.random_int(1, 3)]
            for category in categories:
                obj.categories.add(category)

    @factory.post_generation
    def tags(obj, create, extracted, **kwargs):
        """Add random tags to the post."""
        if not create:
            return
        if extracted:
            for tag in extracted:
                obj.tags.add(tag)
        else:
            # Add 3-7 random tags
            tags = Tag.objects.order_by("?")[: fake.random_int(3, 7)]
            for tag in tags:
                obj.tags.add(tag)


class CommentFactory(factory.django.DjangoModelFactory):
    """Factory for creating Comment objects."""

    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(AuthorFactory)
    content = factory.Faker("paragraph", nb_sentences=4)
    is_approved = factory.Faker("boolean", chance_of_getting_true=80)
    created_at = factory.Faker("date_time_this_year", tzinfo=None)


class EventScheduleFactory(factory.django.DjangoModelFactory):
    """Factory for creating EventSchedule objects."""

    class Meta:
        model = EventSchedule

    title = factory.Faker("sentence", nb_words=4)
    event_type = factory.Faker(
        "random_element",
        elements=["conference", "workshop", "webinar", "meeting", "training"],
    )
    event_date = factory.Faker("date_object")
    event_time = factory.Faker("time_object")
    location = factory.Faker("city")
    description = factory.Faker("paragraph", nb_sentences=3)
    created_at = factory.Faker("date_time_this_year", tzinfo=None)
    updated_at = factory.Faker("date_time_this_year", tzinfo=None)


class PollFactory(factory.django.DjangoModelFactory):
    """Factory for creating Poll objects."""

    class Meta:
        model = Poll

    title = factory.Faker("sentence", nb_words=5)
    question = factory.Faker("sentence", nb_words=10)
    status = factory.Faker(
        "random_element", elements=["draft", "active", "closed", "archived"]
    )
    allow_multiple_votes = factory.Faker("boolean", chance_of_getting_true=30)
    created_at = factory.Faker("date_time_this_year", tzinfo=None)
    updated_at = factory.Faker("date_time_this_year", tzinfo=None)


class EventLogFactory(factory.django.DjangoModelFactory):
    """Factory for creating EventLog objects."""

    class Meta:
        model = EventLog

    event_name = factory.Faker("sentence", nb_words=3)
    log_level = factory.Faker(
        "random_element", elements=["debug", "info", "warning", "error", "critical"]
    )
    log_date = factory.Faker("date_object")
    log_time = factory.Faker("time_object")
    message = factory.Faker("paragraph", nb_sentences=2)
    user = factory.Faker("user_name")
    created_at = factory.Faker("date_time_this_year", tzinfo=None)
