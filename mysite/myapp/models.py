from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.
class PostModel(models.Model):
    header = models.CharField(max_length = 100)
    post = models.CharField(max_length = 240)
    like = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now_add=True) 
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()
    gif = models.ImageField(
        max_length=144,
        upload_to='uploads/%Y/%m/%d/',
        null=False
    )
    audio = models.FileField(
        max_length=144,
        upload_to='uploads/%Y/%m/%d/',
        null=False
    )

    def __str__(self):
        return self.post

    def getLikes(self):
        return self.like

class LikeModel(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')
    likedPost = models.ForeignKey('PostModel', on_delete=models.CASCADE, related_name='liked_post')


class CommentModel(models.Model):
    comment = models.CharField(max_length=240)
    post = models.ForeignKey('PostModel', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.comment
