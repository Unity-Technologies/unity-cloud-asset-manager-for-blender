from .interop_model_base import Interop_Model_Base

class Asset_Info(Interop_Model_Base):
    def __init__(self):
        self.OrganizationId = None
        self.ProjectId = None
        self.AssetId = None
        self.Version = None
        self.Url = None

    def load_from_json(self, asset_info_json: dict):
        self.OrganizationId = asset_info_json.get("OrganizationId")
        self.ProjectId = asset_info_json.get("ProjectId")
        self.AssetId = asset_info_json.get("AssetId")
        self.Version = asset_info_json.get("Version")
        self.Url = asset_info_json.get("Url")

    def __str__(self):
        return f"OrganizationId: {self.OrganizationId} \n ProjectId: {self.ProjectId} \n AssetId: {self.AssetId} \n Version: {self.Version} \n Url: {self.Url}"
