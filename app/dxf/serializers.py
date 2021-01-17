from .models import BylawSpecification, BylawException, GeoJson
from rest_framework import serializers


class SpecificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BylawSpecification
        fields = ['context', 'area', 'code', 'text']


class ExceptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BylawException
        fields = ['area', 'code', 'text']


class GeoJsonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GeoJson
        fields = ['data']