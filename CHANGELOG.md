# Changelog
All notable changes to this package will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.6.0] - 2024-07-18

### Added
- Ability to select a collection at publish time, to automatically link the asset to.

### Changed
- When selecting an organization, the first project in it is no longer selected by default. Thus preventing loading a project' assets when selecting an organization.
- Refactored the content of the Source folder to improve readability and clarity
- At publish time, asset is now automatically frozen.
- Thumbnail is published locally temporarily (as we disabled the transformation)

## [0.5.0] - 2024-05-23

### Added
- Add version selection whenever an asset is being updated.

### Changed
- Upgraded Python SDK dependency to 0.8.2.

## [0.4.0] - 2024-04-19

### Fixed
- Fix new assets creation failing due to the new assets versioning.

## [0.3.0] - 2024-03-14

### Added
- Added `embed textures` checkbox to `Unity Cloud` menu
- Added a preview re-generation when an asset is updated.

### Changed
- AM4B is now using Unity Cloud Python SDK 0.6.0

## [0.2.0] - 2024-02-22

### Added
- Added `Login` and `Logout` buttons to `Unity Cloud` menu.
- Added functionality to select and update an asset in current project.
- Leading and trailing spaces in asset name input string are now removed to comply with validation rules.

### Fixed
- Plugin now recalls previously selected organization and project ids.
- Plugin recalls previously selected organization, project and asset ids only if they are available.
- Removed reference to `InteropException`.

### Changed
- Updated a few URLs in the documentation.
- `unity-cloud` is initialized/uninitialized on add-on registration/unregistration.
- Previously selected organization, project and asset ids are reset after logging out.
- AM4B is now using Unity Cloud Python SDK 0.5.0

### Removed
- Removed the `generate preview` checkbox since previews are now automatically generated for an asset created with a single `.fbx` file.

## [0.1.1] - 2023-11-30

### Changed
- AM4B is now using Unity Cloud Python SDK 0.2.2

## [0.1.0] - 2023-11-15

Initial release

Features:
- Source code of "Asset Manager for Blender" add-on that demonstrates how to:
    - install Unity Cloud Python SDK in integration environment;
    - initialize and uninitialize unity-cloud package;
    - login to Asset Manager using Unity Cloud Python SDK;
    - create new asset and upload data to it.
- Python script to create a ready-to-install Blender add-on.