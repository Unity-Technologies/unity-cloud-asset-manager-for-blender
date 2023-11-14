# Asset Manager for Blender

AM4 Blender add-on allows you to integrate Unity Cloud Asset Manager service within your [Blender](https://www.blender.org/) workflows.
This repository open sources the code of that add-on, so that you can get inspired by it or build on top of it - to create your own custom Asset Manager integration flows for Blender or any other software.

> **Note**: This repository does not accept pull requests, review requests, or any other GitHub-hosted issue management requests.

To connect and find support, join the [Unity forum](https://forum.unity.com/forums/unity-cloud.868/)!

## Table of contents
- [Asset Manager for Blender](#asset-manager-for-blender)
  - [Table of contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
    - [System requirements](#system-requirements)
    - [Supported platforms](#supported-platforms)
    - [Licenses](#licenses)
  - [How do I...?](#how-do-i)
    - [Build the add-on](#build-the-add-on)
    - [Install the add-on](#install-the-add-on)
    - [Publish the 3D view as an asset to Unity Cloud Asset Manager](#publish-the-3d-view-as-an-asset-to-unity-cloud-asset-manager)
  - [Troubleshooting](#troubleshooting)
    - [Security limitations](#security-limitations)
  - [See also](#see-also)
  - [Tell us what you think!](#tell-us-what-you-think)

## Prerequisites

### System requirements

To build the AM4 Blender add-on, you need Python 3.x installed on your machine.

To install and use the AM4 Blender add-on, you need:
- Blender 3.x installed on your machine
- The right permissions to use Asset Manager. See [Get Started with Asset Manager](https://docs.unity3d.com/docs-asset-manager/manual/get-started.html) for more details.

### Supported platforms

AM4 Blender is compatible with:

- Windows x64/Arm64
- Mac x64/Arm64

### Licenses

The Unity Cloud Asset Manager for Blender repository is made available under the [GPL v2 license](GPL-license.txt).

## How do I...?

### Build the add-on

Run the `pack-addon.py` script to create a ZIP file that can be installed in Blender as a plugin.

```
cd .\Scripts
python pack-addon.py (-dw | -lw [LOCAL]) [-n NAME] [-o OUTPUT] [-os {windows,macos,all}]
```

Option | Description
---|---
`-dw, --download` | Download Unity Cloud Python SDK dependency.
`-lw [LOCAL], --local [LOCAL]` | Specify a local folder to copy Unity Cloud Python SDK dependency from.
`-o OUTPUT, --output OUTPUT` | Specify a folder to save the add-on archive in. By default, will create a `Dist` folder at the root of the repository.
`-os {windows,macos,all}, --system {windows,macos,all}` | Specify target platform. By default `all`.

### Install the add-on

To install the add-on, follow these steps:

1. Open Blender.
2. Go to **Edit** > **Preferences**.
3. Go to the **Add-ons** section.
4. Select **Install**.
![installing the add-on](Documentation/Images/install_addon.png)
1. Select the `UCAM4Blender.zip` file that you built, then select **Install Add-on**.
2. Check the checkbox to enable the add-on. The `Unity Cloud` tab appears in your 3D view.
![enabling the add-on](Documentation/Images/enable_addon.png)

### Publish the 3D view as an asset to Unity Cloud Asset Manager

1. From your 3D view, go to **Unity Cloud** > **Upload FBX to Asset Manager**.
![opening the add-on](Documentation/Images/open_addon.png)

> **Note**: If this is the first time you run the add-on, you are automatically redirected to the Unity login page. Make sure you complete the login process, until you are redirected to the following page.
> ![login complete](Documentation/Images/login_complete.png)

1. Go back to Blender. You should now see the `Upload FBX to Asset Manager` popup.
![popup](Documentation/Images/popup.png)

1. Select a target organization and a project. If you don't have one, you can refer to the [add a new project guide](https://docs.unity3d.com/docs-asset-manager/manual/add-project.html).
2. Enter the asset name, description and tags. As part of the export process, these information will be assigned to the asset.
3. Select **OK**.

> **Note**: Once the export is complete, you are automatically redirected to the Asset Manager dashboard, so that you can perform additional edit and publish operations from there.

## Troubleshooting

### Security limitations

When building the add-on, the `-dw` option does not perform any integrity protection step while downloading the Unity Cloud Python SDK.

## See also

- [Technical overview of the add-on](Documentation/technical-overview.md)
- [Unity Cloud Python SDK documentation](https://docs.unity3d.com/docs-asset-manager/manual/python-sdk-index.html)

## Tell us what you think!

Thank you for taking a look at the project! To help us improve and provide greater value, please consider providing [feedback on our forum](https://forum.unity.com/forums/unity-cloud.868/) about your experience with AM4 Blender. Thank you!