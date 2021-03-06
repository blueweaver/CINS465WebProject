from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name = 'main'),
    path('like/<int:pk>', views.likeView, name='likePost'),
    path('login/', auth_views.LoginView.as_view()),
    path('register/', views.register),
    path('logout/', views.logout_view),
    path('comment/<int:pk>', views.addComment, name='addComment'),
    path('post/', views.addPost, name='addPost'),
    path('tag/<slug:slug>/', views.tagged, name="tagged"),
    path('detail/<int:pk>', views.detailPostView, name='detailPost'),
    path('user/<int:pk>', views.userView, name='userView'),
    path('popular/', views.sortByPop, name='popular'),
    path('new/', views.sortByNew, name='new'),
    path('subscribe/<int:pk>', views.subscribeView, name='sub'),

]