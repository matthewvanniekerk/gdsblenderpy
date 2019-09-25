'''
Project purpose is to import a gds and export a blender file.

This borrows heavily from PHIDL (https://github.com/amccaugh/phidl)
and from gdspy (https://github.com/heitzmann/gdspy/)

It is not intended as an individualistic feat, but more as a synthesis of simple
methods to create nice pictures. 


Author:
Matthew van Niekerk
'''
import numpy as np

try:
    import bpy
except:
    print('You must run this file from the Blender build of python to ustilize interop with Blender.')


import matplotlib.pyplot as plt
import phidl.geometry as pg
import math
import phidl
from phidl.device_layout import Device, DeviceReference, Port, Polygon
import gdspy
# when this is run from blenders python, need to import the module in this way
import sys
# sys.path.append('/Users/matthewvanniekerk/Documents/RIT/GIT/GDS-BLENDER-PY/gds-blender-py/')
import os
#test

import sys
import warnings


  
'''
Importer object takes a gds file as a constrcutoor

'''
class Importer(object):
    '''
    Parameters
    ----------
    filename (string) - the filename of the gds file
    layerstack (LayerStack) - Layer Stack for this gds
    '''
    def __init__(self, filename, layerstack, cellname = None):

        self.filename = filename
        self.cellname = cellname
        self.gds = self._import_gds()
        self.layerstack = layerstack
        self.vertices = self._extract_vertices()


    '''
    Paramters
    ---------
    filename (string) - the filename of the GDS

    Returns
    -------
    D (list) - list of Device objects

    Purpose
    -------
    Import any gds file and select the largest top cell as the top cell.
    '''
    def _import_gds(self):
        gdsii_lib = gdspy.GdsLibrary()
        gdsii_lib.read_gds(self.filename)
        top_level_cells = gdsii_lib.top_level()
        cellname = self.cellname 
        if cellname is not None:
            if cellname not in gdsii_lib.cell_dict:
                raise ValueError('The requested cell (named %s) is not present in file %s' % (cellname,self.filename))
            topcell = gdsii_lib.cell_dict[cellname]
        elif cellname is None and len(top_level_cells) == 1:
            topcell = top_level_cells[0]
        elif cellname is None and len(top_level_cells) > 1:
            areas = []
            for cell in top_level_cells:
                areas.append(cell.area())
            ind = areas.index(max(areas))
            topcell = top_level_cells[ind]
            

        D = Device('import_gds')
        polygons = topcell.get_polygons(by_spec = True)

        for layer_in_gds, polys in polygons.items():
            D.add_polygon(polys, layer = layer_in_gds)
        return D
    
    
    def _extract_vertices(self):

        extracted = {}
        points = []
        layers = []
        gds = self.gds
        
        if gds is not list: gds = [gds]
        for item in gds:
            if isinstance(item, (Device, DeviceReference, gdspy.CellArray)):
                polygons_spec = item.get_polygons(by_spec = True, depth = None)
                for key in sorted(polygons_spec):
                    polygons = polygons_spec[key]
                    layers.append(key)
                    points.append(self._vert_polygons(polygons))
            elif isinstance(item, Polygon):
                polygons = item.polygons
                layers.append(key)
                points.append(self._vert_polygons(polygons))     
        extracted['vertices'] = points
        extracted['layers'] = layers
        return extracted

    def _vert_polygons(self, polygons):
        vertices = []
        for poly in polygons:
            points = np.concatenate((poly,[poly[0]]),axis=0)
            points_stack = np.vstack(points)
            points_out = points_stack[:,0],points_stack[:,1]
            vertices.append(points_out)
        return vertices
    
    def draw_in_blender(self):
        # Delete all meshes in the scene
        for item in bpy.data.meshes:
            bpy.data.meshes.remove(item)
        vertices = self.vertices
        layer_stack = self.layerstack
        for layer in layer_stack.layers:
            mat = bpy.data.materials.get(layer.name)
            if mat is None:
                mat = bpy.data.materials.new(name=layer.name)
            mat.diffuse_color = layer.color
            
        vert_list = []
        extrude = []
        lname = []
        for i in range(len(vertices['vertices'])):
            vert = vertices['vertices'][i]
            
            z, thickness, layer_name = layer_stack.fetch_params(vertices['layers'][i])

            if z is None:
                z = -1
            for v in vert:
                vert_list.append(np.array((v[0],v[1],[z]*len(v[0]))).transpose())
                extrude.append(thickness)
                lname.append(layer_name)
                
        for i in range(len(vert_list)):
            if lname[i] is not None:
                verts_data = vert_list[i]
                num_verts = len(verts_data)
                faces_data = [ np.linspace(0,num_verts-1,num_verts).astype(int) ]

                mesh = bpy.data.meshes.new('myMesh_mesh')
                mesh.from_pydata(verts_data,[],faces_data)
                mesh.update()

                new_object = bpy.data.objects.new('meshobj',mesh)
                new_object.data = mesh

                collection = bpy.context.collection
                collection.objects.link(new_object)
                bpy.context.view_layer.objects.active = new_object
                bpy.ops.object.editmode_toggle()

                bpy.ops.mesh.extrude_region_move(
                    TRANSFORM_OT_translate={"value":(0, 0, extrude[i] )}
                )
                bpy.ops.object.editmode_toggle()
        
                new_object.data.materials.append(bpy.data.materials.get(lname[i]))
        
        for lay in self.layerstack.etch_targets:
            name = lay.name
            objects = bpy.data.objects
            for obj in objects:
                if obj.type == 'MESH':
                    for slot in obj.material_slots:
                        #print(str(slot.material))
                        if slot.material == bpy.data.materials.get(name):
                            # TODO Subtraction!!
                            #print('found!')
                            obj.select_set(state=True)
                            



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
        self.etch_targets = []
        for lay in self.layers:
            if lay.etch_target is not None:
                self.etch_targets.append(lay.etch_target)

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


