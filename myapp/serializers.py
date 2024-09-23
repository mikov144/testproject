from rest_framework import serializers
from .models import Parts


class PartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parts
        fields = '__all__'