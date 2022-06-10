from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.views.decorators.cache import cache_page
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.views import View

from .forms import PostForm, CommentForm
from .models import Post, Group, Follow

User = get_user_model()


def page_not_found(request, exception=None):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)


@cache_page(20, key_prefix='index')
def index(request):
    posts = (
        Post.objects.select_related('author', 'group')
        .prefetch_related('comments')
        .all()
    )
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'index.html', {'page': page, 'paginator': paginator}
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    paginator = Paginator(
        Post.objects.select_related('author').filter(group=group), 10
    )
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'group.html',
        {'group': group, 'page': page, 'paginator': paginator},
    )


class AddPost(View):
    form_class = PostForm
    template_name = 'new_post.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        post = Post()
        post.author = request.user
        form = self.form_class(
            request.POST or None, files=request.FILES or None, instance=post
        )
        if form.is_valid():
            post.save()
            return redirect('index')
        return render(request, self.template_name, {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = (
        author.posts.select_related('group').prefetch_related('comments').all()
    )
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'profile.html',
        {
            'author': author,
            'posts_amount': paginator.count,
            'page': page,
            'paginator': paginator,
            'following': check_following_by_author_name(request, username),
        },
    )


def post_view(request, username, post_id):
    post = get_object_or_404(
        Post.objects.select_related('author', 'group').annotate(
            posts_amount=Count('author__posts')
        ),
        id=post_id,
        author__username=username,
    )
    comment_form = CommentForm()
    comments = post.comments.select_related('author').all()
    return render(
        request,
        'post.html',
        {
            'post': post,
            'author': post.author,
            'posts_amount': post.posts_amount,
            'form': comment_form,
            'comments': comments,
            'following': check_following_by_author_name(request, username),
        },
    )


@login_required()
def post_edit(request, username, post_id):
    """
    There is no need to pass Post entity to template, but test won't pass
    without it.
    """

    def return_to_post():
        return redirect('post', username=username, post_id=post.id)

    post = Post.objects.select_related('author').get(
        id=post_id, author__username=username
    )
    if post.author != request.user:
        return return_to_post()

    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post
    )
    if not form.is_valid():
        return render(request, 'new_post.html', {'form': form, 'post': post})
    post.save()

    return return_to_post()


@login_required()
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    else:
        for error in form['text'].errors:
            messages.add_message(request, messages.WARNING, error)
    return redirect('post', username=username, post_id=post.id)


@login_required
def follow_index(request):
    posts = (
        Post.objects.filter(author__following__user=request.user)
        .select_related('author', 'group')
        .prefetch_related('comments')
        .all()
    )
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'follow.html', {'page': page, 'paginator': paginator}
    )


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    else:
        messages.add_message(
            request,
            messages.WARNING,
            'Подписка возможна только на других авторов',
        )
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    following = Follow.objects.filter(
        user=request.user, author__username=username
    )
    if following:
        following.delete()
    return redirect('profile', username=username)


def check_following_by_author_name(request, author_name):
    """
        Check if current user subscribed to author
    """
    return (
        request.user.is_authenticated
        and Follow.objects.filter(
            user=request.user, author__username=author_name
        ).exists()
    )
