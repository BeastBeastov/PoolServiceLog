from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from blog.utils import TITLE_CHOICES


class Post(models.Model):
    author = models.ForeignKey(User, verbose_name='Автор сообщения', on_delete=models.PROTECT)
    status = models.CharField(max_length=1, choices=TITLE_CHOICES, verbose_name="Статус сообщения")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(max_length=1000, verbose_name="Свободный комментарий", blank=True)

    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Изменено")

    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Все сообщения"
        ordering = ['-time_create', 'status','title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_post', kwargs={'pk':self.pk})

    def get_answers(self):
        return Answer.objects.filter(post=self)

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class Answer(models.Model):
    author = models.ForeignKey(User, verbose_name='Автор ответа', on_delete=models.PROTECT)
    content = models.TextField(max_length=1000, verbose_name="Свободный комментарий", blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы на сообщения разработки"
        ordering = ['-time_create', 'post']

    def answer_default():
        return {Post.id}

    post = models.ForeignKey(Post, default=answer_default, verbose_name='К сообщению', on_delete=models.CASCADE)

    def __str__(self):
        """String for representing the comment object."""
        return '%s - %s - %s' % (self.post.content, self.author, self.time_create)

    def get_absolute_url(self):
        return reverse('detail_post', args=[str(self.post.id)])





