from django.contrib import admin

from highlights import models

# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    exclude = ("slug",)
    
admin.site.register(models.Author, AuthorAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "book_no", "slug")
    exclude = ("slug",)
    
admin.site.register(models.Book, BookAdmin)


admin.site.register(models.Highlight)


class TagAdmin(admin.ModelAdmin):
    list_display = ("tag", "slug",)
    exclude = ("slug",)

admin.site.register(models.Tag, TagAdmin)
