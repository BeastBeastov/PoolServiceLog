from django.apps import AppConfig


class PoolserviceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'poolservice'
    verbose_name = 'Журнал PH'


class DataimportConfig(AppConfig):
    name = 'dataimport'
