from . import views
from django.urls import path, include

from .views import GetAllCatalogsAPIView, GetCatalogElementsAPIView, ElementsValidationAPIView

urlpatterns = [
    path('catalogs/', GetAllCatalogsAPIView.as_view()),
    path('items/', GetCatalogElementsAPIView.as_view()),
    path('items/validation/', ElementsValidationAPIView.as_view()),


]