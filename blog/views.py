from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from datetime import date
from .models import Post
from django.views.generic import ListView,View
from .forms import CommentForm,CustomUserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


class starting_page(ListView):
    template_name="blog/index.html"
    model=Post
    ordering=["-date"]
    context_object_name="posts"
    
    def get_queryset(self):
        queryset= super().get_queryset()
        query=queryset[:]
        return query
    
# def starting_page(request):
#     latest_post=Post.objects.all().order_by("-date")[:3]
#     return render(request,"blog/index.html",{
#         "posts": latest_post
#     })

# def posts(request):
#     all_posts=Post.objects.all()
#     return render(request,"blog/all-posts.html",{
#         "posts":all_posts
#     })
class posts(ListView):
    template_name="blog/all-posts.html"
    model = Post
    ordering=["-date"]
    context_object_name="list"
    
class post_detail(View):
    def is_stored(self,request,post_id):
        stored_post=request.session.get("stored_post")
        if stored_post is not None:
            marked_post=post_id in stored_post
        else:
            marked_post=False
            
        return marked_post
    def get(self,request,slug):
        post=Post.objects.get(slug=slug)
        return render(request,"blog/post-detail.html",{
            "post":post,
            "post_tags":post.tags.all(),
            "comment_form":CommentForm(),
            "all_comments":post.comments.all().order_by("-id"),
            "marked_post":self.is_stored(request,post.id)
        })
        
    def post(self,request,slug):
        comment=CommentForm(request.POST)
        post=Post.objects.get(slug=slug)
        
        if comment.is_valid():
            comment=comment.save(commit=False)
            comment.post=post
            comment.save()
            return HttpResponseRedirect(reverse("post-page-detail",args=[slug]))
        post=Post.objects.get(slug=slug)
        return render(request,"blog/post-detail.html",{
            "post":post,
            "post_tags":post.tags.all(),
            "comment_form":comment,
            "all_comments":post.comments.all().order_by("-id"),
            "marked_post":self.is_stored(request,post.id)
        })
        

class ReadLaterView(View):
    
    def get(self,request):
        stored_post=request.session.get("stored_post")
        
        context={}
        if stored_post is None or len(stored_post)==0:
            context["posts"]=[]
            context["has_posts"]=False
        else:
            posts=Post.objects.filter(id__in=stored_post)
            context["posts"]=posts
            context["has_posts"]=True 
        
        return render(request,"blog/stored-posts.html",context)
        
    
    def post(self,request):
        stored_post=request.session.get("stored_post")
        
        if stored_post is None:
            stored_post=[]
        
        post_id= int(request.POST["post_id"])
        
        if post_id not in stored_post:
            stored_post.append(post_id)
        else:
            stored_post.remove(post_id)
            
        request.session["stored_post"]=stored_post
            
        return HttpResponseRedirect("/")
    
# class RegisterView(View):
    
#     def get(self,request):
#         form=RegisterForm()
#         is_equal=False
#         return render(request,"blog/register.html",{
#                 "forms":form,
#                 "is_equal":is_equal
#             })
#     def post(self,request):
#         form=RegisterForm(request.POST)
#         data1=request.POST['password_1']
#         data2=request.POST['password_2']
#         is_equal=False
        
#         if form.is_valid():
#             if data1==data2:
#                 form.save()
#                 return HttpResponseRedirect(reverse("login"))
#             else:
#                 is_equal=True
#                 form=RegisterForm(request.POST)
#                 return render(request,"blog/register.html",{
#                 "forms":form,
#                 "is_equal":is_equal
#             })
#         else:
#             form=RegisterForm()
#             return render(request,"blog/login.html",{
#                 "forms":form
#             })
class RegisterView(View):
    def get(self,request):
        forms=CustomUserCreationForm()
        return render(request,"blog/register.html",{
            "form":forms
        })
    def post(self,request):
        forms=CustomUserCreationForm(request.POST)
        if forms.is_valid():
            forms.save()
            return HttpResponseRedirect(reverse("login"))
        
        return render(request,"blog/register.html",{
            "form":forms
        })   
                
# class loginview(View):
#     def get(self,request):
#         return render(request,"blog/login.html")
#     def post(self, request):
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user=Register.objects.get(user_name=username)
#         if user.user_name==username and user.password_2==password:
#             return HttpResponseRedirect(reverse("starting_page"))
#         else:
#             error_message = "The user does not exist or incorrect password. Please try again!"
#             context = {
#                 "error_message": error_message
#             }
#             return render(request, "blog/login.html", context)
class loginview(View):
    def get(self, request):
        return render(request, "blog/login.html")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("starting_page"))  # Redirect to the homepage after successful login
        else:
            error_message = "Invalid username or password. Please try again."
            return render(request, "blog/login.html", {"error_message": error_message})
        
    
            
        
    
        
 