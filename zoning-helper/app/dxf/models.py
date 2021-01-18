from django.db import models


# Create your models here.
class BylawSpecification(models.Model):
    context = models.CharField(max_length=128)
    area = models.CharField(max_length=128)
    code = models.CharField(max_length=10)
    text = models.TextField()


class BylawException(models.Model):
    area = models.CharField(max_length=128)
    code = models.CharField(max_length=10)
    text = models.TextField()


class GeoJsonFeature(models.Model):
    type = models.CharField(max_length=30)
    geometry = models.JSONField()
    properties = models.JSONField()

    def __str__(self):
        return str(self.properties['codes'])
