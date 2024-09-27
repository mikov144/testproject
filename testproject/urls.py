from django.contrib import admin
from django.urls import path, include

from myapp.views import MaterialsViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'materials', MaterialsViewSet)

urlpatterns = [
    path('', include('myapp.urls')),
]
