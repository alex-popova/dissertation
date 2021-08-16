from django.contrib import admin
from django.contrib.gis.geos import GEOSGeometry
from datetime import datetime
from leaflet.admin import LeafletGeoAdmin
import pandas as pd
import geopandas as gpd
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile
import shapely.wkt
import gurobipy as gp
from gurobipy import GRB

df_expanded_sum = pd.read_csv('/Users/alexandrapopova/Downloads/NPV_polygon_map.csv')
df_expanded = pd.read_csv('/Users/alexandrapopova/Downloads/NPV_polygon_map.csv')
demand_df=pd.read_csv('Net_Demand.csv')
NPV_gdf_epsg3857=pd.read_csv('')

'''create zone array'''
zone_list=df_expanded_sum['Zone'].drop_duplicates().sort_values().reset_index()['Zone'].tolist()
loc_zones = pd.DataFrame(0, index=range(0,44435),columns=zone_list)
for column in loc_zones:
    for i in range(0,44435):
        if (df_expanded_sum.Zone[i]==column):
            loc_zones[column][i]=1
        else:
            continue
loc_zones_array=loc_zones.to_numpy()

'''create energy array'''
energy_df = pd.DataFrame(0, index=range(0,44435),columns=['Vestas', 'Nordex', 'Enercon', 'SolarPV'])
for i in range(0,44435):
    energy_df['Vestas'][i]=np.array(df_expanded[df_expanded['loc_id']==i]['Vestas_Energy_Max_MWh']).astype(object)
    energy_df['Nordex'][i]=np.array(df_expanded[df_expanded['loc_id']==i]['Nordex_Energy_Max_MWh']).astype(object)
    energy_df['Enercon'][i]=np.array(df_expanded[df_expanded['loc_id']==i]['Enercon_Energy_Max_MWh']).astype(object)
    energy_df['SolarPV'][i]=np.array(df_expanded[df_expanded['loc_id']==i]['SolarPV_Energy_Max_MWh']).astype(object)
energy_array=energy_df.to_numpy()

'''create demand constraint array'''
demand_const= pd.DataFrame(0, index=range(0,1),columns=zone_list)
demand_const_array=demand_const.to_numpy()[0]
for column in demand_const:
    demand_const[column][0]=(np.array(demand_df[column])).astype(object)

'''add area constraint'''
loc_area=NPV_gdf_epsg3857['area'].to_numpy()

'''define model coefficients'''
v_cost=df_expanded_sum['Vestas Investment Cost, kEUR'].to_numpy()
n_cost=df_expanded_sum['Nordex Investment Cost, kEUR'].to_numpy()
e_cost=df_expanded_sum['Enercon Investment Cost, kEUR'].to_numpy()
s_cost=df_expanded_sum['SolarPV Investment Cost, kEUR'].to_numpy()
v_NPV=df_expanded_sum['Vestas NPV, kEUR'].to_numpy()
n_NPV=df_expanded_sum['Nordex NPV, kEUR'].to_numpy()
e_NPV=df_expanded_sum['Enercon NPV, kEUR'].to_numpy()
s_NPV=df_expanded_sum['SolarPV NPV, kEUR'].to_numpy()



def function (zone, investment_amount):
    df_expanded_sum['mask']=np.where((df_expanded_sum['Zone']==zone), 1, 0)
    mask_array=df_expanded_sum['mask'].to_numpy()
    cost_max=investment_amount

    I=range(len(df_expanded_sum))
    E=range(4)
    Z=range(len(demand_const.columns))
    H=range(48)

    m=gp.Model()
    x = [[m.addVar(vtype=GRB.INTEGER) for j in J] for i in I] #binary variables
    #for i in I:
    #    m.addConstr(((x[i][0]+x[i][1]+x[i][2])*0.8+x[i][3]*0.02) <= loc_area[i])
    for z in Z:
        for h in H:
            m.addConstr(gp.quicksum((energy_array[i][0][h]*x[i][0]+energy_array[i][1][h]*x[i][1]+energy_array[i][2][h]*x[i][2]+energy_array[i][3][h]*x[i][3])*loc_zones_array[i][z] for i in I) <=demand_const_array[z][h])

    m.addConstr(gp.quicksum(v_cost[i]*x[i][0] + n_cost[i]*x[i][1] + e_cost[i]*x[i][2] + s_cost[i]*x[i][3] for i in I)<=cost_max)
    m.setObjective(gp.quicksum(v_NPV[i] * x[i][0]*mask_array[i]+n_NPV[i]*x[i][1]*mask_array[i]+e_NPV[i]*x[i][2]*mask_array[i]+s_NPV[i]*x[i][3]*mask_array[i] for i in I), GRB.MAXIMIZE)
    m.optimize()

    solution_df=df_expanded_sum.copy()
    vars=m.getVars()
    Vestas_Location=np.array([])
    Nordex_Location=np.array([])
    Enercon_Location=np.array([])
    SolarPV_Location=np.array([])
    for v in range(m.NumVars):
        if v % 4 == 0:
            Vestas_Location=np.append(Vestas_Location,vars[v].x)
        else:
            if v % 3 == 0:
                Nordex_Location=np.append(Nordex_Location,vars[v].x)
            else:
                if v % 2 == 0:
                    Enercon_Location=np.append(Enercon_Location,vars[v].x)
                else:
                    SolarPV_Location=np.append(SolarPV_Location,vars[v].x)

    solution_df['Vestas_Location']=pd.Series(Vestas_Location)
    solution_df['Nordex_Location']=pd.Series(Nordex_Location)
    solution_df['Enercon_Location']=pd.Series(Enercon_Location)
    solution_df['SolarPV_Location']=pd.Series(SolarPV_Location)

    return (solution_df)
