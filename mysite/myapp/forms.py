from django import forms
from . import models

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
   
    header.widget.attrs.update({'class': 'input', 'placeholder': 'Title'})
    post.widget.attrs.update({'class': 'input', 'placeholder': 'Idea'})