# gds-blender-py

Translate GDS to Blender files 

# Dependencies
    -Phidl (https://github.com/amccaugh/phidl)
    -GDSPy (https://github.com/heitzmann/gdspy/)
    -NumPy
    -MatplotLib

# Installation
    a) first `cd` into your blender path:
    `cd /path/to/blender-2.8/2.80/python`
    b) run ensurepip for your blender's python:
    `/bin/python3.7m lib/python3.7/ensurepip`
    c) Now you have pip and can install modules by:
    `bin/pip3 install --target lib/python3.6   packageName`
    d) Install the dependencies manually:
    `bin/pip3 install --target lib/python3.6   numpy`
    `bin/pip3 install --target lib/python3.6   gdspy`
    `bin/pip3 install --target lib/python3.6   phidl`
    e) Run setup.py for this project after downloading from git (untested)
    ALTERNATIVELY (TODO)
    d) Install this module:
    `bin/pip3 install --target lib/python3.6   GDSBlenderPy`

# Creating layer_stack file
TODO Add instrcutions...

# Running Translator
`blender filename.blend --python layerstack-file.py`

Where the layerstack-file.py file has been created following instructions.
See example


# TODO:
Use:
    -Neaten plotting of cross section 
    -Boolean subtract for etch targets
Function:
    -Easier execution (https://blender.stackexchange.com/questions/6817/how-to-pass-command-line-arguments-to-a-blender-python-script)


