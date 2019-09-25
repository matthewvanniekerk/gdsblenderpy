
import os
import sys

# add the path so that tortoise may be imported

path = os.path.dirname((os.path.dirname(os.path.realpath(__file__)))) + '/'
sys.path.append(path)
from GDSBlenderPy import *

file_location = path + 'example/gds-blender-test.GDS'

# From http://phrogz.net/css/distinct-colors.html
colors = [
    (0,0,255),
    (191,102,0
    ),
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

layer1 = Layer('Layer 1', 1, 0, 0, 0.5, colors[0], 1 )
layer2 = Layer('Layer 2', 2, 0, 0.5, 0.5, colors[1], 1 )
layer3 = Layer('Layer 3', 3, 0, 0.3, 0.2, colors[2], 1, etch_target = layer2 )

layerstack = LayerStack('Example', [layer1,layer2,layer3])
layerstack.plot()
imp = Importer(file_location,layerstack)
imp.draw_in_blender()


