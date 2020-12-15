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
    if(request.user.is_authenticated):
        subscriptions = models.SubscribeModel.objects.all()
        currentSubs = subscriptions.filter(subscriber = request.user)
        currentFollowers = subscriptions.filter(creator = request.user)
    else:
        currentSubs = "Login"
        currentFollowers = "login"
    context = {
        "post":posts,
        "title":title,
        "common_tags":common_tags,
        "currentSubs":currentSubs,
        "currentFollowers":currentFollowers,
    }
    return render(request, "home.html", context = context)

def detailPostView(request, pk):
    title = "Detail"
    post = get_object_or_404(models.PostModel, id=pk)
    room_name = post.header
    context = {
        "post":post,
        "title":title,
        'room_name': room_name
    }
    return render(request, "detailPost.html", context = context)

def userView(request, pk):
    post = get_object_or_404(models.PostModel, id=pk)
    title = post.author
    personalPosts = models.PostModel.objects.filter(author = post.author)
    like = models.LikeModel.objects.filter(liker = post.author)
    likedPosts = set()
    for itor in like:
        likedPosts.add(models.PostModel.objects.get(header = itor.likedPost))
    context = {
        "author":post.author,
        "personalPost":personalPosts,
        "likedPost":likedPosts,
        "title":title,
    }
    return render(request, "userPage.html", context = context)

#This function is inspired by this stack overflow post: rb.gy/pb8u2y
@login_required(redirect_field_name='main')
def likeView(request, pk):
    is_liked = False
    post = get_object_or_404(models.PostModel, id=pk)
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
    return  HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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
    if(request.user.is_authenticated):
        subscriptions = models.SubscribeModel.objects.all()
        currentSubs = subscriptions.filter(subscriber = request.user)
        currentFollowers = subscriptions.filter(creator = request.user)
    else:
        currentSubs = "Login"
        currentFollowers = "login"
    context = {
        'tag':tag,
        'common_tags':common_tags,
        'post':posts,
        "currentSubs":currentSubs,
        "currentFollowers":currentFollowers,
    }
    return render(request, 'home.html', context=context)


def sortByPop(request):
    title = "Brandon's Website"
    posts = models.PostModel.objects.all()
    sortedPosts = sorted(posts, key=lambda self: self.getLikes(), reverse=True)
    common_tags = models.PostModel.tags.most_common()[:20]
    room_name = "home"
    if(request.user.is_authenticated):
        subscriptions = models.SubscribeModel.objects.all()
        currentSubs = subscriptions.filter(subscriber = request.user)
        currentFollowers = subscriptions.filter(creator = request.user)
    else:
        currentSubs = "Login"
        currentFollowers = "login"
    context = {
        "post":sortedPosts,
        "title":title,
        "common_tags":common_tags,
        "currentSubs":currentSubs,
        "currentFollowers":currentFollowers,
    }
    return render(request, "home.html", context = context)

def sortByNew(request):
    title = "Brandon's Website"
    posts = models.PostModel.objects.all()
    sortedPosts = sorted(posts, key=lambda self: self.getDate(), reverse=True)
    common_tags = models.PostModel.tags.most_common()[:20]
    room_name = "home"
    if(request.user.is_authenticated):
        subscriptions = models.SubscribeModel.objects.all()
        currentSubs = subscriptions.filter(subscriber = request.user)
        currentFollowers = subscriptions.filter(creator = request.user)
    else:
        currentSubs = "Login"
        currentFollowers = "login"
    context = {
        "post":sortedPosts,
        "title":title,
        "common_tags":common_tags,
        "currentSubs":currentSubs,
        "currentFollowers":currentFollowers,
    }
    return render(request, "home.html", context = context)

@login_required(redirect_field_name='main')
def subscribeView(request, pk):
    is_subscribed = False
    subcription = get_object_or_404(models.PostModel, id=pk)
    if(request.user == subcription.author):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    try:
        models.SubscribeModel.objects.get(subscriber=request.user, creator=subcription.author)
        is_subscribed = True
    except models.SubscribeModel.DoesNotExist:
        pass
    if(is_subscribed == False):
        models.SubscribeModel.objects.create(subscriber=request.user, creator=subcription.author)
    else:
        sub = models.SubscribeModel.objects.get(subscriber=request.user, creator=subcription.author)
        sub.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
