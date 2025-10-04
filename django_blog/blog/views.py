from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, CustomPasswordResetForm, CommentForm
from django.contrib.auth.views import PasswordResetView
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment
from django.views import View
from haystack.query import SearchQuerySet
from taggit.models import Tag


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            form = RegistrationForm()
        return render(request, 'register.html', {'form': form})
    

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = '/password_reset/done/'
    

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    if request.method =="POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            form = ProfileForm(instance=request.user)
        return render(request, 'edit_profile.html', {'form': form})
    

# --- PostListView ---
class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    ordering = ['-created_at']


# --- PostDetailView ---
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


# --- PostCreateView ---
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'tags']
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# --- PostUpdateView ---
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'tags']
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
# --- PostDeleteView ---
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    


# Comment create view

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        post_id = self.kwargs.get('post_id')
        return reverse('post_detail', kwargs={'pk': post_id})
    


# Comment update view
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        post_id = self.object.post.pk
        return reverse('post_detail', kwargs={'pk': post_id})
    

# Comment delete view 
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        post_id = self.object.post.pk
        return reverse('post_detail', kwargs={'pk': post_id})
    

# --- Search Function view ---
class SearchView(View):
    def get(self, request):
        query = request.GET.get('q')
        if query:
            sqs = SearchQuerySet().autocomplete(text=query)
            posts = [result.object for result in sqs]
        else:
            posts = []
        return render(request, 'search_results.html', {'posts': posts})
    

# --- Tag Function ---
def tagged_posts(request, slug):
    tag = Tag.objects.get(slug=slug)
    posts = Post.objects.filter(tags__slug=tag.slug)
    return render(request, 'tagged_posts.html', {'posts': posts, 'tag': tag})
