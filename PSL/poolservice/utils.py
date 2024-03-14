# Файл хранения классов Mixin и всех обобщенных методов и классов и общеприменимых данных

from poolservice.models import *
import pandas as pd
import numpy as np


menu = [
         {'title':'Главная', 'url_name':'home'},
         {'title':'Разработка', 'url_name':'blog'},
         ]

appmenu = [
         {'title':'Добавить сервис', 'url_name':'new_log'},
         {'title':'Новый бассейн', 'url_name':'new_pool'},
         ]


# Обобщенный класс для классов представления в views.py
class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        pools = Pool.objects.all()
        user_pools = Pool.objects.filter(author=self.request.user)
        user_menu = menu.copy()
        app_menu = appmenu.copy()

        context['menu'] = user_menu
        context['appmenu'] =app_menu
        context['pools'] = pools
        context['user_pools'] = user_pools
        #context['queryset'] = queryset

        if 'pool_selected' not in context:
            context['pool_selected'] = 0
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
                'autocomplete': 'off'
            })


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




