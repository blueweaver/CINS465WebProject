from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PostModel(models.Model):
    header = models.CharField(max_length = 100)
    post = models.CharField(max_length = 240)
    like = models.IntegerField(default=0)

    def __str__(self):
        return self.post

    def getLikes(self):
        return self.like

class LikeModel(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')
    likedPost = models.ForeignKey('PostModel', on_delete=models.CASCADE, related_name='liked_post')