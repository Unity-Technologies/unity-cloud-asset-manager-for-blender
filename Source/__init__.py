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
        from . import uc_asset_manager
        uc_asset_manager.logout()
        uc_asset_manager.uninitialize()
        return {'FINISHED'}


def on_selected_org_changed(self, context):
    refresh_projects(self.org_dropdown)


project_items = []
organization_items = []
previous_org_id = None
previous_project_id = None


def refresh_orgs():
    from . import uc_asset_manager
    orgs = uc_asset_manager.get_organizations()
    items = list()
    for org in orgs:
        items.append((org.id, org.name, f"{org.name}. {org.id}"))
    global organization_items
    organization_items = items


def refresh_projects(org_id):
    from . import uc_asset_manager
    if org_id is not None:
        projects = uc_asset_manager.get_projects(org_id)
        items = list()
        for project in projects:
            items.append((project.id, project.name, f"{project.name}. {project.id}"))
        global project_items
        project_items = items
    else:
        project_items = []


def get_organization(self, context):
    return organization_items


def get_projects(self, context):
    return project_items


class ExportToCloudOperator(bpy.types.Operator):
    bl_idname = uc_dialog_op_name
    bl_label = upload_fbx_lbl
    bl_description = "Create a new asset and upload current scene as *.fbx to Asset Manager"

    org_dropdown: bpy.props.EnumProperty(
            items=get_organization,
            name="Organization:",
            description="Select an organization",
            default=0,
            update=on_selected_org_changed,
        )
    project_dropdown: bpy.props.EnumProperty(
            items=get_projects,
            name="Project:",
            description="Select a project",
            default=0,
        )

    name_input: bpy.props.StringProperty(name="Asset name:", default="New asset")
    description_input: bpy.props.StringProperty(name="Asset description:", default="")
    tags_input: bpy.props.StringProperty(name="Tags:", description="Asset tags separated by spaces: tag1 tag2",
                                         default="")
    
    generate_preview: bpy.props.BoolProperty(name="Generate thumbnail", default=False)


    def execute(self, context):
        from .uc_blender_utils import uc_addon_execute
        try:
            tags = self.tags_input.split()
            uc_addon_execute(self.org_dropdown, self.project_dropdown, self.name_input, self.description_input,
                             tags_list=tags, generate_preview=self.generate_preview)
            self.report({'INFO'}, "Asset was uploaded to Unity Cloud Asset Manager")

            global previous_org_id, previous_project_id
            previous_org_id = self.org_dropdown
            previous_project_id = self.project_dropdown
        except Exception:
            self.report({'WARNING'}, "Failed to upload asset to Unity Cloud Asset Manager")
            raise
        return {'FINISHED'}

    def invoke(self, context, event):
        from . import uc_asset_manager
        if not (uc_asset_manager.is_initialized and uc_asset_manager.is_logged_in()):
            raise Exception("Invalid operation: uc_asset_manager must be initialized and logged in.")
        refresh_orgs()
        global organization_items, previous_org_id, previous_project_id
        if previous_org_id is not None:
            self.org_dropdown = previous_org_id
            self.project_dropdown = previous_project_id
        else:
            self.org_dropdown = organization_items[0][0]
            refresh_projects(organization_items[0][0])

        return context.window_manager.invoke_props_dialog(self)


classes = (UC_Category, ExportToCloudOperator, LoginToCloudOperator, LogoutFromCloudOperator)


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
