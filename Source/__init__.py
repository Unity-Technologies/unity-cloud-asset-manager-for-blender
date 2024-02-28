import bpy
from bpy.types import Menu
from .uc_wheel_installation import install_unity_cloud


bl_info = {
    "name": "Upload FBX to Unity Cloud Asset Manager",
    "blender": (2, 93, 0),
    "description": "Exports current scene to *.fbx and publishes it as a new asset in Unity Cloud Asset Manager",
    "category": "Import-Export"
}


uc_dialog_op_name = "uc_addon.addon_dialog"
upload_fbx_lbl = "Upload FBX to Asset Manager"

uc_login_op_name = "uc_addon.addon_login"
login_lbl = "Login"

uc_logout_op_name = "uc_addon.addon_logout"
logout_lbl = "Logout"


class UC_Category(Menu):
    bl_idname = "VIEW3D_MT_UC_category"
    bl_label = "Unity Cloud"

    def draw(self, context):
        layout = self.layout
        from . import uc_asset_manager

        if not uc_asset_manager.is_initialized:
            uc_asset_manager.initialize()

        if uc_asset_manager.is_logged_in():
            layout.operator(uc_dialog_op_name, text=upload_fbx_lbl)
            layout.operator(uc_logout_op_name, text=logout_lbl)
        else:
            layout.operator(uc_login_op_name, text=login_lbl)


class LoginToCloudOperator(bpy.types.Operator):
    bl_idname = uc_login_op_name
    bl_label = login_lbl
    bl_description = "Login to Asset Manager"

    def execute(self, context):
        from . import uc_asset_manager
        uc_asset_manager.login()
        return {'FINISHED'}


class LogoutFromCloudOperator(bpy.types.Operator):
    bl_idname = uc_logout_op_name
    bl_label = logout_lbl
    bl_description = "Logout from Asset Manager"

    def execute(self, context):
        try:
            from . import uc_asset_manager
            uc_asset_manager.logout()
            uc_asset_manager.uninitialize()
        finally:
            global previous_org_id, previous_project_id, previous_asset_idx
            previous_org_id = None
            previous_project_id = None
            previous_asset_idx = None
        return {'FINISHED'}


def on_selected_org_changed(self, context):
    refresh_projects(self, context, self.org_dropdown)

    if len(project_items) > 0:
        self.project_dropdown = project_items[0][0]


def on_selected_project_changed(self, context):
    refresh_assets(self, context, self.org_dropdown, self.project_dropdown)

    if len(assets_items) > 0:
        self.asset_dropdown = assets_items[0][0]


project_items = []
organization_items = []
assets_items = []
assets = {}
previous_org_id = None
previous_project_id = None
previous_asset_idx = None


def refresh_orgs(self, context):
    from . import uc_asset_manager
    orgs = uc_asset_manager.get_organizations()
    items = list()
    for org in orgs:
        items.append((org.id, org.name, f"{org.name}. {org.id}"))
    global organization_items
    organization_items = items


def refresh_projects(self, context, org_id):
    from . import uc_asset_manager
    global project_items

    if org_id is not None:
        projects = uc_asset_manager.get_projects(org_id)
        items = list()
        for project in projects:
            items.append((project.id, project.name, f"{project.name}. {project.id}"))
        project_items = items
    else:
        project_items = []


def refresh_assets(self, context, org_id, project_id):
    from . import uc_asset_manager
    global assets_items, assets

    items = list()
    assets = {}

    if org_id is not None and project_id is not None:
        items.append((UploadToCloudOperator.CREATE_ASSET_VALUE, "<Create new asset>", ""))
        try:
            assets_array = uc_asset_manager.get_assets(org_id, project_id)
            for asset in assets_array:
                items.append((asset.id, asset.name, f"{asset.name}. {asset.id}"))
                assets[asset.id] = asset
        except Exception:
            print(f"Failed to get list from the project {org_id}/{project_id}")
    assets_items = items


def get_organization(self, context):
    return organization_items


def get_projects(self, context):
    return project_items


def get_assets(self, context):
    return assets_items


