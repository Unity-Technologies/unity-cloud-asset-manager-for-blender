# Asset Manager for Blender

AM4 Blender add-on allows you to integrate Unity Cloud Asset Manager service within your [Blender](https://www.blender.org/) workflows.
This repository open sources the code of that add-on, so that you can get inspired by it or build on top of it - to create your own custom Asset Manager integration flows for Blender or any other software.

> **Note**: This repository does not accept pull requests, review requests, or any other GitHub-hosted issue management requests.

To connect and find support, join the [Help & Support page](https://cloud.unity.com/home/dashboard-support)!

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
    - [Login to Unity Cloud Asset Manager](#login-to-unity-cloud-asset-manager)
    - [Upload the 3D view as a new asset to Unity Cloud Asset Manager](#upload-the-3d-view-as-a-new-asset-to-unity-cloud-asset-manager)
    - [Upload the 3D view to an existing asset in Unity Cloud Asset Manager](#upload-the-3d-view-to-an-existing-asset-in-unity-cloud-asset-manager)
    - [Logout from Unity Cloud Asset Manager](#logout-from-unity-cloud-asset-manager)
  - [Troubleshooting](#troubleshooting)
    - [CERTIFICATE\_VERIFY\_FAILED when building the add-on on MacOS](#certificate_verify_failed-when-building-the-add-on-on-macos)
    - [Trouble when installing the addon](#trouble-when-installing-the-addon)
    - [Failed to upload asset - cannot render, no camera](#failed-to-upload-asset---cannot-render-no-camera)
    - [Security limitations](#security-limitations)
  - [See also](#see-also)
  - [Tell us what you think!](#tell-us-what-you-think)

## Prerequisites

### System requirements

To install and use the AM4 Blender add-on, you need:
- Blender installed on your machine (guaranteed support from versions 3.x to 4.1.x)
- The right permissions to use Asset Manager. See [Get Started with Asset Manager](https://docs.unity.com/cloud/en-us/asset-manager/get-started) for more details.

### Supported platforms

AM4 Blender is compatible with:

- Windows x64
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
5. Select the `UCAM4Blender.zip` file that you built, then select **Install Add-on**.
6. Check the checkbox to enable the add-on. The `Unity Cloud` tab appears in your 3D view.

![enabling the add-on](Documentation/Images/enable_addon.png)

### Login to Unity Cloud Asset Manager

Follow these steps if is the first time you run the add-on or you have previously logged out (See [Logout from Unity Cloud Asset Manager](#logout-from-unity-cloud-asset-manager) for information about logout). Otherwise, add-on will automatically log in using the previous session.
1. From your 3D view, go to **Unity Cloud** > **Login**.

![login-to-am](Documentation/Images/login.png)

> **Note**: You will be automatically redirected to the Unity login page. Make sure you complete the login process, until you are redirected to the following page.
> ![login complete](Documentation/Images/login_complete.png)

2. Go back to Blender.

### Upload the 3D view as a new asset to Unity Cloud Asset Manager

1. Ensure you are logged in to Asset Manager (See [Login to Unity Cloud Asset Manager](#login-to-unity-cloud-asset-manager) for more information about login).
2. From your 3D view, go to **Unity Cloud** > **Upload FBX to Asset Manager**.

![opening the add-on](Documentation/Images/open_addon.png)

3. You should now see the `Upload FBX to Asset Manager` popup.

![popup](Documentation/Images/popup.png)

4. Select a target organization and a project. If you don't have one, you can refer to the [create a new project guide](https://docs.unity.com/cloud/en-us/asset-manager/new-asset-manager-project).
5. Ensure `<Create new asset>` option is selected in `Asset` dropdown. 
6. Enter the new asset name, description, collection and tags. As part of the upload process, this information will be assigned to the asset.
> **Note**: To add multiple tags, simply separate them with a space in-between.
7. Check `Embed textures` option to export fbx with textures. This will set path mode to `COPY`, otherwise it will be set to `AUTO`.
8. Select **OK**.
> **Note**: Once the uploading is complete, you are automatically redirected to the Asset Manager dashboard, so that you can perform additional edit and publish operations from there.

### Upload the 3D view to an existing asset in Unity Cloud Asset Manager

1. Ensure you are logged in to Asset Manager (See [Login to Unity Cloud Asset Manager](#login-to-unity-cloud-asset-manager) for more information about login)
2. From your 3D view, go to **Unity Cloud** > **Upload FBX to Asset Manager**.

![opening the add-on](Documentation/Images/open_addon.png)

3. You should now see the `Upload FBX to Asset Manager` popup.

![popup](Documentation/Images/popup.png)

4. Select a target organization and a project. If you don't have one, you can refer to the [create a new project guide](https://docs.unity.com/cloud/en-us/asset-manager/new-asset-manager-project).
5. In `Asset` dropdown select the asset you want to update. Add-on will fetch asset name, asset versions, description and tags.
> **Note**: During uploading, any existing files in the asset will be removed.
6. Select the version you want to update. A new version will be created off of it.
7. Change the asset name, description, collection and tags, if needed. As part of the upload process, this information will be assigned to the asset.
> **Note**: To add multiple tags, simply separate them with a space in-between.

> **Note**: Selecting a collection will only ensure the asset is added to that collection. It will have no impact on any previously linked collection.
8. Check `Embed textures` option to export fbx with textures. This will set path mode to `COPY`, otherwise it will be set to `AUTO`.
9. Select **OK**.
> **Note**: Once the uploading is complete, you are automatically redirected to the Asset Manager dashboard, so that you can perform additional edit and publish operations from there.

### Logout from Unity Cloud Asset Manager

1. From your 3D view, go to **Unity Cloud** > **Logout**. Note, this option is only available when you are logged in.

![logout-from-am](Documentation/Images/logout.png)

> **Note**: Once logout completes, you will be automatically redirected to the following page.
> ![logout complete](Documentation/Images/logout_complete.png)

2. Go back to Blender.

## Troubleshooting

### CERTIFICATE_VERIFY_FAILED when building the add-on on MacOS

Part of the add-on building process requires to download the Unity Cloud Python SDK dependency.
Python 3.x does not rely on MacOS' openSSL ; it comes with its own openSSL bundled and doesn't have access on MacOS' root certificates.

To solve this issue, you have two options:

*1) Run an install command shipped with Python 3.x*
```
cd /Applications/Python\ 3.x/
./Install\ Certificates.command
```

*2) Install the certifi package*
```
pip install certifi
```

### Trouble when installing the addon

1. When installing the addon, there is an automatic process that tries to install the Unity Cloud Python SDK in Blender's integrated python environment. Depending on the setup, this step is prevented by the system and results in an exception (`Error: No module named 'unity_cloud'`).
For those use cases, running Blender with admin privileges might be necessary to make this step possible. Note that this will only be needed once at install time ; any subsequent session of Blender can run without elevated privileges.
2. If you are replacing an version of the addon with another, be sure to close Blender in between. Blender has a tendency to keep outdated code in memory even after you uninstall an addon, which will create conflicts with the new version.

### Failed to upload asset - cannot render, no camera

When uploading an asset, you might run into an error `Failed to upload asset to Unity Cloud Asset Manager`, with additional details `RuntimeError: Error: Cannot render, no camera`.
This error is thrown because AM4B uses the camera to render a preview before uploading the asset. If you don't have any camera on your scene, you'll need to add one.

### Security limitations

When building the add-on, the `-dw` option does not perform any integrity protection step while downloading the Unity Cloud Python SDK.

## See also

- [Technical overview of the add-on](Documentation/technical-overview.md)
- [Unity Cloud Python SDK documentation](https://docs.unity.com/cloud/en-us/asset-manager/python-sdk)

## Tell us what you think!

Thank you for taking a look at the project! To help us improve and provide greater value, please consider providing feedback in our [Help & Support page](https://cloud.unity.com/home/dashboard-support) about your experience with AM4 Blender. Thank you!