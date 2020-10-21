from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from . import forms
from . import models
# Create your views here.
def index(request):
    
    if request.method == "POST":
        post_form = forms.postForm(request.POST)
        if post_form.is_valid():
            post_form.save()
            post_form = forms.postForm()

    else:
        post_form = forms.postForm()
    
    title = "Brandon's Website"
    posts = models.PostModel.objects.all()
    context = {
        "post":posts,
        "title":title,
        "form":post_form,
    }
    return render(request, "displayPosts.html", context = context)


def likeView(request, pk):
    is_liked = False
    post = get_object_or_404(models.PostModel, id=request.POST.get('post_id'))
    try:
        models.LikeModel.objects.get(likedPost = post, liker=request.user)
        is_liked = True
    except models.LikeModel.DoesNotExist:
        pass
    if(is_liked == False):
        models.LikeModel.objects.create(liker=request.user, likedPost=post)
        post.like = post.like + int(1)
        post.save()
    else:
        like = models.LikeModel.objects.get(liker=request.user, likedPost=post)
        like.delete()
        post.like = post.like - int(1)
        post.save()
    return HttpResponseRedirect(reverse("main"))