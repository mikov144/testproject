# from django.core.serializers import serialize
from mptt.utils import get_cached_trees
from rest_framework import generics, viewsets
# from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Materials, Category
from .serializers import MaterialsSerializer, CategorySerializer, CategoryTreeSerializer


class MaterialsViewSet(viewsets.ModelViewSet):
    queryset = Materials.objects.all()
    serializer_class = MaterialsSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('code')
    serializer_class = CategorySerializer


class CategoryTreeView(generics.GenericAPIView):
    queryset = Category.objects.all().prefetch_related('materials')
    serializer_class = CategoryTreeSerializer

    def get(self, request):
        root_nodes = get_cached_trees(self.get_queryset())
        serializer = self.get_serializer(root_nodes, many=True)
        return Response(serializer.data)

# class AddExcell(generics.GenericAPIView):
#     serializer_class = serializes.Serializer
#     parser_classes = (MultiPartParser, FormParser)
#
#     def post(self, request):
#         serializer = self.get_serializer(data=request.FILES)
#         serializer.is_valid(raise_exception=True)
#
#         upload_excell(serializer.validated_data)
