from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from posts.forms import PostForm
from posts.models import Post
from posts.permitions.PostEditChecker import PostEditChecker


@login_required
def new_post(request):
    """
    Just as memo: functional usage
    Using if not request.method and if not form.is_valid() makes us to use
    multiple returns.
    To DRY we'll use render_form
    """

    def render_form(form_to_render: PostForm):
        return render(request, 'new_post.html', {'form': form_to_render})

    form = PostForm(request.POST or None)
    if not request.method == 'POST' or not form.is_valid():
        return render_form(form)
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('index')


class PostCreate(CreateView):
    """
    Just as memo.
    Can use form_class or ( fields = '__all__' & model = Post)
    """

    form_class = PostForm
    template_name = 'new_post.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        return redirect(self.success_url)


class PostEdit(UpdateView):
    """
        Just as memo.
        Need to use pk or slug in url
        Another way is to replace dispatch to:
            def get_queryset(self):
                queryset = super(PostEdit, self).get_queryset()
                queryset = queryset.filter(author=self.request.user)
                return queryset
    """

    model = Post
    form_class = PostForm
    template_name = 'new_post.html'
    success_url = reverse_lazy('post')

    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        if not (self.get_object().author == request.user):
            raise PermissionDenied
        return handler


class PostEditMix(PostEditChecker):
    """
        Just as memo.
        Using UserPassesTestMixin for user permission to edit
    """

    model = Post
    form_class = PostForm
    template_name = 'new_post.html'


class IndexView(ListView):
    """
        Just as memo.
        There will be page_obj variable in template. We can iterate page itself
        but page_obj is instance of Page and we'd use it in pagination block
    """

    model = Post
    template_name = 'index.html'
    paginate_by = 10
    context_object_name = 'page'
    queryset = Post.objects.select_related('author').all()
