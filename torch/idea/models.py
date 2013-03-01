from django.db import models
from django.contrib.auth.models import User

from django_extensions.db.fields import (
    CreationDateTimeField,
    ModificationDateTimeField,
)


class Idea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    author = models.ForeignKey(User, related_name='ideas')

    created = CreationDateTimeField(null=True)
    modified = ModificationDateTimeField(null=True)


def create_idea(user, title, description):
    return Idea.objects.create(
        author=user,
        title=title,
        description=description,
    )
