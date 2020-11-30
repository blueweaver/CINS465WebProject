from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django.template.defaultfilters import slugify
from . import forms
from . import models
# Create your views here.
def index(request):
    
    title = "Brandon's Website"
    posts = models.PostModel.objects.all()
    common_tags = models.PostModel.tags.most_common()[:20]
    context = {
        "post":posts,
        "title":title,
        "common_tags":common_tags,
    }
    return render(request, "home.html", context = context)

#This function is inspired by this stack overflow post: rb.gy/pb8u2y
@login_required(redirect_field_name='main')
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

def logout_view(request):
    logout(request)
    return redirect("/login/")

def register(request):
    if request.method == "POST":
        form_instance = forms.RegistrationForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect("/login/")
    else:
        form_instance = forms.RegistrationForm()
    context = {
        "form":form_instance,
    }
    return render(request, "registration/register.html", context=context)

def addComment(request, pk):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            form.save(request, pk)
            return redirect("/")
    else:
        form = forms.CommentForm()
    context = {
        "title":"Comment",
        "post_id":pk,
        "form":form
    }
    return render(request, "addComment.html", context=context)

def addPost(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = forms.PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request)
            return redirect("/")
    else:
        form = forms.PostForm()
    context = {
        "title":"Make Content",
        "form":form
    }
    return render(request, "addPost.html", context=context)


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    common_tags = models.PostModel.tags.most_common()[:20]
    posts = models.PostModel.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'common_tags':common_tags,
        'post':posts,
    }
    return render(request, 'home.html', context=context)
