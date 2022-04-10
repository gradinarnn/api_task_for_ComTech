from rest_framework import serializers

from .models import Catalog, Element


class ElementsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Element
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        validation = kwargs.pop('validation', None)

        # validation==True говорит а том, что мы хотим провести валидацию и для этого нам нужны только поля ['parent_id', 'code', 'value']
        if validation==True:
            self.Meta.fields = ['parent_id', 'code', 'value']
        else:
            self.Meta.fields = '__all__'

        super(ElementsSerializer, self).__init__(*args, **kwargs)


class GetAllCatalogsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = ['id', 'short_title', 'full_title', 'description', 'version', 'start_date']
        depth = 0

    def __init__(self, *args, **kwargs):
        full_title = kwargs.pop('full_title', None)
        version = kwargs.pop('version', None)
        actual = kwargs.pop('actual', None)

        # full_title и одно из полей (version или actual) показывает нужно нам сериализовывать справочника указанной версии,
        # либо текущей версии, либо добавлять к справочникам элементы
        if full_title and (version or actual == "true"):
            self.Meta.fields.append('elements')
            self.Meta.depth = 1
        else:
            self.Meta.fields = ['id', 'short_title', 'full_title', 'description', 'version', 'start_date']
            self.Meta.depth = 0

        super(GetAllCatalogsSerializer, self).__init__(*args, **kwargs)
