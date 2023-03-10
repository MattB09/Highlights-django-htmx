# Generated by Django 4.1.4 on 2022-12-31 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("highlights", "0004_author_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="slug",
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="tag",
            name="slug",
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="author",
            name="slug",
            field=models.SlugField(blank=True, null=True),
        ),
    ]
