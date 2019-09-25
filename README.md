# gds-blender-py

Translate GDS to Blender files 

# Dependencies

    +Phidl (https://github.com/amccaugh/phidl)
    +GDSPy (https://github.com/heitzmann/gdspy/)
    +NumPy
    +MatplotLib

# Installation
1. First `cd` into your blender path:

    `cd /path/to/blender-2.8/2.80/python`

2. Run ensurepip for your blender's python:

    `/bin/python3.7m lib/python3.7/ensurepip`

3. Now you have pip and can install modules by:

    `bin/pip3 install --target lib/python3.6   packageName`

4. Install the dependencies manually:

    `bin/pip3 install --target lib/python3.6   numpy`
    `bin/pip3 install --target lib/python3.6   gdspy`
    `bin/pip3 install --target lib/python3.6   phidl`

5. Run setup.py for this project after downloading from git (untested)

    ALTERNATIVELY (TODO)

4. Install this module:

    `bin/pip3 install --target lib/python3.6   GDSBlenderPy`

# Creating layer_stack file
TODO Add instrcutions...

# Running Translator
`blender filename.blend --python layerstack-file.py`

Where the layerstack-file.py file has been created following instructions.
See example


# TODO:
## Use:

+Neaten plotting of cross section 

+Boolean subtract for etch targets

## Function:
+[Easier execution](https://blender.stackexchange.com/questions/6817/how-to-pass-command-line-arguments-to-a-blender-python-script)



