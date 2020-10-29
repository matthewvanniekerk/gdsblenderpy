#from .importer import Importer
import matplotlib.pyplot as plt
import numpy as np

class Layer(object):
    '''
    Parameters
    -----------
    layer (int) - the layer number
    datatype (int) - the datatype
    z (float) - the starting z height in microns
    thickness (float) - layer thickness extending from z to final height
    color (float) - (r , g, b, alpha)
    '''
    def __init__(self, name, layer, datatype, z, thickness, color, alpha, etch_target = None ):
        
        self.name = name
        self.layer = layer
        self.datatype = datatype
        self.z = z
        self.thickness = thickness
        self.etch_target = etch_target
        self.color = (color[0]/255,color[1]/255,color[2]/255,alpha)
        
class LayerStack(object):
    '''
    Parameters
    ----------

    layers (list) - list of layers 
    '''
    def __init__(self,name,layers):
        self.name = name
        self.layers = layers
        self.layer_dict = {}
        for lay in self.layers:
            self.layer_dict[lay.name] = lay
        self.etch_targets = []
        self.etch_layers = []
        # create the etch layer and targets
        for lay in self.layers:
            if lay.etch_target is not None:
                self.etch_targets.append(self.layer_dict[lay.etch_target])
                self.etch_layers.append(lay)
                print(self.layer_dict[lay.etch_target])
        # chcange the heights
        for i in range(len(self.etch_layers)):
            el = self.etch_layers[i]
            et = self.etch_targets[i]
            final_height = et.thickness + et.z
            # el.thickness = et.thickness
            el.thickness = et.thickness - el.z
            et.thickness = el.z
            # lay.thickness = lay.z-etch_layer.z
            el.color = et.color

    def plot(self):

        for lay in self.layers:
            plt.fill([0 , 0 , 1, 1],[lay.z,lay.z+lay.thickness, lay.z+lay.thickness, lay.z], label = lay.name, alpha = 0.3,  color = (lay.color[0],lay.color[1],lay.color[2]), lw = 0)
                
        plt.title(self.name)
        plt.grid(False)
        plt.xlabel('')
        plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False)
        plt.ylabel(r'Layer Z Profile ($\mu$m)')
        plt.legend()
        plt.show()

    def fetch_params(self, key):
        for lay in self.layers:
            if key[0] == lay.layer and key[1] == lay.datatype:
                return lay.z, lay.thickness, lay.name
        return 0,0, None


