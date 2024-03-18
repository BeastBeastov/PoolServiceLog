from django.forms import model_to_dict
from rest_framework import generics

from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import *
from .models import *
from .serializers import PoolServiceSerializer
from .utils import *


# Функция предстваления страницы index, аналогично классу представленному ниже
# def index(request):
#     logs = PoolService.objects.all().order_by('-date_create')
#     pools = Pool.objects.all()
#     context = {
#         'logs': logs,
#         'pools': pools,
#         'menu': menu,
#         'pool_selected': 0,
#         'title': 'Главная страница',
#     }
#     return render(request,'poolservice/index.html', context=context)


class PoolServiceView(LoginRequiredMixin, DataMixin, ListView):
    paginate_by = 10
    model = PoolService
    template_name = 'poolservice/index.html'
    context_object_name = 'logs'
    login_url = reverse_lazy('login')  # Сдесь нужно поменять путь когда будет работать страница авторизации
    raise_exception = True  # Ошибка 403 Доступ запрещен

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['queryset'] = self.get_queryset()
        context['menu'] = menu
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        queryset = PoolService.objects.filter(is_published=True).select_related('pool')
        if not self.request.user.is_staff:
            queryset1 = queryset.filter(author=self.request.user)
            queryset2 = queryset.none()
            pools = Pool.objects.filter(author=self.request.user)
            for p in pools:
                queryset2 |= queryset.filter(pool=p)
            queryset = queryset1|queryset2
        elif not self.request.user.is_authenticated:
            queryset = PoolService.objects.none()
        return queryset


class FormValidationError:
    pass


# def new_log(request):
#     if request.method == 'POST':
#         form = NewPoolLogForm(data=request.POST, user=request.user)
#         try:
#             form.instance.author = request.user
#             print(form.is_valid())
#             form.save()
#             return redirect('home')
#         except FormValidationError as e:
#             form.add_error("Ошибка: {}".format(e))
#     else:
#         form = NewPoolLogForm(request.user)
#     context = {
#         'form': form,
#         'menu': menu,
#         'title': 'Добавить новую запись в журнал',
#     }
#     return render(request, 'poolservice/new_log.html', context=context)


class NewLogView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = NewPoolLogForm
    template_name = 'poolservice/new_log.html'
    login_url = reverse_lazy('login') # Сдесь нужно поменять путь когда будет работать страница авторизации
    raise_exception = True # Ошибка 403 Доступ запрещен

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Новая запись')
        return dict(list(context.items()) + list(c_def.items()))

    def get(self, request):
        form = NewPoolLogForm(user=request.user)
        context = {
            'appmenu': appmenu,
            'form': form,
            'menu': menu,  # предполагается, что переменная menu определена
            'title': 'Добавить новую запись в журнал',
        }
        return render(request, 'poolservice/new_log.html', context=context)

    def post(self, request):
        form = NewPoolLogForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('home')
        else:
            context = {
                'appmenu': appmenu,
                'form': form,
                'menu': menu,
                'title': 'Добавить новую запись в журнал',
            }
            return render(request, 'poolservice/new_log.html', context=context)

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     form.save()
    #     return super().form_valid(form)


class NewPoolView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = NewPoolForm
    template_name = 'poolservice/new_pool.html'
    login_url = reverse_lazy('login')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Новый бассейн')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


