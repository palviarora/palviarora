from django.shortcuts import render

# Create your views here.

def home_page(request):
    return render(request, 'index.html')



# blog/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('post_list')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
