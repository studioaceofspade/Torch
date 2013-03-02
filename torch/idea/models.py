from django.db import models
from django.contrib.auth.models import User

from django_extensions.db.fields import (
    CreationDateTimeField,
    ModificationDateTimeField,
)

CREATIVITY = 0
DOWNTOWN_AREAS = 1
ENTREPRENEURSHIP = 2
INNOVATION = 3

STATUS_CHOICES = (
    (CREATIVITY, 'Creativity'),
    (DOWNTOWN_AREAS, 'Downtown Areas'),
    (ENTREPRENEURSHIP, 'Entrepreneurship'),
    (INNOVATION, 'Innovation'),
)


class Idea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    author = models.ForeignKey(User, related_name='ideas')
    tag = models.SmallIntegerField(choices=STATUS_CHOICES, db_index=True)

    created = CreationDateTimeField(null=True)
    modified = ModificationDateTimeField(null=True)


def create_idea(user, title, description, tag):
    return Idea.objects.create(
        author=user,
        title=title,
        description=description,
        tag=tag,
    )
