import sys
import xml.etree.ElementTree as ET

et = xml.etree.ET.parse('../simulation/grid.net.xml')
root = et.getroot()

for edge_tag in root.findall('edge'):
    for lane_tag in edge_tag.findall('lane'):
        allow = lane_tag.get('allow')
        if allow == "pedestrian delivery bicycle":
            root.remove(edge_tag)
            break

et.write('../simulation/clear.net.xml')


###Удаляю перекресток
import sys
import xml.etree.ElementTree as ET

et = ET.parse('../simulation/grid.net.xml')
root = et.getroot()

for element in root:
    if '1042570013' in ET.tostring(element).decode("utf-8"):
        root.remove(element)

et.write('../simulation/clear.net.xml')
