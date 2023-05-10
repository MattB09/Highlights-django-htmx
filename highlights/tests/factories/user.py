from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(**overwrites):
    return User.objects.create(
        username="testuser",
        password="abc123",
        **overwrites,
    )