import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import PoolService

class PoolServiceModel:
    # def __init__(self, title, pool, time_create, time_update, PH, RX, CL, T, water_cond, reagents, works,comment, is_published, author):
    def __init__(self, title, pool):
        self.title = title
        self.pool = pool
        # self.time_create = time_create
        # self.time_update = time_update
        # self.PH = PH
        # self.RX = RX
        # self.CL = CL
        # self.T = T
        # self.water_cond = water_cond
        # self.reagents = reagents
        # self.works = works
        # self.comment = comment
        # self.is_published = is_published
        # self.author = author


class PoolServiceSerializer(serializers.ModelSerializer):
    # pool_id = serializers.IntegerField(default=0)
    # author_id = serializers.IntegerField(default=0)

    class Meta:
        model = PoolService
        fields = '__all__'
        #fields = ('title','pool_id','PH','RX','CL','T','water_cond','works','comment','author_id')

# class PoolServiceSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     pool_id = serializers.IntegerField(default=0)
#     time_create = serializers.DateTimeField(read_only=True)
#     date_update = serializers.DateField(read_only=True)
#     PH = serializers.FloatField(default=None)
#     RX = serializers.IntegerField(default=None)
#     CL = serializers.FloatField(default=None)
#     T = serializers.FloatField(default=None)
#     water_cond = serializers.CharField(max_length=255, default='')
#     works = serializers.CharField(max_length=1000,default='')
#     comment = serializers.CharField(max_length=1000,default='')
#     is_published = serializers.BooleanField(default=True)
#     author_id = serializers.IntegerField(default=0)
#
#     def create(self, validated_data):
#         return PoolService.objects.create(**validated_data)


# def encode():
#     # model = PoolServiceModel('СервисAPI', 5,
#     #                          '20240309 12:12:12', '20240309 12:12:12',
#     #                          7.8,0, 1.0, 25, 'Мутная, зелёная',
#     #                          'Порошок РН минус 2 кг', '', '',
#     #                          'True', 1)
#     model = PoolServiceModel('СервисAPI', 5)
#     model_sr = PoolServiceSerializer(model)
#     print(model_sr.data, type(model_sr.data))
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
#
# def decode():
#     stream = io.BytesIO(b'{"title":"VisitAPIincoming","pool":1}')
#     # stream - мымышленные входящие данные, которые в реале приходят из вне
#     data = JSONParser().parse(stream)
#     serializer = PoolServiceSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)



# class PoolServiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PoolService
#         fields = (
#             'title',
#             'pool',
#             'time_create',
#         )