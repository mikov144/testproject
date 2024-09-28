import pandas as pd
from myapp.serializers import MaterialsSerializer, CategorySerializer

data = pd.read_excel('Catalog_Testovoe.xlsx', engine='calamine', dtype=str).to_dict('records')

for i in data:
    if pd.isna(i['Наименование материала']) and pd.isna(i['Код материала']) and pd.isna(i['Стоимость материала']):
        print(i, 'Это категория')
        category_serializer = CategorySerializer(
            data={

            }
        )
        category_serializer.is_valid(raise_exception=True)
        category_serializer.save()
    else:
        print(i, 'Это материал')
        material_serializer = MaterialsSerializer(
            data={

            }
        )
        material_serializer.is_valid(raise_exception=True)
        material_serializer.save()
