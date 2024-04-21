from datetime import datetime, timedelta, time, date

from openpyxl.workbook import Workbook

from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from pytz import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import *
from .serializers import PoolServiceSerializer
from .utils import *


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
        if context['logs']:
            context['rs_book'] = reagent_statistics(context['logs'])[1]
        c_def = self.get_user_context(title='Журнал PH - Главная страница')
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


class NewLogView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = NewPoolLogForm
    template_name = 'poolservice/new_log.html'
    login_url = reverse_lazy('login') # Сдесь нужно поменять путь когда будет работать страница авторизации
    raise_exception = True # Ошибка 403 Доступ запрещен

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Журнал PH - Новая запись')
        return dict(list(context.items()) + list(c_def.items()))

    def get(self, request):
        form = NewPoolLogForm(user=request.user)
        context = {
            'form': form,
            'menu': menu+appmenu,  # предполагается, что переменная menu определена
            'title': 'Журнал PH - Новая запись',
        }
        return render(request, 'poolservice/new_log.html', context=context)

    def post(self, request):
        form = NewPoolLogForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('log', form.instance.pk)
        else:
            context = {
                'form': form,
                'menu': menu+appmenu,
                'title': 'Журнал PH - Новая запись',
            }
            return render(request, 'poolservice/new_log.html', context=context)


class NewPoolView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = NewPoolForm
    template_name = 'poolservice/new_pool.html'
    login_url = reverse_lazy('login')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Журнал PH - Новый бассейн')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.FILES = self.request.FILES
        form.save()
        return super().form_valid(form)

    def get(self, request):
        form = NewPoolForm(initial={
            'owner':self.request.user.first_name + ' ' + self.request.user.last_name,
            'email':self.request.user.email
        })
        context = {
            'form': form,
            'menu': menu+appmenu,
            'title': 'Журнал PH - Новый бассейн',
        }
        return render(request, 'poolservice/new_pool.html', context=context)


