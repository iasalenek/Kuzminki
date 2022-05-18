import os
import numpy as np
import analysis
from matplotlib import pyplot as plt
import xml.etree.ElementTree as ET
import os, sys

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
    #sys.path.append("/opt/homebrew/bin/") #Мой путь

map_name = 'Kuzminki'
path = f"../simulation/"
os.system(f"rm -r {path}")
os.system(f"mkdir {path}")
os.system(f"cp -fr grid.sumocfg {path}/grid.sumocfg")

os.system(f"netconvert --osm-files {map_name}.osm -o {path}grid.net.xml -W --keep-edges.by-vclass passenger")
#os.system(f"polyconvert --net-file {path}grid.net.xml --osm-files {map_name}.osm --type-file typemap.xml -o {path}grid.poly.xml")