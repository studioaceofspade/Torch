from django.db import models
from django.contrib.auth.models import User

from django_extensions.db.fields import (
    CreationDateTimeField,
)

from torch.idea.models import Idea


class Vote(models.Model):
    voter = models.ForeignKey(User, related_name='votes')
    idea = models.ForeignKey(Idea, related_name='votes')

    created = CreationDateTimeField(null=True)


def create_vote(user, idea):
    return Vote.objects.create(
        voter=user,
        idea=idea,
    )


def get_votes_for_idea(idea):
    return Vote.objects.filter(idea=idea)
