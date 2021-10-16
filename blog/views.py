from django.shortcuts import get_object_or_404, redirect, render,get_object_or_404
from .models import Post
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User
# from django.http import HttpResponse

#Dummy DATA
posts=[
    {
        'author':'APking' ,
        'title': 'CP',
        'content': 'CP is the best way to practice DS and ALGO',
        'date_posted': '26 Sept 2021'
    },
    {
        'author':'ishanmjr' ,
        'title': 'DEV',
        'content': 'Start with HTML & CSS in Web developement followed by javascript',
        'date_posted': '27 Sept 2021'
    }
]
#function view
def home(request):
    context={
        'posts':Post.objects.all()
    }
    return render(request,'blog/home.html',context)
#class list view
class PostListView(ListView):
    model=Post
    template_name='blog/home.html' # searching for <app>/<model>_<viewtype>.html by default
    context_object_name='posts' # here by defalut varible is object list intead of posts
    ordering=['-date_posted']
    paginate_by=5

class UserPostListView(ListView):
    model=Post
    template_name='blog/user_posts.html'
    context_object_name='posts' 
    paginate_by=5
    
    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model=Post

class PostCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model=Post
    fields=['title','content']
    success_message='Post Created Successfully'
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin,LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model=Post
    fields=['title','content']
    success_message='Post Updated Successfully'
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    def test_func(self):
        post=self.get_object()
        return self.request.user==post.author

class PostDeleteView(UserPassesTestMixin,LoginRequiredMixin,SuccessMessageMixin,DeleteView):
    model=Post
    success_message='Post Deleted Successfully'
    success_url='/'
    def test_func(self):
        post=self.get_object()
        return self.request.user==post.author
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)

def about(request):
    return render(request,'blog/about.html',{'title':'About'})
