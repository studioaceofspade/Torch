from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    username = forms.CharField(
        required=False,
        max_length=130,
        widget=forms.TextInput(attrs={'autocompleate': 'off'}),
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'autocompleate': 'off'}),
        required=True,
    )
    password2 = forms.CharField(
        label='Verify Password',
        required=True,
        widget=forms.PasswordInput(attrs={'autocompleate': 'off'}),
    )
    first_name = forms.CharField(
        label='First Name',
        max_length=30,
        required=True,
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        username = username.lower()  # All usernames must be lowercase.

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'This username is already taken. Please choose another.',
            )

        return username

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if (password1 or password2):
            if password1 != password2:
                raise forms.ValidationError('The passwords must match.')
        elif not self.instance.pk:
            raise forms.ValidationError('You must supply a password.')
        return password2

    def save(self, *args, **kwargs):
        password = self.cleaned_data['password1']
        if password:
            self.instance.set_password(password)

        return super(UserForm, self).save(*args, **kwargs)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
        )
