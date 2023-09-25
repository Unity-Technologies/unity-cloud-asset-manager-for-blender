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

python pack-addon.py [-o|--output <OUTPUT_DIRECTORY>] [-n|--name <NAME>]


###Options

- --output: the directory to place the zip-file to. Default is '.'
- --name: the name of the root folder of the resulting addon; also is a name of the zip-file. Default is 'Unity Cloud Blender Addon'