from django.template import RequestContext
from django.shortcuts import render_to_response

from torch.idea.models import Idea


def home(request):
    ideas = Idea.objects.all().select_related()
    most_recent_ideas = ideas.order_by(
        '-created',
    )[:3]
    top_ideas = ideas.order_by(
        '-num_votes',
    )[:3]
    context = RequestContext(request, {
        'most_recent_ideas': most_recent_ideas,
        'top_ideas': top_ideas,
    })

    return render_to_response(
        'home.html',
        context_instance=context,
    )


def about(request):
    context = RequestContext(request, {
    })

    return render_to_response(
        'about.html',
        context_instance=context,
    )


def contact(request):
    context = RequestContext(request, {
    })

    return render_to_response(
        'contact.html',
        context_instance=context,
    )
