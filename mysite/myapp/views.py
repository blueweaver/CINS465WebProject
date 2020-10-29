from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
# Create your views here.
def index(request):
    
    title = "Brandon's Website"
    posts = models.PostModel.objects.all()
    context = {
        "post":posts,
        "title":title,
    }
    return render(request, "displayPosts.html", context = context)

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