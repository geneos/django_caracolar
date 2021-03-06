# Generated by Django 4.0.4 on 2022-06-02 12:13
from django.db import migrations

def generate_superuser(apps, schema_editor):
    """Create a new superuser """
    from django.contrib.auth import get_user_model
    from django.conf import settings

    superuser = get_user_model().objects.create_superuser(
        username=settings.DJANGO_SUPERUSER_USERNAME,
        email=settings.DJANGO_SUPERUSER_EMAIL,
        password=settings.DJANGO_SUPERUSER_PASSWORD,
    )
    superuser.save()


class Migration(migrations.Migration):

    dependencies = [
        ('param', '0003_mediopago'),
    ]

    operations = [
        migrations.RunPython(generate_superuser),
    ]
