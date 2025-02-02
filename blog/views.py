from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin  # Added
from .models import Post

class BlogListView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'  # Better context name

class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detal.html'  # Fixed template name

class BlogCreateView(LoginRequiredMixin, CreateView):  # Added mixin
    model = Post
    template_name = 'new_post.html'  # Standard naming convention
    fields = ('title', 'body')  # Removed author from fields

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set author automatically
        return super().form_valid(form)
    
class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post_edit.html'  # Standard naming convention
    fields = ['title', 'body']

class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'  # Standard naming convention
    success_url = reverse_lazy('home')  # Redirect to home after deletion