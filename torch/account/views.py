from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout,
)
from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render_to_response, get_object_or_404

from torch.account.forms import UserForm, MyAccountUserForm, ForgotEmailForm
from torch.account.models import send_email
from torch.idea.models import Idea


def _deal_with_form_validation(request, form, is_create):
    """
    Returns a tuple of the form:
        (True, User)
        (False, None)
    First section is weather or not the form was valid
    Second section is the user object created (or logged in)
    """
    form_is_valid = form.is_valid()
    user = None
    if form_is_valid:
        if is_create:
            form.save()
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user.is_active:
            django_login(request, user)
    return form_is_valid, user


def account(request, is_create):
    if is_create:
        Form = UserForm
    else:
        Form = AuthenticationForm
    if request.method == 'POST':
        # Stupid AuthenticationForm
        form = Form(data=request.POST)
        form_is_valid, _ = _deal_with_form_validation(request, form, is_create)
        if form_is_valid:
            return redirect('idea_create')
    else:
        form = UserForm()
    context = RequestContext(request, {
        'form': form,
        'is_create': is_create,
    })

    return render_to_response(
        'account/create.html',
        context_instance=context,
    )


def logout(request):
    django_logout(request)
    return redirect('account_login')


def my_account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.user.pk != user.pk:
        raise Http404()

    if request.method == 'POST':
        form = MyAccountUserForm(instance=user, data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('account_my_account', user_id=user.pk)
    else:
        form = MyAccountUserForm(instance=user)

    idea_qs = Idea.objects.filter(
        author=user,
    ).select_related()
    paginator = Paginator(idea_qs, settings.TORCH_PAGINATION)

    page = request.GET.get('page')

    try:
        ideas = paginator.page(page)
    except PageNotAnInteger:
        ideas = paginator.page(1)
    except EmptyPage:
        ideas = paginator.page(paginator.num_pages)

    context = RequestContext(request, {
        'user': user,
        'ideas': ideas,
        'form': form,
    })

    return render_to_response(
        'account/my_account.html',
        context_instance=context,
    )


def forgot_password(request, success):
    if request.method == 'POST':
        form = ForgotEmailForm(data=request.POST)
        if form.is_valid():
            send_email(form.cleaned_data['username'])
            return redirect('account_forgot_password_success')
    else:
        form = ForgotEmailForm()
    context = RequestContext(request, {
        'success': success,
        'form': form,
    })

    return render_to_response(
        'account/forgot_password.html',
        context_instance=context,
    )
