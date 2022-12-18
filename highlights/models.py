import uuid

from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=200, db_index=True)
    user = models.ForeignKey(
        User,
        related_name="authors",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["name"]
        unique_together = ("name", "user",)

    def __str__(self):
        return self.name


class Book(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    title = models.CharField(max_length=200, db_index=True)
    book_no = models.CharField(max_length=2, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        Author, 
        related_name="books",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name="books",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["book_no"]
        unique_together = ("title", "user",)

    def __str__(self):
        return self.title


class Highlight(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    text = models.TextField(db_index=True)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="highlights",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User,
        related_name="highlights",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["text"]
        unique_together = ("text", "user",)

    def __str__(self):
        return self.text[:50] + "..."

    @classmethod
    def new(cls, text, book, user, tags=None):
        highlight = cls.objects.create(
            text=text,
            book=book,
            user=user
        )
        highlight.tags.set(tags)
        return highlight

    def update(self, text, book, tags):
        print("BOOK", book)
        print("BOOK", type(book))
        self.text = text
        self.book = book
        self.tags.set(tags)
        self.save(update_fields=["text", "book"])



class Tag(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    tag = models.CharField(max_length=255, db_index=True)
    user = models.ForeignKey(
        User,
        related_name="tags",
        on_delete=models.CASCADE
    )
    highlights = models.ManyToManyField(
        Highlight,
        related_name="tags"
    )

    class Meta:
        ordering = ["tag"]
        unique_together = ("tag", "user",)
        
    def __str__(self):
        return self.tag