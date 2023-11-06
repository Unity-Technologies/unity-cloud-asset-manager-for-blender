# Asset Manager for Blender

AM4 Blender add-on allows to integrate Unity Cloud Asset Manager service within your [Blender](https://www.blender.org/) workflows.
This repository open sources the code of that addon, so that you can inspire from it - or build on top of it - to create your own custom AM integration flows, be it for Blender or any other software.
This repository currently does not accept pull requests, review requests, or any other GitHub-hosted issue management requests.

To connect and find support, join the [Unity forum](https://forum.unity.com/forums/unity-cloud.868/) !

## Table of contents

- [Asset Manager for Blender](#asset-manager-for-blender)
  - [Table of contents](#table-of-contents)
    - [See also](#see-also)
  - [Overview](#overview)
    - [Supported platforms](#supported-platforms)
  - [How to build the add-on](#how-to-build-the-add-on)
    - [Prerequisites](#prerequisites)
    - [Building the add-on](#building-the-add-on)
  - [How to install and use the add-on](#how-to-install-and-use-the-add-on)
    - [Prerequisites](#prerequisites-1)
    - [Installing the add-on](#installing-the-add-on)
    - [Publishing the 3D view as an asset to the Unity Cloud Asset Manager](#publishing-the-3d-view-as-an-asset-to-the-unity-cloud-asset-manager)
  - [Troubleshooting](#troubleshooting)
    - [Security limitations](#security-limitations)
  - [License](#license)
  - [Tell us what you think!](#tell-us-what-you-think)

### See also

- [Technical overview of the addon](Documentation/technical-overview.md)
- [Python SDK documentation](TODO-placeholder)

## Overview

Once installed in your Blender environment, AM4 Blender provides a quick and easy flow to export your current scene as a new asset in the Unity Cloud Asset Manager.

### Supported platforms

AM4 Blender is currently compatible with:
- Windows x64/Arm64
- Mac x64/Arm64

## How to build the add-on

### Prerequisites

To build the add-on, you'll need:
- Python 3.x installed on your machine

### Building the add-on

Run the `pack-addon.py` script to create a zip-file that can be installed in Blender as a plugin.

```
cd .\Scripts
python pack-addon.py (-dw | -lw [LOCAL]) [-n NAME] [-o OUTPUT] [-os {windows,macos,all}]
```

Option | Description
---|---
-dw, --download | Download Unity Cloud Python SDK dependency.
-lw [LOCAL], --local [LOCAL] | Specify a local folder to copy the Unity Cloud Python SDK dependency from.
-o OUTPUT, --output OUTPUT | Specify a folder to save the addon archive in. By default, will create a `Dist` folder at the root of the repository.
-os {windows,macos,all}, --system {windows,macos,all} | Specify target platform. By default "all".

## How to install and use the add-on

### Prerequisites

To run the add-on, you'll need:
- A (Unity account)[TODO-placeholder] or a (Service account)[TODO-placeholder] to access Unity Cloud services
- Access to the Unity Cloud Asset Manager from the Unity Cloud Dashboard (TODO more details ?)
- Blender 3.x installed on your machine

### Installing the add-on

1. Open blender
2. Open the preferences window (Edit/Preferences)
3. Go to the Add-ons section
4. Click "install" button
![installing the addon](Documentation/Images/install_addon.png)
5. Select the `UCAM4Blender.zip` file that you built, then click "Install Add-on"
6. Enable the add-on by checking the checkbox ; you should see a new `Unity Cloud` tab in your view.
![enabling the addon](Documentation/Images/enable_addon.png)

### Publishing the 3D view as an asset to the Unity Cloud Asset Manager

1. From your 3D view, click on the `Unity Cloud` tab, then `Upload FBX to Asset Manager`
![opening the addon](Documentation/Images/open_addon.png)
2. If this is the first time you run the addon, you'll get automatically redirected to the Unity login page. Make sure you complete the login process, until you are redirected to the following page.
![login complete](Documentation/Images/login_complete.png)
3. Move back to Blender. You should now see the `Upload FBX to Asset Manager` popup.
![popup](Documentation/Images/popup.png)

4. Select a target organization and a project. If you don't have one, you can create them through [organization dashboard](https://id.unity.com/en/organizations) and [project dashboard](https://dashboard.unity3d.com/settings/projects).
5. Select an asset name, description and tags. Those will be the values assigned to the asset that will be created as part of the export process.
6. Click OK.
7. Once the export is complete, you will be automatically redirected to the Asset Manager dashboard, so that you can perform additional edit and publish operations from there.

## Troubleshooting

### Security limitations

When building the addon, the -dw option does not perform any integrity protection step while downloading the Unity Cloud Python SDK.
  
## License

The Unity Cloud Asset Manager for Blender repository is available under the [GPL v2 license](GPL-license.txt).
The Unity Cloud Python SDK that it relies on, however, is licensed under the [Unity Terms of Services](TODO-placeholder).

## Tell us what you think!

Thank you for taking a look at the project! To help us improve and provide greater value, please consider providing [feedback on our forum](https://forum.unity.com/forums/unity-cloud.868/) about your experience with AM4 Blender. Thank you!