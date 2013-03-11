from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    username = forms.EmailField(
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
        email = self.cleaned_data['username']
        if email:
            self.instance.email = email

        return super(UserForm, self).save(*args, **kwargs)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'password',
        )


class MyAccountUserForm(forms.Form):
    username = forms.EmailField(
        label='Email Address',
        required=False,
        max_length=130,
        widget=forms.TextInput(attrs={
            'autocompleate': 'off',
            'placeholder': 'yourname@example.com',
        }),
    )
    first_name = forms.CharField(
        label='Your Name',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'autocompleate': 'off',
            'placeholder': 'What shall we call you?',
        }),
    )
    password1 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'autocompleate': 'off'}),
    )
    password = forms.CharField(
        label='Password',
        required=False,
        widget=forms.PasswordInput(attrs={'autocompleate': 'off'}),
    )

    def __init__(self, instance=None, *args, **kwargs):
        form = super(MyAccountUserForm, self).__init__(*args, **kwargs)
        self.instance = instance
        self.fields['username'].widget.attrs['placeholder'] = instance.username
        first_name_widget = self.fields['first_name'].widget
        first_name_widget.attrs['placeholder'] = instance.first_name
        return form

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name == '':
            return self.instance.first_name
        else:
            self.instance.first_name = first_name
        return first_name

    def clean_username(self):
        username = self.cleaned_data['username']
        if username == '':
            return self.instance.username
        username = username.lower()  # All usernames must be lowercase.

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'This email is already taken. Please choose another.',
            )
        self.instance.username = username

        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        password1 = self.cleaned_data['password1']
        if password == '' and password1 == '':
            return password1
        if password != password1:
            raise forms.ValidationError('The two passwords did not match.')
        return password1

    def save(self, *args, **kwargs):
        password = self.cleaned_data['password']
        if password:
            self.instance.set_password(password)
        email = self.cleaned_data['username']
        if email:
            self.instance.email = email
        self.instance.save()
        return self.instance

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'password',
        )


class ForgotEmailForm(forms.Form):
    username = forms.EmailField(
        label='Email Address',
        required=True,
        max_length=130,
        widget=forms.TextInput(attrs={
            'autocompleate': 'off',
            'placeholder': 'yourname@example.com',
        }),
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(email=username).exists():
            raise forms.ValidationError(
                'That email address is not in our records, please try another',
            )
        return username
