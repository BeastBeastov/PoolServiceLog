from datetime import datetime

from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from multiselectfield import MultiSelectField
from modules.services.utils import unique_slugify

WORK_CHOICES = (
    ('Уборка бассейна ручным водным пылесосом', 'Уборка бассейна ручным водным пылесосом'),
    ('Промывка фильтра', 'Промывка фильтра'),
    ('Уборка бассейна роботом-пылесосом', 'Уборка бассейна роботом-пылесосом'),
    ('Чистка стен щёткой', 'Чистка стен щёткой'),
    ('Долив свежей воды', 'Долив свежей воды'),
    ('Чистка ватерлинии', 'Чистка ватерлинии'),
)

UNITS_CHOICES=[
    ('таб. по 200 гр.', 'таб. по 200 гр.'),
    ('таб. по 20 гр.', 'таб. по 20 гр.'),
    ('таб. по 250 гр.', 'таб. по 250 гр.'),
    ('гр', 'гр'),
    ('кг', 'кг'),
    ('л', 'л'),
    ('мл', 'мл'),
    ('картридж', 'картридж')
]


class ReagentName(models.Model):
    class Meta:
        verbose_name = 'Товарное наименование реагента'
        verbose_name_plural = 'Каталог реагентов'

    article = models.CharField(max_length=20, verbose_name='Артикул', blank=True)
    title = models.CharField(max_length=255, verbose_name='Товарное наименование')
    units = models.CharField(max_length=50, choices=UNITS_CHOICES, verbose_name='Единицы измерения')
    per_unit = models.FloatField(max_length=5, verbose_name='Вес на единицу товара в кг')

    def __str__(self):
        return f'{self.title} в {self.units}'


class Reagent(models.Model):
    class Meta:
        verbose_name = 'Реагенты добавленные во время сервиса'
        verbose_name_plural = 'Добавленные реагенты'

    reagent = models.ForeignKey(ReagentName, null=True, on_delete=models.PROTECT, verbose_name='Реагент')
    quantity = models.FloatField(max_length=5, verbose_name='Количество')
    poolservice = models.ForeignKey('PoolService', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.reagent.title} - {self.get_quantity()} {self.reagent.units}'

    def get_quantity(self):
        return int(self.quantity) if int(self.quantity) == self.quantity else self.quantity


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
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", default="photos/pooldefault.png", verbose_name="Фото")
    author = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Бассейн"
        verbose_name_plural = "Бассейны на обслуживании"
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)
        """
        Изменение размера фото перед сохранением
        """
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width >300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.photo.path)

    def get_absolute_url(self):
        return reverse('pool_show', kwargs={'pool_slug':self.slug})


class PoolService(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    pool = models.ForeignKey('Pool', default=0, on_delete=models.PROTECT, related_name="services", verbose_name="Бассейн")
    time_create = models.DateTimeField(verbose_name="Время создания")
    date_update = models.DateField(auto_now=True, verbose_name="Дата изменения")
    PH = models.FloatField(max_length=4, verbose_name="Ph", null=True, blank=True)
    RX = models.IntegerField(verbose_name="Rx", null=True, blank=True)
    CL = models.FloatField(max_length=4, verbose_name="Cl", null=True, blank=True)
    T = models.FloatField(max_length=4, verbose_name="Т°C", null=True, blank=True)
    water_cond = models.CharField(max_length=50, verbose_name="Состояние воды", blank=True)
    reagents = models.TextField(max_length=1000, verbose_name="Добавленные реагенты", blank=True)
    works = MultiSelectField(choices=WORK_CHOICES, blank=True, max_choices=6, max_length=1000, verbose_name="Сервисные работы")
    fixworks = models.TextField(max_length=1000, verbose_name="Ремонтные работы", blank=True)
    comment = models.TextField(max_length=1000, verbose_name="Свободный комментарий", blank=True)
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    author = models.ForeignKey(User, default=0, verbose_name='Исполнитель', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Сервисный выезд"
        verbose_name_plural = "Журнал сервисных операций"
        ordering = ['-time_create', 'title']

    def __str__(self):
        return f'{self.title} - {self.time_create.date()}'

    def get_absolute_url(self):
        return reverse('log', kwargs={'pk':self.pk})

    def get_previous(self):
        previos = PoolService.objects.filter(time_create__lt=self.time_create).order_by('-time_create').first()
        return previos

    def get_next(self):
        next = PoolService.objects.filter(time_create__gt=self.time_create).order_by('-time_create').last()
        return next

    def save(self, *args, **kwargs):
        if self.time_create is None:
            self.time_create = timezone.now() + timezone.timedelta(hours=3)
        super().save(*args, **kwargs)

    def delta_date(self):
        delta = (datetime.today().date() - self.time_create.date()).days
        weeks = delta // 7
        days = delta % 7
        if days == 1:
            d = 'день'
        elif days > 1 and days < 5:
            d = 'дня'
        elif days > 4:
            d = 'дней'

        if weeks > 10 and weeks < 20:
            w = 'недель'
        elif weeks % 10 == 1:
            w = 'неделя'
        elif weeks % 10 > 1 and weeks % 10 < 5:
            w = 'недели'
        else:
            w = 'недель'

        if weeks < 1 and days < 1:
            result = ' ~ Сегодня'
        elif weeks < 1:
            result = f' ~ {days} {d}'
        elif days < 1:
            result = f' ~ {weeks} {w}'
        else:
            result = f' ~ {weeks} {w} {days} {d}'
        return result