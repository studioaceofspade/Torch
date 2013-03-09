import sys
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from django_extensions.db.fields import (
    CreationDateTimeField,
    ModificationDateTimeField,
)

INNOVATION = 0
CREATIVITY = 1
ENTREPRENEURSHIP = 2

TAG_CHOICES = (
    (INNOVATION, 'Innovation'),
    (CREATIVITY, 'Creativity'),
    (ENTREPRENEURSHIP, 'Entrepreneurship'),
)


class IdeaManager(models.Manager):
    def get_query_set(self):
        return super(
            IdeaManager,
            self,
        ).get_query_set().annotate(
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

    class Meta:
        ordering = ['-created']


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


def order_by_popular(qs):
    """
    Return an list ordered by popularity.

    Popularity is defined by number of votes per hour.
    """
    now = datetime.now()

    def _key(idea):
        if idea.num_votes == 0:
            return sys.maxint
        diff = now - idea.created
        days = diff.days
        hours = diff.seconds / 3600
        hours += days * 24
        return hours / idea.num_votes
    return sorted(qs, key=_key)
