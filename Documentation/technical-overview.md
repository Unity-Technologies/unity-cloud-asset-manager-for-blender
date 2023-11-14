# Technical overview

This document will describe the structure of the "Asset Manager for Blender", explain functionality of the main modules and functions used in this repository.

## Table of contents

- [Technical overview](#technical-overview)
  - [Table of contents](#table-of-contents)
  - [Add-on structure](#add-on-structure)
  - [Add-on registration](#add-on-registration)
  - [Installing Unity Cloud Python SDK in Blender's python runtime](#installing-unity-cloud-python-sdk-in-blenders-python-runtime)
  - [Interface](#interface)
    - [Add-on menu](#add-on-menu)
    - [Add-on dialog](#add-on-dialog)
  - [Listing organizations and projects](#listing-organizations-and-projects)
  - [Asset creation](#asset-creation)
    - [Asset data generation](#asset-data-generation)
    - [Asset data uploading](#asset-data-uploading)
  - [See also](#see-also)
  
## Add-on structure

The AM4B is essentially a set of Python wheel files, that can be installed into Blender as an add-on.
AM4B contains 4 files:
- `__init__.py`
- `uc_wheel_installation.py`
- `uc_blender_utils.py`
- `uc_asset_manager.py`

`__init__.py` contains data that is required by Blender in order to properly register and display the add-on.
`uc_wheel_installation` module installs Unity Cloud Python SDK it in Blender environment.
`uc_blender_utils` module provides methods to generate data, that can be uploaded to Asset Manager (FBX files, thumbnails).
`uc_asset_manager` module provides access to Asset Manager through Unity Cloud Python SDK.

## Add-on registration

`__init__.py` provides information that is required by Blender in order to display the add-on (see [Add-on Tutorial](https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html#what-is-an-add-on) and [Requirements for contributed Scripts](https://wiki.blender.org/wiki/Process/Addons/Guidelines) for details):
- `bl_info`: provides add-on name, description, category, minimum Blender version that the add-on is compatible with.
- `register()` function: initiates installation of Unity Cloud Python SDK in Blender environment, registers Blender operators and displays add-on as Blender scene menu item.
- `unregister()` function: unregisters operators and hides add-on menu item.

## Installing Unity Cloud Python SDK in Blender's python runtime

To install Unity Cloud Python SDK, `__init.py__.register()` executes `install_unity_cloud()` function of `uc_wheel_installation` module. The function identifies the current operating system, checks if it is supported by Unity Cloud Python SDK, selects an according Python wheel file in the add-on zip, and installs it using `pip` command.


## Interface

To define interface of AM4B `__init__.py` implements `UC_Category` and `ExportToCloudOperator` classes, and `draw_func()` function:
- `draw_func()` function displays add-on menu;
- `UC_Category` class describes add-on menu structure and defines menu item functionality;
- `ExportToCloudOperator` class describes add-on

These classes and function must be registered in Blender to display add-on when it is enabled, and unregistered to hide - when disabled:

```
classes = (UC_Category, ExportToCloudOperator)
def register():
    install_unity_cloud()
    for cls in classes:
        bpy.utils.register_class(cls) 
    bpy.types.VIEW3D_MT_editor_menus.append(draw_func)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.VIEW3D_MT_editor_menus.remove(draw_func)
```

### Add-on menu

Add-on menu items are defined with `UC_Category` class and `draw_func` function. See [Blender documentation. Menus](https://docs.blender.org/api/current/bpy.types.Menu.html#menu-bpy-struct) for more information about custom menus in Blender.
`draw_func` function is registered in Blender UI system to display menu structure, described in `UC_Category`, when add-on is enabled.

```
def draw_func(self, context):
    self.layout.menu(UC_Category.bl_idname)
```
    
`UC_Category` class describes the add-on menu and sub-menu items. It provides labels for menu items and define what happens when clicked:

```
uc_dialog_op_name = "uc_addon.addon_dialog"
upload_fbx_lbl = "Upload FBX to Asset Manager"

class UC_Category(Menu):
    bl_idname = "VIEW3D_MT_UC_category"
    bl_label = "Unity Cloud"

    def draw(self, context):
        layout = self.layout
        layout.operator(uc_dialog_op_name, text=upload_fbx_lbl) 
        # display "Upload FBX to Asset Manager" sub-menu item when "Unity Cloud" is clicked. 
        # open add-on dialog when sub-menu item is clicked
```

### Add-on dialog

When `Unity Cloud`->`Upload FBX to Asset Manager` menu is clicked, the `Upload FBX to Asset Manager` dialog opens. The UI and functionality of the dialog is defined by `ExportToCloudOperator` class. See [Blender Documentation. Operators](https://docs.blender.org/api/current/bpy.ops.html) for more information about custom operators in Blender.

```
uc_dialog_op_name = "uc_addon.addon_dialog"
upload_fbx_lbl = "Upload FBX to Asset Manager"

project_items = []
organization_items = []

def on_selected_org_changed(self, context):
    #get a list of projects for currently selected organization
    refresh_projects(self.org_dropdown)
    
def get_organization(self, context):
    return organization_items

def get_projects(self, context):
    return project_items
...   
class ExportToCloudOperator(bpy.types.Operator):
    bl_idname = uc_dialog_op_name
    bl_label = upload_fbx_lbl

    # define properties to be displayed:
    org_dropdown: bpy.props.EnumProperty(
            items=get_organization,
            update=on_selected_org_changed, # define an action when selected organization is changed
            ...)
    project_dropdown: bpy.props.EnumProperty(
            items=get_projects,
            ...)
    name_input: bpy.props.StringProperty(name="Asset name:", default="New asset")
    description_input: bpy.props.StringProperty(name="Asset description:", default="")
    tags_input: bpy.props.StringProperty(name="Tags:", description="Asset tags separated by spaces: tag1 tag2", default="")
    generate_preview: bpy.props.BoolProperty(name="Generate thumbnail", default=False)

    def invoke(self, context, event):
        ...
        # prepare the list of available organizations to be displayed in dropdown
        refresh_orgs()
        # display listed properties in property dialog
        return context.window_manager.invoke_props_dialog(self)
```

See [Blender Documentation. Property definitions](https://docs.blender.org/api/current/bpy.props.html) and [Window Manager](https://docs.blender.org/api/current/bpy.types.WindowManager.html) for more details about custom dialogs in Blender.

## Listing organizations and projects

As mentioned above, access to Asset Manager is provided by `uc_asset_manager` module which uses Unity Cloud Python SDK. The module should be initialized before usage, and uninitialized when it's not in use. The addon dialog initializes `uc_asset_manager` module and performs login every time when dialog is opened, and uninitializes when dialog is closed:

```
class ExportToCloudOperator(bpy.types.Operator):
    ...
    def cancel(self, context):
        from .uc_asset_manager import uninitialize
        uc_asset_manager.uninitialize()

    def invoke(self, context, event):
        from .uc_asset_manager import initialize, login
        uc_asset_manager.initialize()
        uc_asset_manager.login()

        refresh_orgs()

        return context.window_manager.invoke_props_dialog(self)
```

Also, `ExportToCloudOperator` prepares the list of the available organizations and projects: 

```
def refresh_orgs():
    from .uc_asset_manager import get_organizations
    # get available organizations from Asset Manager
    orgs = uc_asset_manager.get_organizations()
    items = list()
    for org in orgs:
        # and prepare them for display in organizations dropbox
        items.append((org.id, org.name, f"{org.name}. {org.id}"))
    global organization_items
    organization_items = items
    org_id = None
    if len(orgs) > 0:
        org_id = orgs[0].id
    # refresh the list of projects in project dropbox
    refresh_projects(org_id)
```   
```
def refresh_projects(org_id):
    from .uc_asset_manager import get_projects
    if org_id is not None:
        # get available project in selected organization
        projects = uc_asset_manager.get_projects(org_id)
        items = list()
        for project in projects:
            # and prepare them for display in projects dropbox
            items.append((project.id, project.name, f"{project.name}. {project.id}"))
        global project_items
        project_items = items
    else:
        project_items = []
```        

## Asset creation

When user clicks "OK", `ExportToCloudOperator.execute()` function is called. It gathers information from user input, calls `uc_addon_execute` function from `uc_blender_utils` module, and uninitializes `uc_asset_manager` module.

```
class ExportToCloudOperator(bpy.types.Operator):
...    
    def execute(self, context):
        from .uc_blender_utils import uc_addon_execute
        try:
            # prepare tags list
            tags = self.tags_input.split()
            # start asset data generation and uploading process
            uc_addon_execute(self.org_dropdown, self.project_dropdown, self.name_input, self.description_input,
                             tags_list=tags, generate_preview=self.generate_preview)
            self.report({'INFO'}, "Asset was uploaded to Unity Cloud Asset Manager")
        except Exception:
            self.report({'WARNING'}, "Failed to upload asset to Unity Cloud Asset Manager")
            raise
        finally:
            #  unitialize when upload is done
            from .uc_asset_manager import uninitialize
            uc_asset_manager.uninitialize()
        return {'FINISHED'}
```

### Asset data generation

The first step of asset creation in AM4B is FBX file and optional thumbnail generation. `uc_blender_utils` module creates a temporary folder on disk, saves the current scene as fbx and thumbnail (if user chose to) in this folder using Python and Blender API. Then the data is sent to `uc_asset_manager` to be uploaded. The temp directory and files will be deleted after the upload:

```
def _export_fbx(file_path):
    bpy.ops.export_scene.fbx(filepath=file_path)

def _get_preview_image(file_path):
    bpy.context.scene.render.resolution_x = 1024
    bpy.context.scene.render.resolution_y = 1024
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = file_path
    bpy.ops.render.render(write_still=True)
    
def uc_addon_execute(org_id: str, project_id: str, name: str, description: str, tags_list: List[str], generate_preview: bool):
    from .uc_asset_manager import export_file_with_preview
    temp_dir = tempfile.mkdtemp()

    temp_fbx_file = os.path.join(temp_dir, f"{name}.fbx")
    try:
        _export_fbx(temp_fbx_file)

        preview_file = None
        if generate_preview:
            preview_file = os.path.join(temp_dir, "thumbnail.png")
            _get_preview_image(preview_file)

        export_file_with_preview(temp_fbx_file, preview_file, name, description, tags_list, org_id, project_id)
    finally:
        shutil.rmtree(temp_dir)    
```

See [Blender Documentation. Export scene operators](https://docs.blender.org/api/current/bpy.ops.export_scene.html#module-bpy.ops.export_scene) and [Render Operators](https://docs.blender.org/api/current/bpy.ops.render.html#module-bpy.ops.render) for information about exporting scene and creating images in Blender.

### Asset data uploading

To upload a new asset to Asset Manager, `uc_asset_manager` creates a new asset in selected project, finds the default dataset and uploads the FBX file to the dataset. If user chose to generate a thumbnail, `uc_asset_manager` looks for "preview" dataset and uploads thumbnail to it. After files are uploaded, the add-on opens created asset in the system browser:

```
def export_file_with_preview(path: str, preview_path: str, name: str, description: str,
                             tags_list: List[str], org_id: str, project_id: str):
    # create asset                            
    asset_creation = AssetCreation(name,
                                   description,
                                   ucam.assets.asset_type.MODEL_3D,
                                   tags_list)

    asset_id = ucam.assets.create_asset(asset_creation, org_id, project_id)
    version = '1'
    # get the dataset of new asset
    datasets = ucam.assets.get_dataset_list(org_id, project_id, asset_id, version)
    # upload fbx file to default dataset
    upload_asset = AssetFileUploadInformation(org_id, project_id, asset_id, version, datasets[0].id, path)
    ucam.assets.upload_file(upload_asset)
    if preview_path is not None:
        #upload thumbnail to preview dataset
        upload_preview_file = AssetFileUploadInformation(org_id, project_id, asset_id,
                                                         version, datasets[1].id, preview_path)
        ucam.assets.upload_file(upload_preview_file)
    # open the asset in system browser
    ucam.interop.open_browser_to_asset_details(org_id, project_id, asset_id, version)
```

See [Unity Cloud Python SDK's Asset management documentation](https://docs.unity3d.com/docs-asset-manager/manual/python-sdk-managing_assets.html) for more information.

## See also

- [Asset Manager for Blender](../README.md)
- [Unity Cloud Python SDK documentation](https://docs.unity3d.com/docs-asset-manager/manual/python-sdk-index.html)
- [How to create your custom integration](https://docs.unity3d.com/docs-asset-manager/manual/integration-how-to-create-your-own.html)