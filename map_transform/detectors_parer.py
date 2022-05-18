import numpy as np
import pandas as pd
import os
import json
import functools as ft

os.system('rm rou.xml')

# Словарь DetID_to_DevID
DetID_to_DevID = {
    '41039': '150540',
    '10330': '3669',
    '14171': '3752',
    #'101122': '400654', #Полоса для общественного транспорта
    '101126': '400667',
    '101122': '430653',
    '15385': '6539'
}

# Поля на которых стоят детекторы (из net файла)
DetID_to_edges = {
    '41039': None,
    '10330': "162959647#1 162959647#2",
    '14171': None,
    #'101122': None,
    '101126': "408298891#0 408298891#1 408298891#2 456567778 27849853",
    '101122': "135733465 146940881 627999455 27849851",
    '15385': "236838900#0 236838900#1 236838900#2 236838900#3 236838900#4 236838900#5 236838900#6 146940895 162258623#0"
}

with open('rou.xml', "a") as route_file:
    route_file.write('<routes>\n')

# Маршруты с детекторов
with open('rou.xml', "a") as route_file:
    for DetID, edges in DetID_to_edges.items():
        if edges is not None:
            route_file.write(
                f'<route id="r_{DetID}" edges="{edges}" color="red"/>\n'
            )

#hours = None
#weekdays = None
#n_seconds = 100000
###код получше
def get_flows(DetIDs, n_seconds = 10000, hours=None, weekdays=None):
    time = 0
    delta = 300
    dfs = []

    for DetID in DetIDs:
        DevID = DetID_to_DevID[DetID]

        with open(f'detectors/data_{DevID}_year.json', 'r') as json_data:
            data = json.load(json_data)
        df = pd.DataFrame(data[0])[['Time', 'Volume']]
        df.Time = pd.to_datetime(df.Time)
        df = df.groupby('Time').sum().reset_index()
        df = df.rename(columns = {'Volume': f'Vol_{DetID}'})

        if hours:
            df = df[df.Time.dt.hour.isin(hours)]
        if weekdays:
            df = df[df.Time.dt.hour.isin(weekdays)]

        dfs.append(df)

    df_final = ft.reduce(lambda left, right: pd.merge(left, right, on='Time'), dfs)[:int(n_seconds / delta + 1)]

    with open('rou.xml', "a") as route_file:
        for index, row in df_final.iterrows():
            for DetID in DetIDs:
                Vol = row[f'Vol_{DetID}']
                if Vol != 0:
                    route_file.write(
                            f'<flow id="flow_{DetID}_{time}_{time + delta}" route="r_{DetID}" begin="{time}" end="{time + delta}" vehsPerHour="{Vol}" departSpeed="max" departPos="base" departLane="best"/> \n'
                        )
            time += delta
            

DetIDs = ['10330', '101126', '101122', '15385']
get_flows(DetIDs, n_seconds=100000, hours=[0, 1, 2, 3, 4, 5], weekdays=None)

with open('rou.xml', "a") as route_file:
    route_file.write('</routes>\n')

