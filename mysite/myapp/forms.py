from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models


def must_be_unique(value):
    user = User.objects.filter(email=value)
    if len(user) > 0:
        raise forms.ValidationError("Email Already in Use")
    return value

class postForm(forms.Form):
    
    header = forms.CharField(
        label='Enter Title',
        required = True,
        max_length = 100,
    )

    post = forms.CharField(
        label='Enter Idea',
        required = True,
        max_length = 240,
    ) 


    def save(self):
        post_instance = models.PostModel()
        post_instance.post = self.cleaned_data["post"]
        post_instance.header = self.cleaned_data["header"]
        post_instance.save()
        return post_instance

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        validators=[must_be_unique]
    )

    class Meta:
        model = User
        fields = ("username", "email",
                  "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CommentForm(forms.Form):

    comment = forms.CharField(
        label='Enter Idea',
        required = True,
        max_length = 240,
    ) 

    def save(self, request, post_id):
        post_instance = models.PostModel.objects.get(id=post_id)
        comment_instance = models.CommentModel()
        comment_instance.post = post_instance
        comment_instance.comment = self.cleaned_data["comment"]
        comment_instance.author = request.user
        comment_instance.save()
        return comment_instance