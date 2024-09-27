from rest_framework import serializers
from .models import Materials, Category


class MaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materials
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'code', 'parent']


# class CategoryTreeSerializer(serializers.ModelSerializer):
#     children = serializers.SerializerMethodField()
#
#     class Meta(CategorySerializer.Meta):
#         model = Category
#         fields = ['id', 'name', 'code', 'parent', 'children']
#
#     def get_children(self, obj):
#         children = obj.get_children()
#         return CategoryTreeSerializer(children, many=True).data
