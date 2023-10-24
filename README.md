#Packing Blender addon

Run Python script `pack-addon.py` to create a zip-file that can be installed in Blender as a plugin.

##Prerequisites

- Python 3.x installed (https://www.python.org/downloads/)

##Usage

pack-addon.py [-h] [-n NAME] [-o OUTPUT] (-dw | -lw [LOCAL]) [-os {windows,macos,all}]

###Options
-  -h, --help: Show help message and exit
-  -n, --name: Specify a name for the addon archive file. "Unity Cloud Blender Addon" is default name
-  -o, --output: Specify a folder to save the addon archive in. "<Path-to-repository>/Dist" is default output folder
-  -dw, --download: Download wheel files
-  -lw, --local: Specify a folder to copy the wheel files from if you choose not to download wheel files
-  -os {windows,macos,all}, --system {windows,macos,all}: Specify target operation system. 'all' is default value
