import uuid

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.urls import reverse

from .utils import slugify


class BaseQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(Q(user=user))
    
    
class AuthorQuerySet(BaseQuerySet):
    pass
    
    
class Author(models.Model):
    objects = AuthorQuerySet.as_manager()
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(null=True, blank=True)
    user = models.ForeignKey(User, related_name="authors", on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]
        unique_together = (
            "name",
            "user",
        )

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('author-detail', kwargs={"slug": self.slug})


def author_pre_save(sender, instance, *args, **kwargs):
    slugify.slug_pre_save(sender, instance, "name", *args, **kwargs)


pre_save.connect(author_pre_save, sender=Author)


class BookQuerySet(BaseQuerySet):
    pass

class Book(models.Model):
    objects = BookQuerySet.as_manager()
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(null=True, blank=True)
    book_no = models.CharField(max_length=2, default=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        Author,
        related_name="books",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(User, related_name="books", on_delete=models.CASCADE)

    class Meta:
        ordering = ["book_no"]
        unique_together = (
            "title",
            "user",
        )

    def __str__(self):
        return self.title


def book_pre_save(sender, instance, *args, **kwargs):
    slugify.slug_pre_save(sender, instance, "title", *args, **kwargs)


pre_save.connect(book_pre_save, sender=Book)


class HighlightQuerySet(BaseQuerySet):
    def search(self, user, query=None):
        qs = self.for_user(user)
        if query is None or query == "":
            return qs
        lookups = Q(text__icontains=query)
        return qs.filter(lookups)
    
    def find_duplicates(self, user, text, id=None):
        return self.for_user(user).filter(Q(text=text)).exclude(id=id)


class Highlight(models.Model):
    objects = HighlightQuerySet.as_manager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField(db_index=True)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="highlights",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="highlights", on_delete=models.CASCADE)

    class Meta:
        ordering = ["text"]
        unique_together = (
            "text",
            "user",
        )

    def __str__(self):
        return self.text[:50] + "..."

    @classmethod
    def new(cls, text, book, user, tags=None):
        highlight = cls.objects.create(text=text, book=book, user=user)
        highlight.tags.set(tags)
        return highlight

    def update(self, text, book, tags):
        self.text = text
        self.book = book
        self.tags.set(tags)
        self.save(update_fields=["text", "book"])


class TagQuerySet(BaseQuerySet):
    def search(self, user, query=None):
        qs = self.for_user(user)
        if query is None or query == "":
            return qs.all()
        lookups = Q(tag__icontains=query)
        return qs.filter(lookups)
    

class Tag(models.Model):
    objects = TagQuerySet.as_manager()
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag = models.CharField(
        max_length=255, 
        db_index=True, 
        error_messages={"unique": "This tag already exists."},
    )
    slug = models.SlugField(null=True, blank=True)
    user = models.ForeignKey(User, related_name="tags", on_delete=models.CASCADE)
    highlights = models.ManyToManyField(Highlight, related_name="tags", blank=True,)

    class Meta:
        ordering = ["tag"]
        unique_together = (
            "tag",
            "user",
        )

    def __str__(self):
        return self.tag
    
    @classmethod
    def new(cls, tag, user):
        tag = cls.objects.create(tag=tag, user=user)
        return tag
        
    def update(self, tag):
        self.tag = tag
        self.save(update_fields=["tag"])


def tag_pre_save(sender, instance, *args, **kwargs):
    slugify.slug_pre_save(sender, instance, "tag", *args, **kwargs)


pre_save.connect(tag_pre_save, sender=Tag)
