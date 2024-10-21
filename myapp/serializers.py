from rest_framework import serializers
from .models import Materials, Category
import os


class MaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materials
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'code', 'parent']


class CategoryTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    materials = MaterialsSerializer(many=True)

    class Meta(CategorySerializer.Meta):
        model = Category
        fields = ['id', 'name', 'code', 'parent', 'children', 'materials']

    def get_children(self, obj):
        children = obj.get_children()
        return CategoryTreeSerializer(children, many=True).data


class ImportSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.xls', '.xlsx']
        if ext.lower() not in valid_extensions:
            raise serializers.ValidationError(
                'Неправильный формат файла. Пожалуйста, загрузите файл формата .xls или .xlsx.')
        return value
