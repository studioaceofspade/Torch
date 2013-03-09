from django.contrib.auth import authenticate, login as django_login
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render_to_response

from torch.account.forms import UserForm


def account(request, is_create):
    if is_create:
        Form = UserForm
    else:
        Form = AuthenticationForm
    if request.method == 'POST':
        # Stupid AuthenticationForm
        form = Form(data=request.POST)
        if form.is_valid():
            if is_create:
                form.save()
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user.is_active:
                django_login(request, user)
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
