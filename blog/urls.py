from django.urls import path
from . import views
urlpatterns = [
    path("",views.starting_page.as_view(),name="starting_page"),
    path("posts",views.posts.as_view(),name="post-page"),
    path("posts/<slug:slug>",views.post_detail.as_view(),name="post-page-detail"),
    path("read-later",views.ReadLaterView.as_view(),name="read-later"),
    path("register",views.RegisterView.as_view(),name="register"),
    path("login",views.loginview.as_view(),name="login")
]
