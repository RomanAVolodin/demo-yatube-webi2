from django import forms
from .models import Post, Comment
from .templatetags.pluralize import rupluralize

MIN_MESSAGE_LENGTH = 5


def validate_length(value):
    length = len(value)
    if length < MIN_MESSAGE_LENGTH:
        simbol_text = rupluralize(length, 'символ,символа,символов')
        raise forms.ValidationError(
            f'Длина сообщения всего {length} {simbol_text}, '
            f'что меньше минимального значения: {MIN_MESSAGE_LENGTH}',
            code='invalid',
        )


class PostForm(forms.ModelForm):
    """
    Slightly change text field for placeholder and length validation.
    Field group used as is in model
    """

    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Укажите текст сообщения'}
        ),
        label='Текст сообщения',
        validators=[validate_length],
        error_messages={'required': 'Текст сообщения - обязателен'},
        strip=True,
    )

    image = forms.ImageField(required=False, label='Файл изображения')

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        help_texts = {'group': 'Поле не обязательно, но желательно'}


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Укажите текст комментария', 'rows': 4}
        ),
        label='Комментарий',
        validators=[validate_length],
        error_messages={'required': 'Текст комментария - обязателен'},
        strip=True,
    )

    class Meta:
        model = Comment
        fields = ('text',)
        help_texts = {'text': 'Оставьте Ваш комментарий'}
