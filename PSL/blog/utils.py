# Сторонние константы
TITLE_CHOICES = (
    ('A', 'Сообщение о критической ошибке'),
    ('B', 'Сообщение, требующее внимания'),
    ('C', 'Предложения по работе проекта'),
    ('D', 'Информационное сообщение'),
)
menu = [
         {'title':'Главная', 'url_name':'home'},
         ]


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


