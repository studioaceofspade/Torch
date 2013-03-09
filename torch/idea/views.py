from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext

from torch.idea.forms import make_IdeaForm
from torch.idea.models import Idea


@login_required
def create(request):
    IdeaForm = make_IdeaForm(request.user)
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home')
    else:
        form = IdeaForm()
    context = RequestContext(request, {
        'form': form,
    })

    return render_to_response(
        'idea/create.html',
        context_instance=context,
    )


def view(request, idea_id):
    idea = get_object_or_404(
        Idea.objects.select_related(),
        pk=idea_id,
    )
    context = RequestContext(request, {
        'idea': idea,
    })

    return render_to_response(
        'idea/view.html',
        context_instance=context,
    )
