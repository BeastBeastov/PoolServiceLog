from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Pool(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название", db_index=True)
    owner = models.CharField(max_length=255, verbose_name="Владелец")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    email = models.EmailField()
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True)
    place = models.TextField(max_length=255, verbose_name="Место расположения", blank=True)
    volume = models.IntegerField(verbose_name="Объём", null=True, blank=True)
    year_create = models.CharField(max_length=10, verbose_name="Год постройки", blank=True)
    equipment = models.TextField(max_length=1000, verbose_name="Комплектация", blank=True)
    description = models.TextField(max_length=1000, verbose_name="Описание", blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", blank=True)
    author = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Бассейн"
        verbose_name_plural = "Бассейны"
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pool_show', kwargs={'pool_slug':self.slug})


class PoolService(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    pool = models.ForeignKey('Pool', default=0, on_delete=models.PROTECT, verbose_name="Бассейн")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    date_update = models.DateField(auto_now=True, verbose_name="Дата изменения")
    PH = models.FloatField(max_length=4, verbose_name="Ph", null=True, blank=True)
    RX = models.IntegerField(verbose_name="Rx", null=True, blank=True)
    CL = models.FloatField(max_length=4, verbose_name="Cl", null=True, blank=True)
    T = models.FloatField(max_length=4, verbose_name="Т°C", null=True, blank=True)
    water_cond = models.CharField(max_length=50, verbose_name="Состояние воды", blank=True)
    reagents = models.TextField(max_length=1000, verbose_name="Добавленные реагенты", blank=True)
    works = models.TextField(max_length=1000, default=None, verbose_name="Выполненные работы", blank=True)
    comment = models.TextField(max_length=1000, verbose_name="Свободный комментарий", blank=True)
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    author = models.ForeignKey(User, default=0, verbose_name='Исполнитель', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Сервисный выезд"
        verbose_name_plural = "Журнал сервисных операций"
        ordering = ['-time_create', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('log', kwargs={'pk':self.pk})

    def get_previous(self):
        previos = PoolService.objects.filter(time_create__lt=self.time_create).order_by('-time_create').first()
        return previos

    def get_next(self):
        next = PoolService.objects.filter(time_create__gt=self.time_create).order_by('-time_create').last()
        return next



"""
class Reagent(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    units = models.CharField(max_length=25, null=True, verbose_name="Единицы измерения", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Реагент"
        verbose_name_plural = "Реагенты"
        ordering = ['title']
"""


class ServiceWork(models.Model):
    # WORKS_CHOICES = (('1', 'Уборка ручным водным пылесосом'),
    #                  ('2', 'Чистка ватерлинии'),
    #                  ('3', 'Уборка роботом-пылесосом'),
    #                  ('4', 'Промывка фильтра'),
    #                  ('5', 'Чистка стен щеткой'),
    #                  ('6', 'Долив свежей воды'))
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Сервисная операция"
        verbose_name_plural = "Сервисные работы"
        ordering = ['title']


