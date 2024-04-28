import io

from django.utils import timezone
from rest_framework import serializers

from .models import PoolService


class PoolServiceModel:
    # def __init__(self, title, pool, time_create, time_update, PH, RX, CL, T, water_cond, reagents, works,comment, is_published, author):
    def __init__(self, title, pool):
        self.title = title
        self.pool = pool


class PoolServiceSerializer(serializers.ModelSerializer):
    time_create = serializers.DateTimeField(required=False)

    class Meta:
        model = PoolService
        fields = '__all__'

