# Technical overview

This document will describe the structure of the "Asset Manager for Blender", explain functionality of the main modules and functions used in this repository.

## Table of contents

- [Technical overview](#technical-overview)
  - [Table of contents](#table-of-contents)
  - [Add-on structure](#add-on-structure)
  - [Add-on registration](#add-on-registration)
  - [Installing Unity Cloud Python SDK in Blender's python runtime](#installing-unity-cloud-python-sdk-in-blenders-python-runtime)
  - [Initialization of Unity Cloud Python SDK](#initialization-of-unity-cloud-python-sdk)
  - [Interface](#interface)
    - [Add-on menu](#add-on-menu)
    - [Login](#login)
    - [Logout](#logout)
    - [Add-on dialog](#add-on-dialog)
  - [Listing organizations and projects](#listing-organizations-and-projects)
  - [Uploading data to Asset Manager](#uploading-data-to-asset-manager)
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
`uc_blender_utils` module provides methods to generate data, that can be uploaded to Asset Manager (FBX files).
`uc_asset_manager` module provides access to Asset Manager through Unity Cloud Python SDK.

## Add-on registration

`__init__.py` provides information that is required by Blender in order to display the add-on (see [Add-on Tutorial](https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html#what-is-an-add-on) and [Requirements for contributed Scripts](https://wiki.blender.org/wiki/Process/Addons/Guidelines) for details):
- `bl_info`: provides add-on name, description, category, minimum Blender version that the add-on is compatible with.
- `register()` function: initiates installation of Unity Cloud Python SDK in Blender environment, registers Blender operators and displays add-on as Blender scene menu item.
- `unregister()` function: unregisters operators and hides add-on menu item.

## Installing Unity Cloud Python SDK in Blender's python runtime

To install Unity Cloud Python SDK, `__init.py__.register()` executes `install_unity_cloud()` function of `uc_wheel_installation` module. The function identifies the current operating system, checks if it is supported by Unity Cloud Python SDK, selects an according Python wheel file in the add-on zip, and installs it using `pip` command.

## Initialization of Unity Cloud Python SDK

To initialize Unity Cloud Python SDK, `__init.py__.register()` executes `initialize()` function of `uc_asset_manager` module. The function initializes Unity Cloud Python SDK and configures it to use user login. This operation is performed when add-on was enabled, or when Blender starts.
To uninitialize, `__init.py__.unregister()` executes `uninitialize()` function of `uc_asset_manager` module. This operation is performed when add-on was disabled, or when Blender is closing.

## Interface

To define interface of AM4B `__init__.py` implements `UC_Category` and `UploadToCloudOperator` classes, and `draw_func()` function:
- `draw_func()` function displays add-on menu;
- `UC_Category` class describes add-on menu structure and defines menu items functionality;
- `LoginToCloudOperator` class describes functionality of "Login" menu item;
- `LogoutFromCloudOperator` class describes functionality of "Logout" menu item;
- `UploadToCloudOperator` class describes functionality of "Upload FBX to Asset Manager" menu item. 

These classes and function must be registered in Blender to display add-on when it is enabled, and unregistered to hide - when disabled.

### Add-on menu

Add-on menu items are defined with `UC_Category` class and `draw_func` function. See [Blender documentation. Menus](https://docs.blender.org/api/current/bpy.types.Menu.html#menu-bpy-struct) for more information about custom menus in Blender.
`draw_func` function is registered in Blender UI system to display menu structure, described in `UC_Category`, when add-on is enabled.

`UC_Category` class describes the add-on menu and sub-menu items. It provides labels for menu items and define what happens when clicked.

### Login

When `Unity Cloud`->`Login` menu is clicked, the add-on will try to perform login to Unity Asset Manager using Unity Cloud Python SDK `identity` module. This functionality is defined in `LoginToCloudOperator` class. See [Blender Documentation. Operators](https://docs.blender.org/api/current/bpy.ops.html) for more information about custom operators in Blender.  

### Logout

When `Unity Cloud`->`Logout` menu is clicked, the add-on will try to perform logout from Unity Asset Manager using Unity Cloud Python SDK `identity` module. This functionality is defined in `LogoutFromCloudOperator` class. See [Blender Documentation. Operators](https://docs.blender.org/api/current/bpy.ops.html) for more information about custom operators in Blender.

### Add-on dialog

When `Unity Cloud`->`Upload FBX to Asset Manager` menu is clicked, the `Upload FBX to Asset Manager` dialog opens. The UI and functionality of the dialog is defined by `UploadToCloudOperator` class. See [Blender Documentation. Operators](https://docs.blender.org/api/current/bpy.ops.html) for more information about custom operators in Blender.

See [Blender Documentation. Property definitions](https://docs.blender.org/api/current/bpy.props.html) and [Window Manager](https://docs.blender.org/api/current/bpy.types.WindowManager.html) for more details about custom dialogs in Blender.

## Listing organizations, projects and assets

As mentioned above, access to Asset Manager is provided by `uc_asset_manager` module which uses Unity Cloud Python SDK. The module should be initialized before usage, and uninitialized when it's not in use (See [Initialization of Unity Cloud Python SDK](#initialization-of-unity-cloud-python-sdk) for more information about initialization).
`UploadToCloudOperator` prepares the list of the available organizations, projects and assets.

## Uploading data to Asset Manager

When user clicks "OK", `UploadToCloudOperator.execute()` function is called. It gathers information from user input, and calls `uc_create_asset` or `uc_update_asset` function from `uc_blender_utils` module depending on selected options.

### Asset data generation

The first step of uploading to AM4B is FBX file. `uc_blender_utils` module creates a temporary folder on disk, saves the current scene as fbx in this folder using Python and Blender API. Then the data is sent to `uc_asset_manager` to be uploaded. The temp directory and files will be deleted after the upload:

See [Blender Documentation. Export scene operators](https://docs.blender.org/api/current/bpy.ops.export_scene.html#module-bpy.ops.export_scene) and [Render Operators](https://docs.blender.org/api/current/bpy.ops.render.html#module-bpy.ops.render) for information about exporting scene and creating images in Blender.

### Asset creation

If user chose to create a new asset, `uc_asset_manager.create_asset` will be executed. It creates a new asset in selected project using Unity Cloud Python SDK `assets` module.

### Asset update

If user chose to update an existing asset, `uc_asset_manager.update_asset` will be executed. It performs a request to update the selected asset with new information, and removes all the existing files from its datasets using Unity Cloud Python SDK `assets` module.

### Asset data uploading

After an asset is prepared for uploading new data, `uc_asset_manager` finds the default dataset and uploads the FBX file. After files are uploaded, the add-on opens the asset in the system browser using Unity Cloud Python SDK `interop` module.

## See also

- [Asset Manager for Blender](../README.md)
- [Unity Cloud Python SDK documentation](https://docs.unity.com/cloud/en-us/asset-manager/python-sdk)
- [How to create your custom integration](https://docs.unity.com/cloud/en-us/asset-manager/create-own-integration)
