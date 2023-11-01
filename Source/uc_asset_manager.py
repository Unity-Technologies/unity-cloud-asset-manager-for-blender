from typing import List
import unity_cloud as ucam
from unity_cloud.models import *
import os


def initialize():
    ucam.initialize()
    ucam.identity.user_login.use()


def login():
    if ucam.identity.user_login.get_authentication_state() != ucam.identity.user_login.Authentication_State.LOGGED_IN:
        ucam.identity.user_login.login()


def logout():
    if ucam.identity.user_login.get_authentication_state() == ucam.identity.user_login.Authentication_State.LOGGED_IN:
        ucam.identity.user_login.logout(True)


def export_file(path: str, name: str, description: str, tags_list: List[str], org_id: str, project_id: str):
    asset_creation = AssetCreation(name,
                                    description,
                                    ucam.assets.asset_type.MODEL_3D, tags_list)

    asset_id = ucam.assets.create_asset(asset_creation, org_id, project_id)
    version = '1'
    datasets = ucam.assets.get_dataset_list(org_id, project_id, asset_id, version)
    upload_asset = AssetFileUploadInformation(org_id, project_id, asset_id, version, datasets[0].id, [path])
    ucam.assets.upload_file(upload_asset)
    ucam.interop.open_browser_to_asset_details(org_id, project_id, asset_id, version)


def get_organizations() -> List[Organization]:
    return ucam.identity.get_organization_list()


def get_projects(org_id: str) -> List[Project]:
    return ucam.identity.get_project_list(org_id)


def uninitialize():
    ucam.uninitialize()
