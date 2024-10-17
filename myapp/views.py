# from django.core.serializers import serialize
from mptt.utils import get_cached_trees
from rest_framework import generics, viewsets

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
import logging

from .models import Materials, Category
from .serializers import MaterialsSerializer, CategorySerializer, CategoryTreeSerializer, ImportSerializer


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
        logging.basicConfig(level=logging.DEBUG)
        try:
            data = request.FILES
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                logging.error('Invalid serializer')
                return Response({
                    'status': False,
                    'message': 'Выберите правильный файл'
                }, status=status.HTTP_400_BAD_REQUEST)

            excel_file = data.get('file')
            logging.info('Reading Excel file')
            data = pd.read_excel(excel_file, engine='calamine', dtype=str).to_dict('records')
            materials = []
            categories = {}
            logging.info(f'Data from Excel: {data}')

            for i in data:
                parent_category = None
                if not pd.isna(i['Родительский элемент']):
                    parent_code = next((item['Код категории'] for item in data if item['Наименование категории'] == i['Родительский элемент']), None)
                    parent_category = categories.get(parent_code)

                category, created = Category.objects.update_or_create(
                    code=int(i['Код категории']),
                    defaults={'name': i['Наименование категории'], 'parent': parent_category}
                )
                categories[i['Код категории']] = category
                logging.info(f'Created category: {category}')

                if not pd.isna(i['Наименование материала']) and not pd.isna(i['Код материала']) and not pd.isna(i['Стоимость материала']):
                    material = Materials(
                        name=i['Наименование материала'],
                        code=int(i['Код материала']),
                        price=float(i['Стоимость материала']),
                        category=category
                    )
                    materials.append(material)
                    logging.info(f'Appended material: {material}')

            if materials:
                Materials.objects.bulk_create(materials)
                logging.info('Bulk create materials')

            return Response({
                'status': True,
                'message': 'Данные загружены'
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(f'Exception: {e}')
            return Response({
                'status': False,
                'message': 'Не удалось загрузить данные'
            }, status=status.HTTP_400_BAD_REQUEST)






'''
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

                category, created = CategoryTest.objects.update_or_create(
                    code=int(i['Код категории']),
                    parent=i['Родительский элемент'],
                    defaults={'name': i['Наименование категории']}
                )
                categories.append(category)

                if not pd.isna(i['Наименование материала']) and not pd.isna(i['Код материала']) and not pd.isna(i['Стоимость материала']):
                    material = MaterialTest(
                        name=i['Наименование материала'],
                        code=int(i['Код материала']),
                        price=float(i['Стоимость материала'])
                    )
                    materials.append(material)

            MaterialTest.objects.bulk_create(materials)

            return Response({
                'status':True,
                'message':'Данные загружены'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'status': False,
                'message': 'Не удалось загрузить данные'
            }, status=status.HTTP_400_BAD_REQUEST)
'''