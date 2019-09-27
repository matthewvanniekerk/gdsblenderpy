# gds-blender-py

Translate GDS to Blender files 

# Dependencies

+ [Phidl](https://github.com/amccaugh/phidl)
+ [GDSPy](https://github.com/heitzmann/gdspy/)
+ NumPy
+ MatplotLib

While not an explicit dependency, [KLayout](https://klayout.de) is a fantastic open source tool for viewing and creating GDS files.

# Installing Blender
Follow instructions to install [Blender](https://www.blender.org)

Add blender to path, to allow for commands from the terminal.
The executable exists in these locations (by default).

## Windows
+ 64-bit

`C:\Program Files\Blender Foundation\Blender\blender.exe`

+ 32-bit

`C:\Program Files (x86)\Blender Foundation\Blender\blender.exe`

## Linux

`/usr/bin/blender`

## MacOS

`/Applications/blender/blender.app/Contents/MacOS/blender`


# Installation of this Package
These instructions help to install pip into the python that comes with blender, since python is not released with pip in the first place. More detail can be found [here](https://blender.stackexchange.com/questions/56011/how-to-install-pip-for-blenders-bundled-python) or with a differently worded google search.
1. First `cd` into your blender path:

    `cd /path/to/blender-2.8/2.80/python`

2. Run ensurepip for your blender's python:

    `/bin/python3.7m lib/python3.7/ensurepip`

    * in MacOS, ./python3.7m will run the executable instead of just the filename

3. Now you have pip and can install modules by:

    `bin/pip3 install --target lib/python3.6   packageName`

4. Install the dependencies manually:

    `bin/pip3 install --target lib/python3.6   numpy`
    
    `bin/pip3 install --target lib/python3.6   gdspy`

    `bin/pip3 install --target lib/python3.6   phidl`

5. Run setup.py for this project after downloading from git (untested)

## ALTERNATIVELY (TODO)

4. Install this module:

    `bin/pip3 install --target lib/python3.6   GDSBlenderPy`

# Creating layer_stack file
TODO Add instrcutions...

# Running Translator
`blender filename.blend --python layerstack-file.py`

Where the layerstack-file.py file has been created following instructions.
See example

# TODO
## Use

+ Neaten plotting of cross section 

+ Figure out way to do dopings?

+ Fix plot cross section

## Function
+ [Easier execution](https://blender.stackexchange.com/questions/6817/how-to-pass-command-line-arguments-to-a-blender-python-script)



