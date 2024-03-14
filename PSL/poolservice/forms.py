from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from captcha.fields import CaptchaField

from .utils import *

WORK_CHOICES = (
    ('Ничего', 'Ничего'),
    ('Уборка бассейна ручным водным пылесосом', 'Уборка бассейна ручным водным пылесосом'),
    ('Промывка фильтра', 'Промывка фильтра'),
    ('Уборка бассейна роботом-пылесосом', 'Уборка бассейна роботом-пылесосом'),
    ('Чистка стен щёткой', 'Чистка стен щёткой'),
    ('Долив свежей воды', 'Долив свежей воды'),
    ('Чистка ватерлинии', 'Чистка ватерлинии'),
)


class NewPoolLogForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pool'].empty_label = "Объект не выбран"
        self.fields['works'].empty_label = "Ничего"
        if user.is_staff:
            self.fields['pool'].queryset = Pool.objects.all()
        else:
            self.fields['pool'].queryset = Pool.objects.filter(author=user)

    works = forms.MultipleChoiceField(label='Выполненые работы', widget=forms.CheckboxSelectMultiple(),
                                          choices=WORK_CHOICES)

    class Meta:
        model = PoolService
        fields = ['title','pool','PH','RX','CL','T','water_cond','reagents','works','comment']


class NewPoolForm(DataMixinForm, forms.ModelForm):
    title = forms.CharField(label='Название объекта',
                               widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Малиновка 11х5.5м'}))
    slug = forms.SlugField(label='URL',
                               widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'malinovka-11x5_5m'}))

    class Meta:
        model = Pool
        fields = ['title','slug','owner','email','phone','place','volume','year_create','equipment','description']


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