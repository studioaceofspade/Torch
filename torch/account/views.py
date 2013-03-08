from django.contrib.auth import authenticate, login as django_login
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render_to_response


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user.is_active:
                django_login(request, user)
            return redirect('idea_create')
    else:
        form = AuthenticationForm()
    context = RequestContext(request)
    data = {
        'form': form,
    }

    return render_to_response(
        'account/login.html',
        data,
        context_instance=context,
    )
