from django.contrib.auth.models import User
from django import forms

from torch.idea.models import Idea


def make_IdeaForm(user):

    class IdeaForm(forms.ModelForm):
        title = forms.CharField(
            label='What do you want to call your idea?',
            required=True,
            max_length=200,
            widget=forms.TextInput(attrs={
                'placeholder': 'I think it would be a good idea if Elkhart...',
                'class': 'input-xxlarge title-input',
                'type': 'text',
            }),
        )
        description = forms.CharField(
            required=True,
            label='Why should people like your idea?',
            widget=forms.Textarea(attrs={
                'placeholder': 'The reason we should do this is...',
                'class': 'input-xxlarge description-input',
                'type': 'text',
                'rows': '2',
            }),
        )

        def clean(self, *args, **kwargs):
            result = super(IdeaForm, self).clean(*args, **kwargs)
            if not isinstance(user, User):
                raise forms.ValidationError('This field is required.')
            return result

        def save(self, *args, **kwargs):
            self.instance.author = user
            return super(IdeaForm, self).save(*args, **kwargs)

        class Meta:
            model = Idea
            exclude = ('author')
    return IdeaForm
