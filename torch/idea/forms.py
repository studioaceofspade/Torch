from django.contrib.auth.models import User
from django.forms import ModelForm, ValidationError

from torch.idea.models import Idea


def make_IdeaForm(user):
    class IdeaForm(ModelForm):

        def clean(self, *args, **kwargs):
            result = super(IdeaForm, self).clean(*args, **kwargs)
            if not isinstance(user, User):
                raise ValidationError('This field is required.')
            return result

        def save(self, *args, **kwargs):
            self.instance.author = user
            return super(IdeaForm, self).save(*args, **kwargs)

        class Meta:
            model = Idea
            exclude = ('author')
    return IdeaForm
