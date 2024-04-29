from django.shortcuts import render, redirect
from .forms import ProfileForm
from .models import Profile
# Create your views here.

def home_page(request):
    return render(request, 'index.html')



# blog/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

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
    success_url = reverse_lazy('`post_list`')

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

class Navbar(View):

    def get(self, request):
        action = request.GET.get('action')
        if action == 'about':
            return self.about(request)
        elif action == 'home':
            return self.home(request)
        return HttpResponse("NavbarView")

    def about(self,request):
        return render(request, 'about.html')

    def home(self, request):
        return render(request, 'index.html')
    
@login_required
def profile(request):
    profile_obj, created = Profile.objects.get_or_create(user = request.user)
    if request.method == 'POST':
        # post request
        form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile_obj)
    return render(request, 'profile.html', {'form':form, 'username':request.user.username})