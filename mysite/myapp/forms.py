from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from taggit.models import Tag
from taggit.forms import *
from moviepy.editor import *
import subprocess
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from . import models


def must_be_unique(value):
    user = User.objects.filter(email=value)
    if len(user) > 0:
        raise forms.ValidationError("Email Already in Use")
    return value

def must_be_unique_header(value):
    title = models.PostModel.objects.filter(header=value)
    if len(title) > 0:
        raise forms.ValidationError("Title Already in Use")
    return value





class PostForm(forms.Form):
    
    header = forms.CharField(
        label='Enter Title',
        required = True,
        max_length = 100,
        validators=[must_be_unique_header]
    )

    post = forms.CharField(
        label='Enter Description',
        required = True,
        max_length = 240,
    ) 

    gif = forms.FileField(
        label='Enter Gif',
        required = True,
        validators=[FileExtensionValidator(['gif'])]
    )

    audio = forms.FileField(
        label='Enter MP3',
        required = True,
        validators=[FileExtensionValidator(['mp3'])]
    )

    tags = TagField(
        label='Enter Tags',
        max_length = 240,
    ) 

    def save(self, request):
        post_instance = models.PostModel()
        post_instance.post = self.cleaned_data["post"]
        post_instance.header = self.cleaned_data["header"]
        post_instance.gif = self.cleaned_data["gif"]
        post_instance.audio = self.cleaned_data["audio"]
        post_instance.author = request.user
        post_instance.slug = slugify(post_instance.header)
        tags = self.cleaned_data['tags']
        post_instance.save()
        for tag in tags:
            post_instance.tags.add(tag)
        #video = VideoFileClip(post_instance.gif.path)
        #video.set_audio(post_instance.audio.path)
        #post_instance.finalVideo = video
        #video.close()
        #video._committed = False
        #post_instance.save()
        
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