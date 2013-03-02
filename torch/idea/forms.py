from django.forms import ModelForm

from torch.idea.models import Idea


class IdeaForm(ModelForm):
    class Meta:
        model = Idea
