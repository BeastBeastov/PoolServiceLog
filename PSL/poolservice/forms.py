from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from captcha.fields import CaptchaField

from .utils import *

WORK_CHOICES = (
    ('Уборка бассейна ручным водным пылесосом', 'Уборка бассейна ручным водным пылесосом'),
    ('Промывка фильтра', 'Промывка фильтра'),
    ('Уборка бассейна роботом-пылесосом', 'Уборка бассейна роботом-пылесосом'),
    ('Чистка стен щёткой', 'Чистка стен щёткой'),
    ('Долив свежей воды', 'Долив свежей воды'),
    ('Чистка ватерлинии', 'Чистка ватерлинии'),
)


class NewPoolLogForm(forms.ModelForm):
    queryset = Pool.objects.none()
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pool'].empty_label = "Объект не выбран"
        if user.is_staff:
            self.fields['pool'].queryset = Pool.objects.all()
            self.queryset = self.fields['pool'].queryset
        else:
            self.fields['pool'].queryset = Pool.objects.filter(author=user)
            self.queryset = self.fields['pool'].queryset

    works = forms.MultipleChoiceField(label='Сервисные работы', required=False,
                                      widget=forms.CheckboxSelectMultiple(
                                          attrs={'type':'checkbox'}
                                      ), choices=WORK_CHOICES)

    title = forms.CharField(label='Заголовок',
                            widget=forms.TextInput(
                                attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'например: Выезд по заявке'}))
    pool = forms.ModelChoiceField(label='Объект', queryset=queryset,
                                  widget=forms.Select(
                                      attrs={'class': 'form-select', 'type': 'text'}
                                  ))
    PH = forms.FloatField(label='Ph', required=False,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control form-control-sm',}))
    RX = forms.IntegerField(label='Redox', required=False,
                         widget=forms.TextInput(
                             attrs={'class': 'form-control form-control-sm', }))
    CL = forms.FloatField(label='Cl', required=False,
                         widget=forms.TextInput(
                             attrs={'class': 'form-control form-control-sm', }))
    T = forms.FloatField(label='Т°C', required=False,
                         widget=forms.TextInput(
                             attrs={'class': 'form-control form-control-sm', }))
    water_cond = forms.CharField(label='Состояние воды', required=False,
                        widget=forms.TextInput(
                            attrs={'class': 'form-control form-control-sm', 'placeholder': 'например: Чистая, прозрачная' }))
    reagents = forms.CharField(label='Добавленные реагенты', required=False,
                                 widget=forms.Textarea(
                                     attrs={'class': 'form-control form-control-sm', 'rows':'4',
                                            'placeholder': 'Эти данные не попадут в статистику.\nДля добавления реагентов восползутейсь кнопкой "Реагенты" на странице подробного описания сервисной записи.'}))
    fixworks = forms.CharField(label='Ремонтные работы', required=False,
                              widget=forms.Textarea(
                                  attrs={'class': 'form-control form-control-sm', 'rows': '3',
                                         'placeholder': 'например: Устранили протечку в районе шарового крана'}))
    comment = forms.CharField(label='Свободный комментарий', required=False,
                               widget=forms.Textarea(
                                   attrs={'class': 'form-control form-control-sm', 'rows': '3',
                                          'placeholder': 'например: Сильный ветер насыпал листвы с деревьев'}))

    class Meta:
        model = PoolService
        fields = ['title','pool','PH','RX','CL','T','water_cond','reagents','works','fixworks','comment']


class NewPoolForm(DataMixinForm, forms.ModelForm):
    title = forms.CharField(label='Название объекта',
                               widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Малиновка 11х5.5м'}))
    slug = forms.SlugField(label='URL',
                               widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'malinovka-11x5_5m'}))
    place = forms.CharField(label='Место расположения', required=False,
                               widget=forms.Textarea(
                                   attrs={'class': 'form-control form-control-sm', 'rows': '3',
                  'placeholder': 'например: Московская область, Ленинский р-н, пос.Володарского, ул.Гарибальди, д.14'}))
    equipment = forms.CharField(label='Комплектация', required=False,
                               widget=forms.Textarea(
                                   attrs={'class': 'form-control form-control-sm', 'rows': '3',
                         'placeholder': 'например: Чаша: монолит-бетон, переливной лоток\nОблицовка: мозаика, мрамор.'}))
    description = forms.CharField(label='Описание', required=False,
                                widget=forms.Textarea(
                                    attrs={'class': 'form-control form-control-sm', 'rows': '3',
                         'placeholder': 'например: Уличный бассейн с павильоном и подогревом, сезонного использования'}))

    class Meta:
        model = Pool
        fields = ['title','slug','owner','email','phone','place','volume',
                  'year_create','equipment','description','photo']


class ReagentNameForm(DataMixinForm, forms.ModelForm):
    class Meta:
        model = ReagentName
        fields = '__all__'


class ReagentForm(DataMixinForm, forms.ModelForm):
    queryset = ReagentName.objects.all()
    reagent = forms.ModelChoiceField(label='Добавить реагент', queryset=queryset,
                                  widget=forms.Select())
    quantity = forms.FloatField(label='Количество')

    class Meta:
        model = Reagent
        fields = ['reagent','quantity']


class RegisterUserForm(DataMixinForm, UserCreationForm):
    username = forms.CharField(label='Логин',widget=forms.TextInput(attrs={'class':'form-input','placeholder':'username'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input','placeholder':'Иван'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input','placeholder':'Иванов'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-input','placeholder':'name@example.com'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']


class LoginUserForm(DataMixinForm, AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(DataMixinForm, forms.Form):
    name = forms.CharField(label='Имя', max_length=255, widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    content = forms.CharField(label='Комментарий', widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}))
    captcha = CaptchaField()