# unity-cloud-blender-addon
[View this project in Backstage](https://backstage.corp.unity3d.com/catalog/default/component/unity-cloud-blender-addon) <br/>
# Converting to public repository
Any and all Unity software of any description (including components) (1) whose source is to be made available other than under a Unity source code license or (2) in respect of which a public announcement is to be made concerning its inner workings, may be licensed and released only upon the prior approval of Legal.
The process for that is to access, complete, and submit this [FORM](https://docs.google.com/forms/d/e/1FAIpQLSe3H6PARLPIkWVjdB_zMvuIuIVtrqNiGlEt1yshkMCmCMirvA/viewform).

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
