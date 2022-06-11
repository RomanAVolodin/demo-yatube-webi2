from django.contrib.auth import get_user_model
from django.db import models
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail import delete as delete_thumbnail
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Community')
        verbose_name_plural = _('Communities')

    def __str__(self):
        return self.title

    @property
    def last_dozen_posts(self):
        return self.posts.all()[:12]


class ImagedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(image__isnull=False)


class Post(models.Model):
    text = models.TextField(verbose_name=_('Post text'))
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Publication date'), db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('Author'),
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True,
        verbose_name=_('Community'),
    )
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name=_('Image'))

    # imaged_objects = ImagedManager()

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ['-pub_date']

    @property
    def thumbnail(self):
        if self.image:
            return get_thumbnail(
                self.image, '960x339', crop='center', upscale=True
            )
        return None

    def clear_thumbnails(self):
        if self.image:
            delete_thumbnail(self.image)

    def delete(self, *args, **kwargs):
        self.clear_thumbnails()
        super(Post, self).delete(*args, **kwargs)

    def __str__(self):
        return f'Пост #{self.id}'


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Comment'),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Author'),
    )
    text = models.TextField(verbose_name=_('Comment text'))
    created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date')
    )

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['-created']

    def __str__(self):
        return f'#{self.id}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name=_('Follower'),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name=_('Author'),
    )

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
        unique_together = ['user', 'author']

    def __str__(self):
        return f'{self.user} на {self.author}'

