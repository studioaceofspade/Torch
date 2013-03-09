from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    username = forms.CharField(
        label='Email Address',
        required=True,
        max_length=130,
        widget=forms.TextInput(attrs={
            'autocompleate': 'off',
            'placeholder': 'yourname@example.com',
        }),
    )
    first_name = forms.CharField(
        label='Your Name',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'autocompleate': 'off',
            'placeholder': 'What shall we call you?',
        }),
    )
    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={'autocompleate': 'off'}),
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        username = username.lower()  # All usernames must be lowercase.

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'This email is already taken. Please choose another.',
            )

        return username

    def save(self, *args, **kwargs):
        password = self.cleaned_data['password']
        if password:
            self.instance.set_password(password)

        return super(UserForm, self).save(*args, **kwargs)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'password',
        )
