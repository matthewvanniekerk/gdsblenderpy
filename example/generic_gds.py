
import os
import sys

# add the path so that module may be imported from within blender python env

path = os.path.dirname((os.path.dirname(os.path.realpath(__file__)))) + '/'
sys.path.append(path)
from GDSBlenderPy import Layer , LayerStack , Importer

file_location = path + 'example/gds-blender-test.GDS'

# From http://phrogz.net/css/distinct-colors.html
colors = [
    (0,0,255),
    (191,102,0),
    (76,51,0),
    (48,86,191),
    (246,255,128),  
    (80,89,45),  
    (134,179,170),
    (238,0,255),  
    (166,155,0),  
    (0,51,20),  
    (178,80,45),  
    (121,242,170),  
    (38,77,74),  
    (179,146,134),  
    (255,102,0),  
    (166,0,133)
]

Si =     Layer('Silicon', 1, 0, 0,    0.22, colors[0], 1 )
SiEtch = Layer('Si Etch', 20, 0, 0.11, 1, colors[1], 1, etch_target = Si )
Via = Layer('Via',     11, 0, 0.22, 1, colors[2], 1 )
Metal = Layer('Metal',   12, 0, 1.22, 2, colors[3], 1 )

layerstack = LayerStack('Simple Stack', [Si, SiEtch, Via, Metal])
# layerstack.plot()
imp = Importer(file_location,layerstack)
imp.draw_in_blender()


