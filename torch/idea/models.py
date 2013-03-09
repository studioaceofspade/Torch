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

TAG_CHOICES = (
    (CREATIVITY, 'Creativity'),
    (DOWNTOWN_AREAS, 'Downtown Areas'),
    (ENTREPRENEURSHIP, 'Entrepreneurship'),
    (INNOVATION, 'Innovation'),
)


class IdeaManager(models.Manager):
    def get_queryset(self):
        return super(
            IdeaManager,
            self,
        ).get_queryset().aggregate(
            num_votes=models.Count('votes'),
        )


class Idea(models.Model):
    """
    ``title`` is the viewable name of the idea in question.

    ``description`` is a short description of the idea.

    ``author`` is the user that created a given instance of Idea.

    ``tag`` is one of ``TAG_CHOICES``. Ideally ``TAG_CHOICES`` is in
    alphabetical order to make sorting easier.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()

    author = models.ForeignKey(User, related_name='ideas')
    tag = models.SmallIntegerField(choices=TAG_CHOICES, db_index=True)

    created = CreationDateTimeField(null=True)
    modified = ModificationDateTimeField(null=True)

    objects = IdeaManager()


def create_idea(user, title, description, tag):
    """
    This is a helper function to create an Idea object. I am not sure if it is
    actually needed, but for now lets keep it.
    """
    return Idea.objects.create(
        author=user,
        title=title,
        description=description,
        tag=tag,
    )