def on_asset_changed(self, context):
    if self.asset_dropdown == UploadToCloudOperator.CREATE_ASSET_VALUE:
        self.name_input = UploadToCloudOperator.DEFAULT_ASSET_NAME
        self.description_input = ""
        self.tags_input = ""
    else:
        global assets
        asset = assets[self.asset_dropdown]
        self.name_input = asset.name
        self.description_input = asset.description if asset.description is not None else ""
        tags = ""
        if asset.tags is not None:
            for tag in asset.tags:
                tags += f'{tag} '
        self.tags_input = tags


def contains_item(lst, item):
    return any(triple[0] == item for triple in lst)


class UploadToCloudOperator(bpy.types.Operator):
    bl_idname = uc_dialog_op_name
    bl_label = upload_fbx_lbl
    bl_description = "Create a new asset and upload current scene as *.fbx to Asset Manager"
    DEFAULT_ASSET_NAME = "New asset"
    CREATE_ASSET_VALUE = "-1"

    org_dropdown: bpy.props.EnumProperty(
        items=get_organization,
        name="Organization:",
        description="Select an organization",
        update=on_selected_org_changed,
    )
    project_dropdown: bpy.props.EnumProperty(
        items=get_projects,
        name="Project:",
        description="Select a project",
        update=on_selected_project_changed,
    )

    asset_dropdown: bpy.props.EnumProperty(
        items=get_assets,
        name="Asset:",
        description="Select an asset",
        update=on_asset_changed,
    )

    name_input: bpy.props.StringProperty(name="Asset name:", default=DEFAULT_ASSET_NAME)
    description_input: bpy.props.StringProperty(name="Asset description:", default="")
    tags_input: bpy.props.StringProperty(name="Tags:", description="Asset tags separated by spaces: tag1 tag2",
                                         default="")

    def execute(self, context):
        try:
            name = self.name_input.strip()
            tags = self.tags_input.split()
            from . import uc_blender_utils

            if self.asset_dropdown == self.CREATE_ASSET_VALUE:
                new_asset_id = uc_blender_utils.uc_create_asset(self.org_dropdown, self.project_dropdown,
                                                                name, self.description_input, tags)
                self.report({'INFO'}, "Asset was created and uploaded to Unity Cloud Asset Manager")
                refresh_assets(self, context, self.org_dropdown, self.project_dropdown)
                self.asset_dropdown = new_asset_id
            else:
                uc_blender_utils.uc_update_asset(self.org_dropdown, self.project_dropdown,
                                                 assets[self.asset_dropdown].id,
                                                 name, self.description_input, tags)
                self.report({'INFO'}, "Asset was updated in Unity Cloud Asset Manager")
        except Exception:
            self.report({'WARNING'}, "Failed to upload asset to Unity Cloud Asset Manager")
            raise
        finally:
            global previous_org_id, previous_project_id, previous_asset_idx
            previous_org_id = self.org_dropdown
            previous_project_id = self.project_dropdown
            previous_asset_idx = self.asset_dropdown
        return {'FINISHED'}

    def invoke(self, context, event):
        from . import uc_asset_manager
        if not (uc_asset_manager.is_initialized and uc_asset_manager.is_logged_in()):
            raise Exception("Invalid operation: uc_asset_manager must be initialized and logged in.")
        refresh_orgs(self, context)
        global organization_items, previous_org_id, previous_project_id
        if previous_org_id is not None and contains_item(organization_items, previous_org_id):
            self.org_dropdown = previous_org_id

            if contains_item(project_items, previous_project_id):
                self.project_dropdown = previous_project_id

                if contains_item(assets_items, previous_asset_idx):
                    self.asset_dropdown = previous_asset_idx
        else:
            self.org_dropdown = organization_items[0][0]

        return context.window_manager.invoke_props_dialog(self)


classes = (UC_Category, UploadToCloudOperator, LoginToCloudOperator, LogoutFromCloudOperator)


def draw_func(self, context):
    self.layout.menu(UC_Category.bl_idname)


def register():
    install_unity_cloud()
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_editor_menus.append(draw_func)

    from . import uc_asset_manager
    uc_asset_manager.initialize()


def unregister():
    from . import uc_asset_manager
    uc_asset_manager.uninitialize()

    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.VIEW3D_MT_editor_menus.remove(draw_func)


if __name__ == "__main__":
    register()
