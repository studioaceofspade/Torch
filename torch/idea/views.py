from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.simplejson import loads

from torch.idea.forms import make_IdeaForm
from torch.idea.models import Idea, order_by_popular


def create(request):
    IdeaForm = make_IdeaForm(request.user)
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            idea = form.save()
            url = str(reverse('idea_view', kwargs={'idea_id': idea.pk}))
            return HttpResponse(
                loads(
                    {'url': url},
                ),
                mimetype="application/json",
            )
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


def manage(request):
    idea_qs = Idea.objects.all().select_related()
    sort = request.GET.get('sort')
    available_sorts = {
        'num_votes': '-num_votes',
        'popular': '',
    }
    if sort and sort in available_sorts:
        if sort == 'popular':
            idea_qs = order_by_popular(idea_qs)
        else:
            idea_qs = idea_qs.order_by(available_sorts[sort])
    paginator = Paginator(idea_qs, settings.TORCH_PAGINATION)

    page = request.GET.get('page')

    try:
        ideas = paginator.page(page)
    except PageNotAnInteger:
        ideas = paginator.page(1)
    except EmptyPage:
        ideas = paginator.page(paginator.num_pages)
    context = RequestContext(request, {
        'sort': sort,
        'ideas': ideas,
    })
    return render_to_response(
        'idea/manage.html',
        context_instance=context,
    )
