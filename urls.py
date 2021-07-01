"""capacityplanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf.urls import url
import django.contrib.auth.views
from capacityapp.models import NPVMap
from capacityapp.models import LinesMap
from capacityapp.models import ZoneMap
from capacityapp.models import WindMap

import capacityapp.views

from capacityapp.views import NPV_dataset
from capacityapp.views import lines_dataset
from capacityapp.views import zone_dataset
from capacityapp.views import wind_dataset

urlpatterns = [
    url(r'^$', capacityapp.views.home),
    url(r'^NPV_dataset/$', NPV_dataset, name='NPV_dataset'),
    url(r'^lines_dataset/$', lines_dataset, name='lines_dataset'),
    url(r'^zone_dataset/$', zone_dataset, name='zone_dataset'),
    url(r'^wind_dataset/$', wind_dataset, name='wind_dataset'),
    path('admin/', admin.site.urls),
]
