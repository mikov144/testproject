from rest_framework import generics, viewsets
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Materials, Category
from .serializers import MaterialsSerializer, CategorySerializer


class MaterialsViewSet(viewsets.ModelViewSet):
    queryset = Materials.objects.all()
    serializer_class = MaterialsSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('code')
    serializer_class = CategorySerializer


# class CategoryTreeView(generics.GenericAPIView):
#     queryset = Category.objects.all().order_by('code')
#     serializer_class = CategoryTreeSerializer
#
#     def get(self, request):
#         root_nodes = get_children(self.get_queryset())
#         serializer = self.get_serializer(root_nodes, many=True)
#         return Response(serializer.data)

