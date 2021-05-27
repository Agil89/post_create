from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import Post

USER_MODEL = get_user_model()


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('Username'),
        'autofocus': True
    }), )
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('my_post',)
        widgets = {
            'user_name': forms.TextInput(attrs={
                'label':'My post',
                'class': 'form-control',
            }),
        }

