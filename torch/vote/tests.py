from django.contrib.auth.models import User
from django.test import TestCase

from torch.idea.models import create_idea
from torch.vote.models import Vote, create_vote, get_votes_for_idea


class VoteTestCase(TestCase):
    def test_simple(self):
        user = User.objects.create()
        idea = create_idea(
            user=user,
            title='test',
            description='foobar',
        )
        vote = Vote.objects.create(
            voter=user,
            idea=idea,
        )
        self.assertNotEqual(vote, None)

    def test_create_vote(self):
        # We will be using the create_idea function to create idea objects, so
        # I only ever have to change it in one place.
        user = User.objects.create()
        idea = create_idea(
            user=user,
            title='test',
            description='foobar',
        )
        vote = create_vote(
            user=user,
            idea=idea,
        )
        self.assertNotEqual(idea, None)
        self.assertEqual(vote.voter, user)
        self.assertEqual(vote.idea, idea)

    def test_get_votes_for_idea(self):
        # Create two ideas, give one of them one vote, and the other two votes,
        # make sure the expected counts are correct.
        user = User.objects.create()

        # Two ideas
        idea_1 = create_idea(
            user=user,
            title='test',
            description='foobar',
        )
        idea_2 = create_idea(
            user=user,
            title='test',
            description='foobar',
        )

        # Three votes, one 1 and two for 2
        vote_1 = create_vote(
            user=user,
            idea=idea_1,
        )
        vote_2 = create_vote(
            user=user,
            idea=idea_2,
        )
        vote_3 = create_vote(
            user=user,
            idea=idea_2,
        )

        # Make sure the vote counts, vote pks are correct
        votes = get_votes_for_idea(idea_1)
        self.assertEqual(votes.count(), 1)
        self.assertEqual(
            set(votes.values_list('pk', flat=True)),
            set([vote_1.pk]),
        )

        votes = get_votes_for_idea(idea_2)
        self.assertEqual(votes.count(), 2)
        self.assertEqual(
            set(votes.values_list('pk', flat=True)),
            set([vote_2.pk, vote_3.pk]),
        )
