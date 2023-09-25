from typing import List
from unity_cloud import interop as ucam
from unity_cloud.models import *
import os


__env_var_name = 'UNITY_CLOUD_SERVICES_ENV'
__env_variable: str

__provider_env_name = 'UNITY_CLOUD_SERVICES_DOMAIN_PROVIDER'
__provider_variable: str


def initialize():
    global __env_variable
    global __provider_variable

    __env_variable = os.getenv(__env_var_name)
    os.environ[__env_var_name] = 'Staging'

    __provider_variable = os.getenv(__provider_env_name)
    os.environ[__provider_env_name] = 'UnityServices'

    ucam.identity.initialize()
    ucam.assets.initialize()


def login():
    if ucam.identity.get_authentication_state() != ucam.identity.Authentication_State.LOGGED_IN:
        ucam.identity.login()


def logout():
    if ucam.identity.get_authentication_state() == ucam.identity.Authentication_State.LOGGED_IN:
        ucam.identity.logout(True)


def export_file(path: str, name: str, description: str, tags_list: List[str], org_id: str, project_id: str):
    asset_creation = Asset_Creation(name,
                                    description,
                                    ucam.assets.asset_type.MODEL_3D, tags_list)

    asset_id = ucam.assets.create_asset(asset_creation, org_id, project_id)
    version = '1'
    datasets = ucam.assets.get_dataset_list(org_id, project_id, asset_id, version)
    upload_asset = Asset_Upload_Information(org_id, project_id, asset_id, version, datasets[0].id, [path])
    ucam.assets.upload_file(upload_asset)
    ucam.assets.open_browser_to_asset_details(org_id, project_id, asset_id, version)


def get_organizations() -> List[Organization]:
    return ucam.assets.get_organization_list()


def get_projects(org_id: str) -> List[Project]:
    return ucam.assets.get_project_list(org_id)


def uninitialize():
    ucam.identity.dispose()
    ucam.assets.dispose()
    if __env_variable is not None:
        os.environ[__env_var_name] = __env_variable
    else:
        del os.environ[__env_var_name]

    if __provider_variable is not None:
        os.environ[__provider_env_name] = __provider_variable
    else:
        del os.environ[__provider_env_name]
