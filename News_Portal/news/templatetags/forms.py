from django.forms import ModelForm
from .models import Post


# Создаём модельную форму
class PostForm(ModelForm):
    # в класс мета, как обычно, надо написать модель, по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.

    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'post_title',
            'post_text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('post_title')
        text = cleaned_data.get('post_text')
        if text == title:
            raise ValidationError(
                {'text': 'Текст публикации не должен быть идентичен её названию'}
            )
        return cleaned_data















