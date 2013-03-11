from django.db import models, IntegrityError
from django.contrib.auth.models import User, AnonymousUser

from django_extensions.db.fields import (
    CreationDateTimeField,
)

from torch.idea.models import Idea


class Vote(models.Model):
    """
    ``voter`` is the user that cast the vote. If it is blank/null then the
    ``ip`` must be set. (This means that an AnonymousUser cast a vote.

    ``idea`` is the idea that ``voter`` voted on. This field cannot be
    blank/null.

    ``ip`` is only used if the vote was cast by an AnonymousUser. In theory the
    ``ip`` field should be unique.

    ``created`` is the date the instance was created.
    """
    voter = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='votes',
    )
    idea = models.ForeignKey(Idea, related_name='votes')
    ip = models.CharField(max_length=15, blank=True, null=True)

    created = CreationDateTimeField(null=True)

    class Meta:
        """
        Ensure that a voter can only cast one vote per idea.
        """
        unique_together = ['voter', 'idea']


def create_vote(user, idea, ip=None):
    """
    This is a helper function to create a vote. If ``user`` is an AnonymousUser
    then ``ip`` must be set. Otherwise call ``get_or_create`` on the Vote table
    to ensure that we are not violating the unique_together constraint between
    ``voter`` and ``idea``.
    """
    if ip and Vote.objects.filter(ip=ip).exists():
        return None, False
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
    vote, created = Vote.objects.get_or_create(**vote_kwargs)
    return vote, created


def get_votes_for_idea(idea):
    return Vote.objects.filter(idea=idea)