@login_required
def update_log(request, log_id):
    log = PoolService.objects.get(pk=log_id)
    form = NewPoolLogForm(instance=log, user=request.user)
    context = {
        'form': form,
        'log': log,
        'title': 'Журнал PH - Изменить ' + str(log.title) + ' ' + str(log.pool) + ' ' + str(log.time_create.date()),
        'menu': menu + appmenu,
    }
    if request.method == "POST":
        form = NewPoolLogForm(data=request.POST, instance=log, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('log', log_id)
        else:
            error = "Форма заполнена не верно"
    return render(request, 'poolservice/update.html', context=context)


class DeleteLogView(LoginRequiredMixin, DeleteView):
    model = PoolService
    template_name = 'poolservice/log_delete.html'
    context_object_name = 'log'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Журнал PH - Удаление записи'
        context['pk_url_kwarg'] = 'pk'
        return context


class PoolLogsView(LoginRequiredMixin, DataMixin, ListView):
    paginate_by = 5
    model = PoolService
    template_name = 'poolservice/index.html'
    context_object_name = 'logs'
    allow_empty = False # Исключает вывод ошибок если список выбора по объекту пустой

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['queryset'] = self.get_queryset()
        context['rs_book'] = reagent_statistics(context['logs'])[1]
        context['title'] = 'Журнал PH - Все записи по ' + str(context['logs'][0].pool)
        context['pool_selected'] = context['logs'][0].pool_id
        c_def = self.get_user_context(title='Журнал PH - Все записи по ' + str(context['logs'][0].pool))
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
        context['rs'] = Reagent.objects.filter(poolservice=context['log'])
        c_def = self.get_user_context(title=str(context['log'].title))
        return dict(list(context.items()) + list(c_def.items()))


class PoolView(DataMixin, DetailView):
    model = Pool
    template_name = 'poolservice/pool_show.html'
    slug_url_kwarg = 'pool_slug'
    current_year = datetime.now().year
    start_date = datetime(current_year,1,1) + timedelta(hours=3)

    def get(self, request, pool_slug):
        pool = Pool.objects.get(slug=pool_slug)
        context = {
            'pool': pool,
            'menu': menu+appmenu,
            'title': 'Журнал PH - ' + pool.title
        }
        if request.GET.get('start_date'):
            self.start_date = request.GET.get('start_date')
        queryset = PoolService.objects.filter(pool=pool.pk)
        date_book = list()
        for log in queryset:
            date_book.append(log.time_create)
        context['date_book'] = date_book
        queryset = queryset.filter(time_create__gte=self.start_date)
        first = 0
        for log in queryset:
            first = log
        if first:
            context['first_log_time'] = first.time_create
        context['logs'] = queryset
        if queryset:
            context['reagents_book'], context['rs_book'] = reagent_statistics(queryset)
        total = queryset.count()
        ph_count = queryset.filter(PH__gte=5).count()
        rx_count = queryset.filter(RX__gte=300).count()
        cl_count = queryset.filter(CL__gte=0.05).count()
        t_count = queryset.filter(T__gte=5).count()
        if ph_count >= total / 2: context['show_ph'] = True
        if rx_count >= total / 2: context['show_rx'] = True
        if cl_count >= total / 2: context['show_cl'] = True
        if t_count >= total / 2: context['show_t'] = True
        return render(request, 'poolservice/pool_show.html'.format(self.start_date), context=context)


def pool_update(request, pool_slug):
    pool = get_object_or_404(Pool, slug=pool_slug)
    form = NewPoolForm(instance=pool)

    context = {
        'form': form,
        'log': pool,
        'title': 'Журнал PH - Изменить ' + str(pool.title),
        'menu': menu+appmenu,
    }
    if request.method == "POST":
        form = NewPoolForm(data=request.POST, instance=pool, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pool_show', pool_slug)
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
        context['title'] = 'Журнал PH - Удаление объекта'
        context['pk_url_kwarg'] = 'pk'
        return context


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'poolservice/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Журнал PH - Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        return redirect('home')


class CreateReagentNameView(DataMixin, CreateView):
    form_class = ReagentNameForm
    template_name = 'poolservice/add_reagent_name.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Журнал PH - Новый реагент')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AddReagentView(DataMixin, CreateView):
    model = ReagentForm
    template_name = 'poolservice/add_reagent_log.html'
    current_pk = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Журнал PH - Добавить реагент'
        return context

    def get(self, request, pk):
        form = ReagentForm()
        self.current_pk = pk
        context = {
            'log': PoolService.objects.get(pk=pk),
            'rs': Reagent.objects.filter(poolservice=pk),
            'pk': pk,
            'form': form,
            'menu': menu+appmenu,
            'title': 'Журнал PH - Добавить реагент',
        }
        return render(request, 'poolservice/add_reagent_log.html', context=context)

    def post(self, request, pk):
        form = ReagentForm(data=request.POST)
        if form.is_valid():
            reagent = form.cleaned_data.get('reagent')
            quantity = form.cleaned_data.get("quantity")
            ps = PoolService.objects.get(pk=pk)
            Reagent.objects.create(poolservice=ps, reagent=reagent, quantity=quantity)
            return redirect(request.META.get('HTTP_REFERER'))
            # return redirect(ps.get_absolute_url())
        else:
            context = {
                'log': PoolService.objects.get(pk=pk),
                'rs': Reagent.objects.filter(poolservice=pk),
                'form': form,
                'menu': menu+appmenu,
                'title': 'Журнал PH - Добавить реагент',
            }
            return render(request, 'poolservice/add_reagent_log.html', context=context)


def delete_reagent_log(request, pk):
    reagent_log = Reagent.objects.get(pk=pk)
    reagent_log.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def admin_view(request):
    return redirect('admin')


def main(request):
    context = {
        'title': 'Журнал PH',
    }
    return render(request, 'poolservice/main.html', context=context)


def about(request):
    context = {
        'menu': menu+appmenu,
        'title': 'О проекте "Журнал PH"',
    }
    return render(request,'poolservice/about.html', context=context)


def export_to_excel(request, pool_slug):
    pool = Pool.objects.get(slug=pool_slug)
    start_load_date = request.GET.get('start_load_date')
    end_load_date = request.GET.get('end_load_date')
    end_date = datetime.strptime(end_load_date, "%Y-%m-%d")
    end_time = time(23, 59)
    end_time = datetime.combine(end_date, end_time)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="poolservice_oreder.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Журнал сервисных операций"

    # Добавляем заголовки столбцов
    start = start_load_date
    end = end_load_date
    description = ["Журнал сервисных операций по объекту: " + pool.title + " с " + start + " по " + end]
    headers = ["Дата", "Заголовок", "Состояние воды", "Ph", "Redox", "Cl", "T",
               "Добавленные реагенты", "Сервисные работы", "Ремонтные работы", "Свободный комментарий"]
    ws.append(description)
    ws.append(headers)

    # Выбираем данные из модели
    logs = PoolService.objects.filter(pool=pool.pk)
    logs = logs.filter(time_create__gte=start_load_date)
    logs = logs.filter(time_create__lte=end_time)
    for l in logs:
        reagents = Reagent.objects.filter(poolservice=l)
        r_list = ''
        if l.PH == None: l.PH = ''
        if l.RX == None: l.RX = ''
        if l.CL == None: l.CL = ''
        if l.T == None: l.T = ''
        w_list = ''
        if l.works:
            for w in l.works:
                w_list += w + ' \n'
        if l.reagents:
            r_list += l.reagents +' \n'
        if reagents:
            for r in reagents:
                if r.quantity == int(r.quantity): r.quantity=int(r.quantity)
                r_list += r.reagent.title + ' ' + str(r.quantity) + ' ' + r.reagent.units + ' \n'
        ws.append([l.time_create.date(), l.title, l.water_cond, str(l.PH), str(l.RX), str(l.CL), str(l.T),
                   r_list, w_list, l.fixworks, l.comment])
    # Save the workbook to the HttpResponse
    wb.save(response)
    return response


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

