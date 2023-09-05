from .interop_model_base import Interop_Model_Base

class User_Info(Interop_Model_Base):
    def __init__(self):
        self.Id = None
        self.Name = None
        self.Email = None
        self.Organizations = []
        self.LogoutUrl = None
        self.SessionExpiryTicks = 0
        self.License = License()
        self.Entitlements = []

    def load_from_json(self, user_info_json: dict):
        self.Id = user_info_json.get("Id")
        self.Name = user_info_json.get("Name")
        self.Email = user_info_json.get("Email")
        self.Organizations = self.__get_organizations(user_info_json.get("Organizations"))
        self.LogoutUrl = user_info_json.get("LogoutUrl")
        self.SessionExpiryTicks = int(user_info_json.get("SessionExpiryTicks"))
        self.License = License()
        self.License.load_from_json(user_info_json.get("License"))
        self.Entitlements = self.__get_entitlements(user_info_json.get("Entitlements"))
        
    def __get_organizations(self, organizations_json: dict):
        organizations = []
        for organization_json in organizations_json:
            org = Organization()
            org.load_from_json(organization_json)
            organizations.append(org)
        return organizations

    def __get_entitlements(self, entitlements_json: dict):
        entitlements = []
        for entitlement_json in entitlements_json:
            entitlement = Entitlement()
            entitlement.load_from_json(entitlement_json)
            entitlements.append(entitlement)
        return entitlements

    def __str__(self):
        return f"Id: {self.Id} \n Name: {self.Name} \n Email: {self.Email} \n Organizations: {self.Organizations[0]}"

class Organization(Interop_Model_Base):
    def __init__(self):
        self.Id = None
        self.Name = None
        self.AllowCreateNewProject = True
        self.IsPrimaryOrg = True
        self.AllowRequestLicense = True

    def load_from_json(self, organization_json: dict):
        self.Id = organization_json.get("Id")
        self.Name = organization_json.get("Name")
        self.AllowCreateNewProject = bool(organization_json.get("AllowCreateNewProject"))
        self.IsPrimaryOrg = bool(organization_json.get("IsPrimaryOrg"))
        self.AllowRequestLicense = bool(organization_json.get("AllowRequestLicense"))

    def __str__(self):
        return f"Id: {self.Id} \n Name: {self.Name}"

class License(Interop_Model_Base):
    def __init__(self):
        self.ExpiryTicks = 0
        self.Type = 0
        self.EntitlementId = None

    def load_from_json(self, license_json: dict):
        self.ExpiryTicks = int(license_json.get("ExpiryTicks"))
        self.Type = int(license_json.get("Type"))
        self.EntitlementId = license_json.get("EntitlementId")

class Entitlement(Interop_Model_Base):
    def __init__(self):
        self.ExpiryTicks = 0
        self.Type = 0
        self.EntitlementId = None

    def load_from_json(self, entitlement_json: dict):
        self.ExpiryTicks = int(entitlement_json.get("ExpiryTicks"))
        self.Type = int(entitlement_json.get("Type"))
        self.EntitlementId = entitlement_json.get("EntitlementId")
