from rest_framework import generics, viewsets
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Parts, Category
from .serializers import PartsSerializer


class PartsViewSet(viewsets.ModelViewSet):
    queryset = Parts.objects.all()
    serializer_class = PartsSerializer

    @action(methods=['get'], detail=False)
    def category(self, request):
        cats = Category.objects.all()
        return Response({'cats': [c.name for c in cats]})
