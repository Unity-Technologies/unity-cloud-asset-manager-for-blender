import unity_cloud as ucam
import pathlib

from typing import List
from unity_cloud.models import *

is_initialized = False


def initialize():
    global is_initialized
    if not is_initialized:
        ucam.initialize()
        ucam.identity.user_login.use()
        is_initialized = True


def is_logged_in():
    return ucam.identity.user_login.get_authentication_state() == ucam.identity.user_login.Authentication_State.LOGGED_IN


def login():
    if ucam.identity.user_login.get_authentication_state() != ucam.identity.user_login.Authentication_State.LOGGED_IN:
        ucam.identity.user_login.login()


def logout():
    if ucam.identity.user_login.get_authentication_state() == ucam.identity.user_login.Authentication_State.LOGGED_IN:
        ucam.identity.user_login.logout(True)


def create_asset(org_id: str, project_id: str, name: str):
    asset_creation = AssetCreation(name, ucam.assets.AssetType.MODEL_3D)
    return ucam.assets.create_asset(asset_creation, org_id, project_id)


def create_asset_version(org_id: str, project_id: str, asset_id: str, parent_version: str):
    return ucam.assets.create_unfrozen_asset_version(org_id, project_id, asset_id, parent_version)


def update_asset(org_id: str, project_id: str, asset_id: str, version: str, name: str, description: str,
                 tags: List[str], collection: str):
    asset_update = AssetUpdate(name, ucam.assets.AssetType.MODEL_3D, description, tags)
    ucam.assets.update_asset(asset_update, org_id, project_id, asset_id, version)

    if (collection != None):
        ucam.assets.link_assets_to_collection(org_id, project_id, collection, [asset_id])


def publish_payload(org_id: str, project_id: str, asset_id: str, version: str, dataset_tag: str, file_name: str, path: str):
    dataset_list = ucam.assets.get_dataset_list(org_id, project_id, asset_id, version)

    dataset = next(d for d in dataset_list if dataset_tag in d.system_tags)

    # Remove any pending file
    file_list = ucam.assets.get_file_list(org_id, project_id, asset_id, version, dataset.id)
    for file in file_list:
        ucam.assets.remove_file(org_id, project_id, asset_id, version, dataset.id, file.path)

    extension = pathlib.Path(path).suffix
    upload_asset = FileUploadInformation(org_id, project_id, asset_id, version, dataset.id, path,
                                         file_name + extension)
    ucam.assets.upload_file(upload_asset, disable_automatic_transformations=True)


def freeze_asset(org_id: str, project_id: str, asset_id: str, version: str):
    ucam.assets.freeze_asset_version(org_id, project_id, asset_id, version, "Updated model via Blender plugin")


def open_asset_details(org_id: str, project_id: str, asset_id: str, version: str):
    ucam.interop.open_browser_to_asset_details(org_id, project_id, asset_id, version)


def get_organizations() -> List[Organization]:
    return ucam.identity.get_organization_list()


def get_projects(org_id: str) -> List[Project]:
    return ucam.identity.get_project_list(org_id)


def get_assets(org_id: str, project_id: str) -> List[Asset]:
    return ucam.assets.get_asset_list(org_id, project_id)


def list_collections(org_id: str, project_id: str) -> List[Collection]:
    return ucam.assets.list_collections(org_id, project_id)


def get_asset_versions(org_id: str, project_id: str, asset_id: str) -> List[Asset]:
    return ucam.assets.search_versions_in_asset(org_id, project_id, asset_id)


def uninitialize():
    global is_initialized
    if is_initialized:
        ucam.uninitialize()
        is_initialized = False
