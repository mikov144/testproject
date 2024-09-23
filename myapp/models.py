from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Parts(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    code = models.IntegerField(blank=True)
    price = models.IntegerField(blank=True)

    class Meta:
        verbose_name = 'Parts'
        verbose_name_plural = 'Parts'

    def __str__(self):
        return self.title

class Category(MPTTModel):
    name = models.CharField(max_length=100, db_index=True)
    catCode = models.IntegerField(blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name