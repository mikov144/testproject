from django.contrib import admin
from django.urls import path, include

from myapp.views import MaterialsViewSet, CategoryViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'materials', MaterialsViewSet)
router.register(r'category', CategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
