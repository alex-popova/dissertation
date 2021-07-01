from django.contrib import admin
from django.contrib.gis.geos import GEOSGeometry
from datetime import datetime
from leaflet.admin import LeafletGeoAdmin
import pandas as pd
import geopandas as gpd
from pandas import ExcelWriter
from pandas import ExcelFile
import shapely.wkt

from capacityapp.models import NPVMap
from capacityapp.models import LinesMap
from capacityapp.models import ZoneMap
from capacityapp.models import WindMap

# Register your models here.

class CapacityPlannerAdmin(LeafletGeoAdmin):
    pass

admin.site.register(NPVMap, CapacityPlannerAdmin)
admin.site.register(LinesMap, CapacityPlannerAdmin)
admin.site.register(ZoneMap, CapacityPlannerAdmin)
admin.site.register(WindMap, CapacityPlannerAdmin)

df_NPV_reader = pd.read_csv('/Users/alexandrapopova/Downloads/NPV_Map_csv.csv')
df_NPV_reader = df_NPV_reader.head(100)

df_lines_reader = pd.read_csv('/Users/alexandrapopova/Downloads/linesmap_simplified.csv')
df_zones_reader = pd.read_csv('/Users/alexandrapopova/Downloads/zone_map.csv')
df_wind_reader = pd.read_csv('/Users/alexandrapopova/Downloads/wind_map_2.csv')

for index, row in df_NPV_reader.iterrows():
    PolId= row['index']
    zone = row['zone']
    DailyEnergy= row['Daily Ener']
    NPV=row['NPV, kEUR']
    geom=row['WKT']

    NPVMap(PolId=PolId, zone=zone, DailyEnergy=DailyEnergy, NPV=NPV, geom=geom).save()

for index, row in df_lines_reader.iterrows():
    LineId= row['line_id']
    voltage = row['voltage']
    geom=row['WKT']

    LinesMap(LineId=LineId, voltage=voltage, geom=geom).save()

for index, row in df_zones_reader.iterrows():
    zone= row['zone']
    price = row['average_price_average_price']
    geom=row['WKT']

    ZoneMap(zone=zone, price=price, geom=geom).save()

for index, row in df_wind_reader.iterrows():
    speed= row['title']
    colorcode = row['fill']
    geom=row['WKT']

    WindMap(speed=speed, colorcode=colorcode, geom=geom).save()
