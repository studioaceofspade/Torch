from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from torch.idea.forms import make_IdeaForm


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
    context = RequestContext(request)
    data = {
        'form': form,
    }

    return render_to_response(
        'idea/create.html',
        data,
        context_instance=context,
    )
