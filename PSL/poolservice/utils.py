# Файл хранения классов Mixin и всех обобщенных методов и классов и общеприменимых данных
from django.urls import reverse_lazy

from poolservice.models import *
import pandas as pd
import numpy as np


menu = [
         {'title':'Начало', 'url_name':'begin'},
         {'title':'Разработка', 'url_name':'blog'},
         ]

appmenu = [
         {'title':'Добавить сервис', 'url_icon':'poolservice/icons/add_service_icon.html' ,'url_name':'new_log'},
         {'title':'Новый бассейн', 'url_icon':'poolservice/icons/add_pool_icon.html', 'url_name':'new_pool'},
         {'title':'Новый реагент', 'url_icon':'poolservice/icons/add_reagent_icon.html', 'url_name':'add_reagent_name'},
         ]


# Обобщенный класс для классов представления в views.py
class DataMixin:
    login_url = reverse_lazy('login')
    raise_exception = True

    def get_user_context(self, **kwargs):
        context = kwargs
        pools = Pool.objects.all()
        user_pools = Pool.objects.filter(author=self.request.user)
        user_menu = menu.copy()
        app_menu = appmenu.copy()

        context['menu'] = user_menu + app_menu
        context['pools'] = pools
        context['user_pools'] = user_pools

        return context


class DataMixinForm:
    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'on'
            })


def reagent_statistics(queryset):
    if not queryset: return None
    reagent_set = Reagent.objects.none()
    reagents_book = dict()
    for log in queryset:
        reagent_set|=Reagent.objects.filter(poolservice=log.pk)
    for item in reagent_set:
        reagents_book[item.reagent.title] =  reagents_book.pop(item.reagent.title, 0) + item.quantity * item.reagent.per_unit
    for key, item in reagents_book.items():
        reagents_book[key] = round(item, 2)
    return reagents_book, reagent_set


def dataimport():

    def nnn(S):
        S = S.to_list()
        N = len(S)
        for i in range(N):
            L = str(S[i])
            L = L.replace('nan', '')
            S[i] = L
        S = pd.Series(np.array(S))
        return S

    def numn(S):
        S = S.to_list()
        for i in range(len(S)):
            L = str(S[i])
            L = L.replace('nan', '')
            L = L.replace(',','.')
            if L=='':
                S[i] = 0
            else:
                S[i] = float(L)
        S = pd.Series(np.array(S))
        return S


    def up_data(file):
        df = pd.read_excel(file)

        df.rename(columns={
            'Время создания': 'time_create',
            'Обьект': 'pool',
            'Владелец, Пользователь, Управляющий': 'owner',
            'Контактный телефон': 'phone',
            'Адрес электронной почты': 'email',
            'Уровень PH?': 'PH',
            'Уровень Хлора (Cl)?': 'CL',
            'Redox?': 'RX',
            'Температура воды': 'T',
            'Состояние воды': 'water_cond',
            'Что было добавлено из хим.реагентов?': 'reagents',
            'Свободный комментарий (не обязательно)': 'comment',

        }, inplace=True)

        df.rename(columns={
            'Сервисные работы по уходу за бассейном: / Уборка бассейна ручным водным пылесосом': 'w1'
        }, inplace=True)
        df.rename(columns={
            'Сервисные работы по уходу за бассейном: / Промывка фильтра': 'w2'
        }, inplace=True)
        df.rename(columns={
            'Сервисные работы по уходу за бассейном: / Уборка роботом - пылесосом': 'w3'
        }, inplace=True)
        df.rename(columns={
            'Сервисные работы по уходу за бассейном: / Чистка стен щеткой': 'w4'
        }, inplace=True)
        df.rename(columns={
            'Сервисные работы по уходу за бассейном: / Чистка ватерлинии': 'w5'
        }, inplace=True)
        df.rename(columns={
            'Сервисные работы по уходу за бассейном: / Долив свежей воды': 'w6'
        }, inplace=True)

        ds = df['works'] = df.w1.map(str) + ' ' + df.w2.map(str) + ' ' + df.w3.map(
            str) + ' ' + df.w4.map(str) + ' ' + df.w5.map(str) + ' ' + df.w6.map(str)
        #ds = ds.to_list()
        ds = nnn(ds)
        df['works'] = pd.Series(np.array(ds))
        df['phone'] = nnn(df['phone'])
        df['email'] = nnn(df['email'])
        df['PH'] = numn(df['PH'])
        df['CL'] = numn(df['CL'])
        df['RX'] = numn(df['RX'])
        df['T'] = numn(df['T'])
        df['water_cond'] = nnn(df['water_cond'])
        df['reagents'] = nnn(df['reagents'])
        df['comment'] = nnn(df['comment'])


        return df


    file = 'C:/Users/77109/PycharmProjects/PoolServiceLog/PSL/poolservice/ZhurnalPH.xlsx'
    df = up_data(file)
    df = df.reset_index()

    i=0
    for index, row in df.iterrows():
            p = Pool(title=row['pool'], slug=str(index)+'PSL1', owner=row['owner'], phone=row['phone'], email=row['email'])
            #print(p.title, p.slug, p.owner, p.email, p.phone)
            p.save()
            ps = PoolService(title=row['pool'],
                             time_create=row['time_create'],
                             PH=row['PH'],
                             CL=row['CL'],
                             RX=row['RX'],
                             T=row['T'],
                             water_cond=row['water_cond'],
                             reagents=row['reagents'],
                             works=row['works'],
                             comment=row['comment'],
                             )
            #print(ps.title, ps.PH, ps.CL, ps.RX, ps.T, ps.water_cond, ps.reagents, ps.works, ps.comment)
            ps.save()




