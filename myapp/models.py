from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Materials(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование материала')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='materials', verbose_name='Категория')
    code = models.PositiveIntegerField(unique=True, verbose_name='Код материала')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Стоимость материала')

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'

    def __str__(self):
        return self.name

class Category(MPTTModel):
    name = models.CharField(max_length=100, verbose_name='Наименование категории')
    code = models.PositiveIntegerField(unique=True, verbose_name='Код категории')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='Родительский элемент')

    class MPTTMeta:
        order_insertion_by = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name