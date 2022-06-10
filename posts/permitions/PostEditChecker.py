from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView


class PostEditChecker(UserPassesTestMixin, UpdateView):
    raise_exception = False

    def get_success_url(self):
        return reverse_lazy(
            'post',
            kwargs={
                'post_id': self.get_object().id,
                'username': self.get_object().author.username,
            },
        )

    def handle_no_permission(self):
        return redirect(
            reverse_lazy(
                'post',
                kwargs={
                    'post_id': self.get_object().id,
                    'username': self.get_object().author.username,
                },
            )
        )

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
