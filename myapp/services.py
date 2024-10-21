from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
import logging
from .models import Materials, Category
from .serializers import ImportSerializer


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
                    'message': 'Неправильный формат файла. Пожалуйста, загрузите файл формата .xls или .xlsx.'
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
