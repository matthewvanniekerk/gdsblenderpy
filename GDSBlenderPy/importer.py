'''
TODO:
-Comment the code nicely

Project purpose is to import a gds and export a blender file.

This project depends heavily on:

PHIDL (https://github.com/amccaugh/phidl)
gdspy (https://github.com/heitzmann/gdspy/)

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

from .layer import Layer, LayerStack
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

from progressbar import *
  
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
        self.layerstack = layerstack
        self.gds = self._import_gds()
        self._etch_target_helper()
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
    '''
    Remove the drawn etch layers 
    '''
    def _remove_etch_layers(self):
        
        for lay in self.layerstack.etch_layers:
            self.gds.remove_layers(layers = (lay.layer,lay.datatype))

    '''
    Take the etch layer, boolean difference the two layers, and add 
    that layer to the layer that was removed.
    '''
    def _etch_target_helper(self):

        etch_layers = []
        etch_targets = []
        layer_target = []
        for elay in self.layerstack.etch_layers:
            etch_layers.append(self.gds.get_polygons(by_spec = True, depth = None)[(elay.layer,elay.datatype)])
            layer_target.append((elay.layer,elay.datatype))
        for etar in self.layerstack.etch_targets:
            etch_targets.append(self.gds.get_polygons(by_spec = True, depth = None)[(etar.layer,etar.datatype)])
            
        # Do this with gdspy! dont go back to Device.

        etch_layers,etch_targets
        new_polygons = []
        for i in range(len(etch_targets)):
            p = gdspy.fast_boolean(operand1 = etch_targets[i], \
                                operand2 = etch_layers[i], \
                                operation = 'not', \
                                precision = 1e-9, \
                                max_points = 4000,\
                                layer = layer_target[i][0],\
                                datatype = layer_target[i][1] )
            new_polygons.append(p)
        self._remove_etch_layers()

        for i in range(len(new_polygons)):
            self.gds.add_polygon(new_polygons[i],layer = layer_target[i])

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
                
        widgets = ['Drawing:', Percentage(), ' ', Bar(marker='#', left = '[', right = ']' ), \
                   ' ', ETA(), ' ', FileTransferSpeed()]
        pbar = ProgressBar(widgets = widgets, max_value= len(vert_list) + len(lname))
        pbar.start()
        for i in range(len(vert_list)):
            if lname[i] is not None:
                verts_data = vert_list[i]
                num_verts = len(verts_data)
                faces_data = [ np.linspace(0,num_verts-1,num_verts).astype(int) ]

                mesh = bpy.data.meshes.new('myMesh_mesh')
                mesh.from_pydata(verts_data,[],faces_data)
                mesh.update()

                new_object = bpy.data.objects.new(lname[i],mesh)
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
                pbar.update(i)
                i = i + 1
        
        
        # Join All like materials to one Mesh
        context = bpy.context
        scene = context.scene
        for layer in lname:
            mats = [m.name for m in bpy.data.materials if m.name== layer]
            for mat in mats:
                obs = [o for o in scene.objects
                        if o.type == 'MESH'
                        and mat in o.material_slots]

                if len(obs) > 1:
                    # clear prior selection
                    for o in context.selected_objects:
                        o.select_set(False)
                    for o in obs:
                        o.select_set(True)
                    context.view_layer.objects.active = obs[0]
                    bpy.ops.object.join()
            i = i + 1
        pbar.finish()
        
        





        