import random

from django.utils.text import slugify


def slugify_instance(instance, field, new_slug=None):
    if new_slug:
        slug = new_slug
    else:
        slug = slugify(getattr(instance, field))

    Klass = instance.__class__
    qs = Klass.objects.filter(user=instance.user, slug=slug).exclude(id=instance.id)
    if qs.exists():
        rand_int = random.randint(1, 1000)
        rand_str = str(rand_int).zfill(4)
        slug = f"{slug}-{rand_str}"
        return slugify_instance(instance, field, new_slug=slug)
    instance.slug = slug
    return instance


def slug_pre_save(sender, instance, field, *args, **kwargs):
    if instance.slug is None:
        slugify_instance(instance, field)
