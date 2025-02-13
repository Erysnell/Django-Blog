from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from .models import Post

class BlogListView(ListView):
 model = Post
 template_name = "home.html"

class BlogDetailView(DetailView): # new
 model = Post
 template_name = "post_detail.html"

class BlogCreateView(LoginRequiredMixin,CreateView): 
    model = Post
    template_name = "post_new.html"
    fields = ["title", "body"]
    login_url = 'login' 
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) # Redirige a esta URL si el usuario no está autenticado

class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # new
 model = Post
 template_name = "post_edit.html"
 fields = ["title", "body"]
 login_url = 'login'

 def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class BlogDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView): # new
 model = Post
 template_name = "post_delete.html"
 success_url = reverse_lazy("home")
 login_url = 'login'

 def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user