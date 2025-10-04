from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from django import forms
from .models import CustomUser, Post, Comment
from taggit.forms import TagWidget

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'profile_picture']


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Enter your email", max_length=254,
    widget= forms.TextInput(attrs={'placeholder': 'Email'}))


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
        'content': forms.Textarea(attrs={'rows': 3, 'cols': 50})
    }


        def clean_content(self):
            content = self.cleaned_data['content']
            if not content:
                raise forms.ValidationError('Comment content cannot be empty.')
            if len(content) < 5:
                raise forms.ValidationError('Comment content must be atleast 5 characters long')
            return content
