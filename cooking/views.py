from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.db.models import F, Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .forms import CommentForm, PostAddForm, SignInForm, SignUpForm
from .models import Category, Comment, Post
from .serializers import CategorySerializer, PostSerializer


class Index(ListView):
    """For the main page."""

    model = Post
    context_object_name = 'posts'
    template_name = 'cooking/index.html'
    extra_context = {'title': 'Main page'}


def get_category_list(request, pk):
    """Reaction to click on category button."""
    posts = Post.objects.filter(category_id=pk)

    context = {
        'title': posts[0].category,
        'posts': posts,
    }

    return render(request, 'cooking/index.html', context)


def get_post_detail(request, pk):
    """Post page."""
    post = Post.objects.get(pk=pk)
    Post.objects.filter(pk=pk).update(watched=F('watched') + 1)
    additional_post = Post.objects.all().exclude(pk=pk).order_by('-watched')
    comments = Comment.objects.filter(post=post)

    context = {
        'title': post.title,
        'post': post,
        'comments': comments,
        'additional_posts': additional_post,
    }

    if request.user.is_authenticated:
        context['comment_form'] = CommentForm

    return render(request, 'cooking/post_detail.html', context)


def sign_up(request):
    """User registration."""
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered')
            return redirect('log_in')
    else:
        form = SignUpForm()

    context = {
        'title': 'Sign up',
        'form': form,
    }

    return render(request, 'cooking/sign_up_form.html', context)


def user_login(request):
    """User authentication."""
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('index')
    else:
        form = SignInForm()

    context = {
        'title': 'Sign in',
        'form': form,
    }

    return render(request, 'cooking/sign_in_form.html', context)


def user_logout(request):
    """User log out."""
    logout(request)
    return redirect('index')


class PostAdd(CreateView):
    """Adding a post from a user."""

    form_class = PostAddForm
    template_name = 'cooking/post_add_form.html'
    extra_context = {'title': 'Add post'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(UpdateView):
    """Editing a post with a button."""

    model = Post
    form_class = PostAddForm
    template_name = 'cooking/post_add_form.html'
    extra_context = {'title': 'Editing post'}


class PostDelete(DeleteView):
    """Deleting a post with a button."""

    model = Post
    success_url = reverse_lazy('index')
    context_object_name = 'post'


class SearchResults(Index):
    """Search for a word in titles and in the content of articles."""

    def get_queryset(self):
        word = self.request.GET.get('q')

        return Post.objects.filter(Q(title__icontains=word) | Q(content__icontains=word))


def add_comment(request, post_id):
    """Adding a comment to a post."""
    form = CommentForm(data=request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = Post.objects.get(pk=post_id)
        comment.save()
        messages.success(request, 'Your comment has been successfully added')

    return redirect('post_detail', post_id)


def get_profile(request, user_id):
    """User page."""
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(author=user)

    context = {
        'user': user,
        'posts': posts,
    }

    return render(request, 'cooking/profile.html', context)


class UserChangePassword(PasswordChangeView):
    """Simplified way to change user password."""

    template_name = 'cooking/password_change_form.html'
    success_url = reverse_lazy('index')


class CookingPostsAPI(ListAPIView):
    """Getting all posts via API."""

    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer


class CookingPostAPIDetail(RetrieveAPIView):
    """Getting a post via API."""

    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)


class CookingCategoriesAPI(ListAPIView):
    """Getting all categories via API."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CookingCategoryAPIDetail(RetrieveAPIView):
    """Getting a category via API."""

    queryset = Post.objects.filter(is_published=True)
    serializer_class = CategorySerializer


class SwaggerAPIDoc(TemplateView):
    """API documentation."""

    template_name = 'swagger/swagger_ui.html'
    extra_context = {
        'schema_url': 'openapi-schema',
    }
