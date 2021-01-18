from django.core.management.base import BaseCommand
from dxf.models import BylawSpecification, BylawException, GeoJsonFeature


class Command(BaseCommand):
    def handle(self, *args, **options):
        BylawSpecification.objects.all().delete()
        BylawException.objects.all().delete()
        GeoJsonFeature.objects.all().delete()
