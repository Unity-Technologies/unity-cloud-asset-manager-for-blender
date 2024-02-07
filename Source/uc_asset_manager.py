from typing import List
import unity_cloud as ucam
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
    upload_asset = AssetFileUploadInformation(org_id, project_id, asset_id, version, dataset_id, upload_file_path, cloud_file_path)
    ucam.assets.upload_file(upload_asset)


def create_asset(path: str, preview_path: str, name: str, description: str,
                 tags_list: List[str], org_id: str, project_id: str) -> str:
    asset_creation = AssetCreation(name,
                                   description,
                                   ucam.assets.asset_type.MODEL_3D,
                                   tags_list)

    asset_id = ucam.assets.create_asset(asset_creation, org_id, project_id)
    version = '1'
    datasets = ucam.assets.get_dataset_list(org_id, project_id, asset_id, version)
    __upload_file_to_dataset(org_id, project_id, asset_id, version, datasets[0].id, path, name)
    if preview_path is not None:
        __upload_file_to_dataset(org_id, project_id, asset_id, version, datasets[1].id, preview_path, name + " Preview")
    ucam.interop.open_browser_to_asset_details(org_id, project_id, asset_id, version)
    return asset_id


def update_asset(path: str, preview_path: str, name: str, description: str,
                 tags_list: List[str], org_id: str, project_id: str, asset_id: str):
    version = '1'
    asset_update = AssetUpdate(name,
                               description,
                               ucam.assets.asset_type.MODEL_3D,
                               tags_list)
    if ucam.assets.update_asset(asset_update, org_id, project_id, asset_id, version):
        datasets = ucam.assets.get_dataset_list(org_id, project_id, asset_id, version)

        for asset_dataset in datasets:
            file_list = ucam.assets.get_file_list(org_id, project_id, asset_id, version, asset_dataset.id)
            for file in file_list:
                ucam.assets.remove_file(org_id, project_id, asset_id, version, asset_dataset.id, file.path)

        __upload_file_to_dataset(org_id, project_id, asset_id, version, datasets[0].id, path)
        if preview_path is not None:
            __upload_file_to_dataset(org_id, project_id, asset_id, version, datasets[1].id, preview_path)

    ucam.interop.open_browser_to_asset_details(org_id, project_id, asset_id, version)


def get_organizations() -> List[Organization]:
    return ucam.identity.get_organization_list()


def get_projects(org_id: str) -> List[Project]:
    return ucam.identity.get_project_list(org_id)


def get_assets(org_id: str, project_id: str) -> List[Asset]:
    return ucam.assets.get_asset_list(org_id, project_id)


def uninitialize():
    global is_initialized
    if is_initialized:
        ucam.uninitialize()
        is_initialized = False
