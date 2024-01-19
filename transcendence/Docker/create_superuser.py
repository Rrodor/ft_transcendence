import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@42.fr")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "trans")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
