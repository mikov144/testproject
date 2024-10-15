# from django.core.serializers import serialize
from mptt.utils import get_cached_trees
from rest_framework import generics, viewsets

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd

from .serializers import ImportSerializer

from .models import Materials, Category, MaterialTest, CategoryTest
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


class ImportModelAPIView(APIView):
    serializer_class = ImportSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        try:
            data = request.FILES
            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response({
                    'status':False,
                    'message':'Выберите правильный файл'
                }, status=status.HTTP_400_BAD_REQUEST)

            excel_file = data.get('file')
            data = pd.read_excel(excel_file, engine='calamine', dtype=str).to_dict('records')
            materials = []
            categories = []

            for i in data:

                if pd.isna(i['Наименование материала']) and pd.isna(i['Код материала']) and pd.isna(i['Стоимость материала']):
                    continue
                else:
                    material = MaterialTest(
                        name=i['Наименование материала'],
                        code=i['Код материала'],
                        price=i['Стоимость материала']
                    )
                    materials.append(material)

                category = CategoryTest(
                    name=i['Наименование категории'],
                    code=i['Код категории']
                )
                categories.append(category)

            MaterialTest.objects.bulk_create(materials)
            CategoryTest.objects.bulk_create(categories)

            return Response({
                'status':True,
                'message':'Данные загружены'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'status': False,
                'message': 'Не удалось загрузить данные'
            }, status=status.HTTP_400_BAD_REQUEST)
