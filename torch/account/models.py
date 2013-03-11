import uuid
from textwrap import dedent

from django.contrib.auth.models import User
from django.core.mail import send_mail as django_send_mail


def send_email(username):
    user = User.objects.get(
        username=username,
    )
    new_password = str(uuid.uuid4())
    user.set_password(new_password)
    user.save()
    django_send_mail(
        subject='Forgot password',
        message=dedent('''
            Your password has been reset to:

            %s

            Please log in and change the password to something easier to read.
        ''' % new_password),
        from_email='donotreply@donotreply.com',
        recipient_list=[username],
        fail_silently=True,
    )
