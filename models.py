#from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import MultiPolygon

# Create your models here.
class NPVMap(models.Model):
    NPV=models.FloatField()
    geom=models.MultiPolygonField()

    def __str__(self):
        return self.PolId

    class Meta:
        verbose_name_plural='NPVMap'

class LinesMap(models.Model):
    LineId= models.CharField(max_length=1000)
    voltage= models.IntegerField()
    geom=models.MultiLineStringField()

    def __str__(self):
        return self.LineId

    class Meta:
        verbose_name_plural='LinesMap'

class ZoneMap(models.Model):
    zone= models.CharField(max_length=100)
    price= models.FloatField()
    geom=models.MultiPolygonField()

    def __str__(self):
        return self.LineId

    class Meta:
        verbose_name_plural='ZoneMap'

class WindMap(models.Model):
    speed= models.CharField(max_length=100)
    colorcode= models.CharField(max_length=100)
    geom=models.MultiPolygonField()

    def __str__(self):
        return self.LineId

    class Meta:
        verbose_name_plural='WindMap'
