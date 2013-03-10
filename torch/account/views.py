from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout,
)
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render_to_response

from torch.account.forms import UserForm


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
