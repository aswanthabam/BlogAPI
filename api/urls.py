from django.urls import path
from .views import PostView, TokenView, UserRegisterView, UserVerify

urlpatterns = [
    path('user/register/', UserRegisterView.as_view()),
    path('user/is-logged-in/', UserVerify.as_view()),
    path('user/login/', TokenView.as_view()),

    path('posts/', PostView.as_view()),
    path('posts/create/', PostView.as_view()),
    path('posts/<str:slug>/', PostView.as_view()),
    path('posts/<str:slug>/edit/', PostView.as_view()),
    path('posts/<str:slug>/delete/', PostView.as_view())
]