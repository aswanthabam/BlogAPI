from django.urls import path
from .views import PostView, TokenView, UserRegisterView, UserVerify, TokenRefresh, GetPostsView

urlpatterns = [
    path('user/register/', UserRegisterView.as_view()),
    path('user/is-logged-in/', UserVerify.as_view()),
    path('user/login/', TokenView.as_view()),
    path('user/refresh-token/', TokenRefresh.as_view()),

    path('posts/', GetPostsView.as_view()),
    path('posts/create/', PostView.as_view()),
    path('posts/<str:slug>/', GetPostsView.as_view()),
    path('posts/<str:slug>/edit/', PostView.as_view()),
    path('posts/<str:slug>/delete/', PostView.as_view())
]