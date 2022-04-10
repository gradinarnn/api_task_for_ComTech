import json

from django.core.exceptions import ValidationError
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Catalog, Element
from .serializers import GetAllCatalogsSerializer, ElementsSerializer
from .utils import get_actual_catalog


class GetAllCatalogsAPIView(APIView):
    """
        Эндпоинт для получения справочников
    """
    serializer_class = GetAllCatalogsSerializer

    def get(self, request):
        filter_date = request.GET.get('date')

        # получаем справочники, актуальные на указанную дату
        if filter_date:
            try:
                all_catalogs = Catalog.objects.filter(start_date__lte=filter_date)
            except ValidationError:
                return HttpResponseBadRequest("неверный формат даты")

        # получаем все справочники
        else:
            all_catalogs = Catalog.objects.all()
        catalog_serializer = self.serializer_class(all_catalogs, many=True)
        return Response(catalog_serializer.data, status=status.HTTP_200_OK)


class GetCatalogElementsAPIView(APIView):
    """
        Эндпоинт для получения элементов справочника
    """
    serializer_class = GetAllCatalogsSerializer

    def get(self, request):
        catalog_full_title = request.GET.get('catalog_full_title')
        catalog_version = request.GET.get('catalog_version')
        actual = request.GET.get('actual')

        # получаем справочник указанной версии
        if catalog_full_title and catalog_version:
            try:
                catalog = Catalog.objects.get(full_title=catalog_full_title, version=catalog_version)
            except Catalog.DoesNotExist:
                return HttpResponseNotFound("каталог с таким полным именем каталога или версии не существует")

        # получаем справочник текущей версии
        elif catalog_full_title and (actual == "true"):
            catalog = get_actual_catalog(full_title=catalog_full_title)
            if catalog:
                catalog = catalog[0]
            else:
                return HttpResponseNotFound("актуального каталога с таким полным именем не существует")
        else:
            return HttpResponseBadRequest('один из параметров запроса введен неверно')

        catalog_serializer = self.serializer_class(catalog, full_title=catalog_full_title, version=catalog_version)

        return Response(catalog_serializer.data, status=status.HTTP_200_OK)


class ElementsValidationAPIView(APIView):
    """
        Эндпоинт для валидации элементов справочника
    """
    serializer_class = ElementsSerializer

    def post(self, request):
        elements = json.loads(request.body).get('elements')
        catalog_full_title = json.loads(request.body).get('catalog_full_title')
        catalog_version = json.loads(request.body).get('catalog_version')
        actual = json.loads(request.body).get('actual')

        # получаем справочник указанной версии
        if catalog_full_title and catalog_version:
            try:
                catalog = Catalog.objects.get(full_title=catalog_full_title, version=catalog_version)
            except Catalog.DoesNotExist:
                return HttpResponseNotFound("каталог с таким полным именем каталога или версии не существует")

        # получаем справочник текущей версии
        elif catalog_full_title and (actual == "true"):
            catalog = get_actual_catalog(full_title=catalog_full_title)
            if catalog:
                catalog = catalog[0]
            else:
                return HttpResponseNotFound("актуального каталога с таким полным именем не существует")
        else:
            return HttpResponseBadRequest('нехватает полного имени каталога или версии')

        valid_elements = {'valid_elements': []}
        for element in elements:

            # проводим валидацию элемента справочника(параметр validation=True показывает что мы делаем валидацию)
            serializer = self.serializer_class(data=element, validation=True)
            if serializer.is_valid():

                # если элемент валиден, то проверяем есть ли такой элемент в справочнике
                valid_element = Element.objects.all().filter(catalog=catalog, parent_id=element["parent_id"],
                                                             value=element["value"],
                                                             code=element["code"])

                # проводим сериализацию элемента справочника(параметр validation=False показывает что мы делаем сериализацию)
                valid_serializer_element = self.serializer_class(instance=valid_element, validation=False, many=True)

                # если элемент есть в справочнике, то добавляем его в итоговый список
                if valid_serializer_element.data:
                    valid_elements['valid_elements'].append(valid_serializer_element.data)

        return Response(valid_elements, status=status.HTTP_200_OK)
