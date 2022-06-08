from django.contrib.auth import get_user_model
from django.db import models
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail import delete as delete_thumbnail


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'

    def __str__(self):
        return self.title

    @property
    def last_dozen_posts(self):
        return self.posts.all()[:12]


class Post(models.Model):
    text = models.TextField(verbose_name='Текст сообщения')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации', db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True,
        verbose_name='Сообщество',
    )
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
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
        verbose_name='Пост',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created']

    def __str__(self):
        return f'Коммент #{self.id}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписант',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ['user', 'author']

    def __str__(self):
        return f'Подписка {self.user} на {self.author}'

