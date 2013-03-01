from django.db import models, IntegrityError
from django.contrib.auth.models import User, AnonymousUser

from django_extensions.db.fields import (
    CreationDateTimeField,
)

from torch.idea.models import Idea


class Vote(models.Model):
    voter = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='votes',
    )
    idea = models.ForeignKey(Idea, related_name='votes')
    ip = models.CharField(max_length=15, blank=True, null=True)

    created = CreationDateTimeField(null=True)


def create_vote(user, idea, ip=None):
    vote_kwargs = {
        'idea': idea,
    }
    if isinstance(user, AnonymousUser):
        if ip is None:
            raise IntegrityError('Must pass in ip address for anon users.')
        vote_kwargs['voter'] = None
        vote_kwargs['ip'] = ip
    else:
        vote_kwargs['voter'] = user
    return Vote.objects.create(**vote_kwargs)


def get_votes_for_idea(idea):
    return Vote.objects.filter(idea=idea)
