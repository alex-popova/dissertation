from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from datetime import datetime
from django.core.serializers import serialize
from capacityapp.models import NPVMap
from capacityapp.models import LinesMap
from capacityapp.models import ZoneMap
from capacityapp.models import WindMap
from django.template.context import Context
import geopandas as gpd
import pandas as pd

# Create your views here.
def NPV_dataset(request):
    npvmap=serialize('geojson', NPVMap.objects.all())
    return HttpResponse(npvmap, content_type='json')

def lines_dataset(request):
    linesmap=serialize('geojson', LinesMap.objects.all())
    return HttpResponse(linesmap, content_type='json')

def zone_dataset(request):
    zonemap=serialize('geojson', ZoneMap.objects.all())
    return HttpResponse(zonemap, content_type='json')

def wind_dataset(request):
    windmap=serialize('geojson', WindMap.objects.all())
    return HttpResponse(windmap, content_type='json')


def home(request):
    """Renders home page """
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
        }

    )
