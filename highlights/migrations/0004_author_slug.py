# Generated by Django 4.1.4 on 2022-12-31 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("highlights", "0003_alter_author_user_alter_book_user_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="slug",
            field=models.SlugField(null=True),
        ),
    ]
