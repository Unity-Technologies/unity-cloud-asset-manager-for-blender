> [!IMPORTANT]<br /> **Deprecation notice**<br />
The Asset Manager for Blender add-on is deprecated and is no longer being actively developed or supported by Unity. The add-on doesn't support recent versions of Blender and won't receive future updates or bug fixes.<br />
**Recommended alternative**<br />
To integrate external digital content creation (DCC) tools with Unity Asset Manager, use the [Unity Cloud Python SDK](https://docs.unity.com/en-us/cloud/asset-manager/python-sdk) and the associated [Command-Line Interface (CLI) tool](https://github.com/Unity-Technologies/unity-cloud-python-sdk-samples/tree/main/bulk_upload_cli).

# Asset Manager for Blender

Use the Asset Manager for Blender (AM4B) add-on to integrate the Unity Cloud Asset Manager service within your [Blender](https://www.blender.org/) workflows.
The source code of the AM4B add-on is publicly exposed in this repository, providing inspiration and a foundation for you to create your own custom Asset Manager integration flows for Blender or any other software. That is, you can copy code blocks for your projects. However, you can't make open source contributions to the Unity AM4B repository on GitHub.

> **Note**: This repository does not accept pull requests, review requests, or any other GitHub-hosted issue management requests.

Find and connect support services on the [Help & Support](https://cloud.unity.com/home/dashboard-support) page.

## Table of contents
- [Asset Manager for Blender](#asset-manager-for-blender)
  - [Table of contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
    - [Before you start](#before-you-start)
    - [Supported platforms](#supported-platforms)
    - [Licenses](#licenses)
  - [How do I...?](#how-do-i)
    - [Build the AM4B add-on](#build-the-am4b-add-on)
    - [Install the AM4B add-on](#install-the-am4b-add-on)
    - [Sign in to Unity Cloud Asset Manager](#sign-in-to-unity-cloud-asset-manager)
    - [Upload the 3D view as a new asset to Unity Cloud Asset Manager](#upload-the-3d-view-as-a-new-asset-to-unity-cloud-asset-manager)
    - [Upload the 3D view to an existing asset in Unity Cloud Asset Manager](#upload-the-3d-view-to-an-existing-asset-in-unity-cloud-asset-manager)
    - [Sign out from the AM4B add-on](#sign-out-from-the-am4b-add-on)
  - [Troubleshooting](#troubleshooting)
    - [CERTIFICATE\_VERIFY\_FAILED when building the AM4B add-on on MacOS](#certificate_verify_failed-when-building-the-am4b-add-on-on-macos)
    - [Problem when installing the AM4B addon](#problem-when-installing-the-am4b-add-on)
       - [Error: No module named 'unity_cloud'](#error-no-module-named-unity_cloud)
       - [Conflicts after add-on replacement](#conflicts-after-add-on-replacement)
    - [Failed to upload asset - cannot render, no camera](#failed-to-upload-asset---cannot-render-no-camera)
    - [Security limitations](#security-limitations)
  - [See also](#see-also)
  - [Tell us what you think](#tell-us-what-you-think)

## Prerequisites

> **Note**: To manage assets, you need the [`Asset Manager Admin`](https://docs.unity.com/cloud/en-us/asset-manager/org-project-roles#organization-level-roles) role at the organization level or the [`Asset Manager Contributor`]( https://docs.unity.com/cloud/en-us/asset-manager/org-project-roles#project-level-roles) add-on role at the project level. Asset Manager Contributors can manage assets only for the specific projects to which they have access.

### Before you start

Before you install and use the AM4B add-on, make sure you have the following:
- Blender installed on your machine (guaranteed support from versions 3.x to 4.1.x)
- The required permissions. Read more about [verifying permissions](https://docs.unity.com/cloud/en-us/asset-manager/org-project-roles#verify-your-permissions).

   >  **Note**: Asset Manager roles define the permissions that you have for a single Asset Manager project. Depending on your work, permissions might vary across projects.

### Supported platforms

The AM4B add-on is compatible with the following platforms:

- Windows x64
- Mac x64/Arm64

### Licenses

The Unity Cloud Asset Manager for Blender repository is provided under the [GPL v2 license](GPL-license.txt).

## How do I...?

### Build the AM4B add-on

Run the `pack-addon.py` script to create a ZIP file that you can install in Blender as a plugin.

```
cd .\Scripts
python pack-addon.py [-o OUTPUT]
```

Option | Description
---|---
`-o OUTPUT, --output OUTPUT` | Specify a folder where you want to save the add-on archive. By default, if no output folder is specified, the script creates a `Dist` folder at the root of the repository.

### Install the AM4B add-on

To install the AM4B add-on, follow these steps:

1. Open Blender.
2. Go to **Edit** > **Preferences**.
3. Go to the **Add-ons** section.
4. Select **Install**.

![installing the add-on](Documentation/Images/install_addon.png)

5. Select the `UCAM4Blender.zip` file that you [built](#build-the-am4b-add-on).
6. Select **Install Add-on**.
7. To enable the add-on, select **Import Export: Upload FX to Unity Cloud Asset Manager**. The `Unity Cloud` tab appears in your 3D view.

![enabling the add-on](Documentation/Images/enable_addon.png)

### Sign in to Unity Cloud Asset Manager

Follow these steps if it is the first time you run the AM4B add-on or you have previously signed out. Read more about [signing out from the AM4B add-on](#sign-out-from-the-am4b-add-on). Otherwise, the AM4B add-on automatically signs in using the previous session.
1. From your 3D view, go to **Unity Cloud** > **Login**.

![login-to-am](Documentation/Images/login.png)

> **Note**: You are redirected to the Unity sign-in page. Complete the sign-in process, until it takes you to the following page:
>
> ![login complete](Documentation/Images/login_complete.png)

2. Go back to Blender.

### Upload the 3D view as a new asset to Unity Cloud Asset Manager

1. Sign in to Asset Manager. Read more about [signing in to Unity Cloud Asset Manager](#sign-in-to-unity-cloud-asset-manager).
2. From your 3D view, go to **Unity Cloud** > **Upload FBX to Asset Manager**.

![opening the add-on](Documentation/Images/open_addon.png)

3. Fill the fields of the `Upload FBX to Asset Manager` dialog as follows:

   ![popup](Documentation/Images/popup.png)

   1. Select a target organization and a project. If you don't have one, [create a new project](https://docs.unity.com/cloud/en-us/asset-manager/new-asset-manager-project).
   1. Select `<Create new asset>` in the `Asset` dropdown list. 
   1. Enter the new asset name, description, collection, and tags. As part of the upload process, the system assigns this information to the asset.
       > **Note**: To add multiple tags, separate them with spaces.
   1. Select `Embed textures` to upload textures along with the .fbx file. When you select `Embed textures`, the path mode changes to `COPY`. By default, path mode is set to `AUTO`.
   1. Select **OK**.
       > **Note**: When the upload is complete, you are redirected to the Asset Manager dashboard, where you can additionally edit and publish assets.

### Upload the 3D view to an existing asset in Unity Cloud Asset Manager

1. Sign in to Asset Manager. Read more about [signing in to Unity Cloud Asset Manager](#sign-in-to-unity-cloud-asset-manager).
2. From your 3D view, go to **Unity Cloud** > **Upload FBX to Asset Manager**.

![opening the add-on](Documentation/Images/open_addon.png)

3. Fill the fields of the `Upload FBX to Asset Manager` dialog as follows:

   ![popup](Documentation/Images/popup.png)

   1. Select a target organization and a project. If you don't have one, [create a new project](https://docs.unity.com/cloud/en-us/asset-manager/new-asset-manager-project).
   1. Select the asset that you want to update in the `Asset` dropdown list. The add-on fetches the asset name, asset versions, description, and tags of the selected asset.
       > **Note**: During upload, the system removes any existing files in the asset.
   1. Select the version you want to update. A new version is created from it.
   1. Change the asset name, description, collection, and tags, if needed. As part of the upload process, the system assigns this information to the asset.
       > **Note**: To add multiple tags, separate them with spaces.

       > **Note**: When you select a collection, it adds the asset only to that collection. It has no impact on any previously linked collection.
   1. Select `Embed textures` to export FBX with textures. This sets the path mode to `COPY`. By default, it is set to `AUTO`.
   1. Select **OK**.
       > **Note**: When the upload is complete, you are redirected to the Asset Manager dashboard, where you can additionally edit and publish assets.

### Sign out from the AM4B add-on

1. From your 3D view, go to **Unity Cloud** > **Logout**.
   >**Note** This option is available only when you are signed in.

![logout-from-am](Documentation/Images/logout.png)

> **Note**: When the sign-out process completes, you are redirected to the following page:
> 
> ![logout complete](Documentation/Images/logout_complete.png)

2. Go back to Blender.

## Troubleshooting

### CERTIFICATE_VERIFY_FAILED when building the AM4B add-on on MacOS

To build the AM4B add-on, you must download the Unity Cloud Python SDK dependency.
Python 3.x comes with its own bundled OpenSSL and doesn't rely on MacOS's OpenSSL. It doesn't have access to MacOS's root certificates either.

To solve this issue, use either of the following two methods:

* Run the install command that is shipped with Python 3.x.
   ```
   cd /Applications/Python\ 3.x/
   ./Install\ Certificates.command
   ```

* Install the certifi package.
   ```
   pip install certifi
   ```

### Problem when installing the AM4B add-on

#### `Error: No module named 'unity_cloud'`

During the AM4B add-on installation, an automatic process tries to install the Unity Cloud Python SDK in Blender's integrated Python environment. Depending on the setup, this step might be blocked by the system, which results in the following exception: `Error: No module named 'unity_cloud'`.

To solve this issue, allow automatic installation of the Unity Cloud Python SDK into Blender's integrated Python environment when running Blender with admin privileges. 

>**Note** Allowing this step is necessary only once at install time. Blender can run without elevated privileges in any subsequent session.

#### Conflicts after add-on replacement 

When you replace one version of the add-on with another, close Blender in between. Blender tends to keep outdated code in memory even after you uninstall an add-on, which might lead to conflicts with the new version.

### Failed to upload asset - cannot render, no camera

When you upload an asset, the system may throw this error:

* Error message: `Failed to upload asset to Unity Cloud Asset Manager`
* Additional details: `RuntimeError: Error: Cannot render, no camera`
The system throws this error because the AM4B add-on uses the camera to render a preview before uploading the asset. If you don't have any camera on your scene, add one.

### Security limitations

When you build the AM4B add-on, if you want to skip the integrity protection step during the download of the Unity Cloud Python SDK, use the `-dw` option.

## See also

- [Technical overview of the add-on](Documentation/technical-overview.md)
- [Unity Cloud Python SDK documentation](https://docs.unity.com/cloud/en-us/asset-manager/python-sdk)

## Tell us what you think

Thank you for exploring our project! Please help us improve and deliver greater value by providing your feedback about your experience with the AM4B add-on in our [Help & Support](https://cloud.unity.com/home/dashboard-support) page. We appreciate your input!
