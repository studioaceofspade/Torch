from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.simplejson import dumps

from torch.account.forms import UserForm as TorchUserForm
from torch.account.views import _deal_with_form_validation
from torch.idea.forms import make_IdeaForm
from torch.idea.models import Idea, order_by_popular
from torch.vote.models import create_vote


def create(request):
    IdeaForm = make_IdeaForm(request.user)
    is_create = False

    # If the user is logged in then we don't need a form.
    if request.user.is_authenticated():
        UserForm = None
    elif request.method == 'POST':
        # Figure out if its creating a user account or logging in.
        if 'first_name' in request.POST:
            is_create = True
            UserForm = TorchUserForm
        else:
            UserForm = AuthenticationForm

    if request.method == 'POST':
        # We need to authenticate the user and rebuild the IdeaForm
        user_form_is_valid = True
        if UserForm is not None:
            user_form = UserForm(data=request.POST)
            user_form_is_valid, user = _deal_with_form_validation(
                request,
                user_form,
                is_create,
            )
            if user_form_is_valid:
                IdeaForm = make_IdeaForm(user)
        idea_form = IdeaForm(request.POST)
        if idea_form.is_valid() and user_form_is_valid:
            idea = idea_form.save()
            url = reverse('idea_view', kwargs={'idea_id': idea.pk})
            return HttpResponse(
                dumps(
                    {'url': url},
                ),
                mimetype="application/json",
            )
    else:
        idea_form = IdeaForm()
        user_form = TorchUserForm()
    context = RequestContext(request, {
        'user_form': user_form,
        'idea_form': idea_form,
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


def vote(request, idea_id):
    idea = get_object_or_404(
        Idea.objects.select_related(),
        pk=idea_id,
    )
    ip = request.META['REMOTE_ADDR']
    host = request.META['REMOTE_HOST']
    vote, created = create_vote(
        request.user,
        idea,
        ip='%s:%s' % (host, ip),
    )
    return HttpResponse(
        dumps(
            {'created': created},
        ),
        mimetype="application/json",
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
