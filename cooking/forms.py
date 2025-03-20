from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, Post


class PostAddForm(forms.ModelForm):
    """Form for adding a post from a user."""

    class Meta:
        """Meta class that specifies the behavioral character, blueprint for the class."""

        model = Post
        fields = ('title', 'content', 'photo', 'category')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class SignInForm(AuthenticationForm):
    """User authentication form."""

    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class SignUpForm(UserCreationForm):
    """User registration form."""

    class Meta:
        """Meta class that specifies the behavioral character, blueprint for the class."""

        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
    )


class CommentForm(forms.ModelForm):
    """Form for writing a comment."""

    class Meta:
        """Meta class that specifies the behavioral character, blueprint for the class."""

        model = Comment
        fields = ('text',)

        widgets = {'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comment text'})}
