from rest_framework import serializers
from .models import Parts


class PartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parts
        fields = '__all__'


# class ClassSystemsTreeSerializer(serializers.ModelSerializer):
#     children = serializers.SerializerMethodField()
#
#     class Meta(ClassSystemsSerializer.Meta):
#         model = ClassSystemsModel
#         fields = ['id', 'name', 'code', 'parent', 'children']
#
#     def get_children(self, obj):
#         children = obj.get_children()
#         return ClassSystemsTreeSerializer(children, many=True).data