# @login_required
# def new_pool(request):
#     if request.method == 'POST':
#         form = NewPoolForm(request.POST)
#         if form.is_valid:
#             try:
#                 form.author = request.user
#                 form.save()
#                 return redirect('home')
#             except:
#                 form.add_error("Ошибка")
#     else:
#         form = NewPoolForm()
#     context = {
#         'form': form,
#         'menu': menu,
#         'title': 'Добавить новый бассейн',
#     }
#     return render(request, 'poolservice/new_pool.html', context=context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'poolservice/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'poolservice/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def update_log(request, log_id):
    log = PoolService.objects.get(pk=log_id)
    form = NewPoolLogForm(instance=log, user=request.user)
    context = {
        'appmenu': appmenu,
        'form': form,
        'log': log,
        'title': 'Изменить ' + str(log.title) + ' ' + str(log.pool) + ' ' + str(log.time_create.date()),
        'menu': menu,
    }
    if request.method == "POST":
        form = NewPoolLogForm(data=request.POST, instance=log, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = "Форма заполнена не верно"
    return render(request, 'poolservice/update.html', context=context)


# @login_required # Для ограничения доступа используется специальный декоратор
# def delete_log(request, log_id):
#     log = PoolService.objects.get(pk=log_id)
#     log.delete()
#     return redirect('home')

class DeleteLogView(LoginRequiredMixin, DeleteView):
    model = PoolService
    template_name = 'poolservice/log_delete.html'
    context_object_name = 'log'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление'
        context['pk_url_kwarg'] = 'pk'
        return context


# @login_required
# def show_log(request, pk):
#     log = get_object_or_404(PoolService, pk=pk)
#
#     context = {
#         'pk_url_kwarg': pk,
#         'log': log,
#         'title': log.title,
#         'menu': menu,
#     }
#     return render(request, 'poolservice/log.html', context=context)

# Функция представления для примера, аналогичная нижеописанному классу представления
# def pool_logs(request, pool_id):
#     logs = PoolService.objects.filter(pool_id=pool_id).order_by('date_create')
#     pools = Pool.objects.all()
#     context = {
#         'logs': logs,
#         'pools': pools,
#         'menu': menu,
#         'pool_selected': pool_id,
#         'title': 'Главная страница',
#     }
#     return render(request, 'poolservice/index.html', context=context)


class PoolLogsView(LoginRequiredMixin, DataMixin, ListView):
    # Оставил этот класс без использования DataMixin, чтобы наглядно видеть и понимать разницу
    paginate_by = 5
    model = PoolService
    template_name = 'poolservice/index.html'
    context_object_name = 'logs'
    allow_empty = False # Исключает вывод ошибок если список выбора по объекту пустой

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['queryset'] = self.get_queryset()
        # context['menu'] = menu
        context['title'] = 'Сервис ' + str(context['logs'][0].pool)
        context['pool_selected'] = context['logs'][0].pool_id
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return PoolService.objects.filter(pool__id=self.kwargs['pool_id'],  is_published=True)


class LogView(LoginRequiredMixin, DataMixin, DetailView):
    model = PoolService
    template_name = 'poolservice/log.html'
    context_object_name = 'log'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk_url_kwarg'] = 'pk'
        context['works'] = context['log'].works
        context['object_list'] = PoolLogsView.queryset
        c_def = self.get_user_context(title=str(context['log'].title))
        return dict(list(context.items()) + list(c_def.items()))


# Функция представления для примера, аналогичная нижеописанному классу представления
# def pool_show(request, pool_slug):
#     pool = get_object_or_404(Pool, slug=pool_slug)
#
#     context = {
#         'title': pool.title,
#         'menu': menu,
#         'pool': pool,
#     }
#     return render(request, 'poolservice/pool_show.html', context=context)


class PoolView(DataMixin, DetailView):
    model = Pool
    template_name = 'poolservice/pool_show.html'
    slug_url_kwarg = 'pool_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = PoolService.objects.filter(pool=context['pool'])[:20]
        c_def = self.get_user_context(title='Бассейн ' + str(context['pool']))
        return dict(list(context.items()) + list(c_def.items()))


def pool_update(request, pool_slug):
    pool = get_object_or_404(Pool, slug=pool_slug)
    form = NewPoolForm(instance=pool)

    context = {
        'appmenu': appmenu,
        'form': form,
        'log': pool,
        'title': 'Изменить ' + str(pool.title),
        'menu': menu,
    }
    if request.method == "POST":
        form = NewPoolForm(data=request.POST, instance=pool)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = "Форма заполнена не верно"
    return render(request, 'poolservice/pool_update.html', context=context)


class DeletePoolView(DeleteView):
    model = Pool
    template_name = 'poolservice/pool_delete.html'
    context_object_name = 'pool'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление'
        context['pk_url_kwarg'] = 'pk'
        return context


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'poolservice/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


def admin_view(request):
    return redirect('admin')


def development(request):
    context = {
        'menu': menu,
        'title': 'Разработка PoolService',
    }
    return render(request, 'poolservice/development.html', context=context)


def main(request):
    context = {
        'title': 'Начало',
    }
    return render(request, 'poolservice/main.html', context=context)


def about(request):
    context = {
        'menu': menu,
        'title': 'О сайте',
    }
    return render(request,'poolservice/about.html', context=context)


def pages(request, page):
    return HttpResponse(f"<h1>Вывод по страницам</h1><p>{page}</p>")


def archive(request, year):
    if int(year) > 2024:
        raise Http404()
    elif int(year) < 1950:
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Вывод по годам</h1><p>{year}</p>")



def pageNotFound(request, exception):
    return HttpResponseNotFound(f"<h1>Страница не найдена</h1>")


class PoolServiceAPIView(APIView):
    def get(self, request):
        ps = PoolService.objects.all()
        return Response({'logs':PoolServiceSerializer(ps, many=True).data})

    def post(self, request):
        serializer = PoolServiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'log': serializer.data})
        # log_new = PoolService.objects.create(
        #     title=request.data['title'],
        #     pool_id=0,
        #     PH=request.data['PH'],
        #     RX=request.data['RX'],
        #     CL=request.data['CL'],
        #     T=request.data['T'],
        #     author_id=0
        # )
        # return Response({'log': PoolServiceSerializer(log_new).data})

# class PoolServiceAPIView(generics.ListAPIView):
#     queryset = PoolService.objects.all()
#     serializer_class = PoolServiceSerializer
