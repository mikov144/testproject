from django.urls import path, include
from myapp.views import MaterialsViewSet, CategoryViewSet, CategoryTreeView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'materials', MaterialsViewSet)
router.register(r'category', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('category-tree/', CategoryTreeView.as_view(), name='category_tree'),
]
