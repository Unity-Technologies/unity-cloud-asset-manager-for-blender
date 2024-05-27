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


def __upload_file_to_dataset(org_id: str, project_id: str, asset_id: str, version: str, dataset_id: str, upload_file_path: str, cloud_file_path: str):
    upload_asset = FileUploadInformation(org_id, project_id, asset_id, version, dataset_id, upload_file_path, cloud_file_path)
    ucam.assets.upload_file(upload_asset)


def create_asset(path: str, name: str, description: str, tags_list: List[str], org_id: str,
                 project_id: str) -> str:
    asset_creation = AssetCreation(name, ucam.assets.AssetType.MODEL_3D, description, tags_list)

    asset = ucam.assets.create_asset(asset_creation, org_id, project_id)
    version = asset.version
    datasets = ucam.assets.get_dataset_list(org_id, project_id, asset.id, version)
    extension = pathlib.Path(path).suffix

    __upload_file_to_dataset(org_id, project_id, asset.id, version, datasets[0].id, path, name + extension)

    try:
        ucam.assets.freeze_asset_version(org_id, project_id, asset.id, version, "Initial version")
    except:
        pass
    ucam.interop.open_browser_to_asset_details(org_id, project_id, asset.id, version)
    return asset.id


def update_asset(path: str, name: str, description: str, tags_list: List[str], org_id: str, project_id: str,
                 asset_id: str, asset_version: str, is_frozen: bool):

    if is_frozen:
        asset_version = ucam.assets.create_unfrozen_asset_version(org_id, project_id, asset_id, asset_version).version

    asset_update = AssetUpdate(name,
                               ucam.assets.AssetType.MODEL_3D,
                               description,
                               tags_list)
    if ucam.assets.update_asset(asset_update, org_id, project_id, asset_id, asset_version):
        asset_dataset = ucam.assets.get_dataset_list(org_id, project_id, asset_id, asset_version)[0]

        file_list = ucam.assets.get_file_list(org_id, project_id, asset_id, asset_version, asset_dataset.id)
        for file in file_list:
            ucam.assets.remove_file(org_id, project_id, asset_id, asset_version, asset_dataset.id, file.path)

        extension = pathlib.Path(path).suffix
        __upload_file_to_dataset(org_id, project_id, asset_id, asset_version, asset_dataset.id, path, name + extension)
        ucam.assets.start_transformation(org_id, project_id, asset_id, asset_version, asset_dataset.id,
                                         ucam.models.WorkflowType.THUMBNAIL_GENERATION)

        try:
            ucam.assets.freeze_asset_version(org_id, project_id, asset_id, asset_version, "Updated model via Blender plugin")
        except:
            pass

    ucam.interop.open_browser_to_asset_details(org_id, project_id, asset_id, asset_version)


def get_organizations() -> List[Organization]:
    return ucam.identity.get_organization_list()


def get_projects(org_id: str) -> List[Project]:
    return ucam.identity.get_project_list(org_id)


def get_assets(org_id: str, project_id: str) -> List[Asset]:
    return ucam.assets.get_asset_list(org_id, project_id)


def get_asset_versions(org_id: str, project_id: str, asset_id: str) -> List[Asset]:
    return ucam.assets.search_asset_versions(org_id, project_id, asset_id)


def uninitialize():
    global is_initialized
    if is_initialized:
        ucam.uninitialize()
        is_initialized = False