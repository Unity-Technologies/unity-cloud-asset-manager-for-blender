import bpy
import tempfile
import os.path
import shutil
from typing import List
from bpy.types import Menu
from .uc_wheel_installation import install_unity_cloud
from . import uc_asset_manager

############### Constants

NO_PROJECT_VALUE = "-1"
CREATE_NEW_ASSET_VALUE = "-1"
NO_COLLECTION_VALUE = "-1"

DEFAULT_ASSET_NAME = "New asset"

############### Global variables

# What is displayed in the dropdowns
global_project_items = []
global_organization_items = []
global_assets_items = []
global_asset_versions_items = []
global_collections_items = []

# Internal cache
global_assets_cache = {}

# Cache of previously selected values
global_previous_org_id = None
global_previous_project_id = None
global_previous_asset_id = None
global_previous_asset_version_id = None


############### Blender hooks

def on_selected_org_changed(self, context):
    _refresh_projects(self, self.org_dropdown)
    self.project_dropdown = global_project_items[0][0]


def on_selected_project_changed(self, context):
    if (self.project_dropdown != None and self.project_dropdown != NO_PROJECT_VALUE):
        _refresh_assets(self, self.org_dropdown, self.project_dropdown)
        self.asset_dropdown = global_assets_items[0][0]
        _refresh_collections(self, self.org_dropdown, self.project_dropdown)
        self.collection_dropdown = global_collections_items[0][0]


def on_selected_asset_changed(self, context):
    if (self.asset_dropdown == CREATE_NEW_ASSET_VALUE):
        self.name_input = "New asset"
        self.description_input = ""
        self.tags_input = ""
    else:
        _refresh_asset_versions(self, self.org_dropdown, self.project_dropdown, self.asset_dropdown)
        self.version_dropdown = global_asset_versions_items[0][0]

        asset = global_assets_cache[self.asset_dropdown]
        self.name_input = asset.name
        self.description_input = asset.description if asset.description != None else ""
        tags = ""
        if asset.tags != None:
            for tag in asset.tags:
                tags += f'{tag} '
        self.tags_input = tags


def get_organizations(self, context):
    return global_organization_items


def get_projects(self, context):
    return global_project_items


def get_assets(self, context):
    return global_assets_items


def get_asset_versions(self, context):
    return global_asset_versions_items


def get_collections(self, context):
    return global_collections_items


############### Internal methods

def _refresh_orgs(self):
    global global_organization_items

    tmp_items = list()
    orgs = uc_asset_manager.get_organizations()
    for org in orgs:
        tmp_items.append((org.id, org.name, f"{org.name}. {org.id}"))
    global_organization_items = tmp_items


def _refresh_projects(self, org_id):
    global global_project_items

    if org_id != None:
        tmp_items = list()
        tmp_items.append((NO_PROJECT_VALUE, "<None>", ""))

        projects = uc_asset_manager.get_projects(org_id)
        for project in projects:
            tmp_items.append((project.id, project.name, f"{project.name}. {project.id}"))
        global_project_items = tmp_items
    else:
        global_project_items = [(NO_PROJECT_VALUE, "<None>", "")]


def _refresh_assets(self, org_id, project_id):
    global global_assets_items, global_assets_cache

    global_assets_cache = {}

    tmp_items = list()
    tmp_items.append((CREATE_NEW_ASSET_VALUE, "<Create new asset>", ""))
    try:
        assets = uc_asset_manager.get_assets(org_id, project_id)
        for asset in assets:
            if (asset.is_frozen):
                tmp_items.append((asset.id, asset.name, f"{asset.name}. {asset.id}"))
                global_assets_cache[asset.id] = asset
    except Exception as error:
        print(f"Failed to get asset list from the project {org_id}/{project_id}")
        print(error)
    global_assets_items = tmp_items


def _refresh_collections(self, org_id, project_id):
    global global_collections_items

    tmp_items = list()
    tmp_items.append((NO_COLLECTION_VALUE, "<None>", ""))
    try:
        collections = uc_asset_manager.list_collections(org_id, project_id)
        for collection in collections:
            tmp_items.append((collection.name, collection.name, collection.description))
    except Exception as error:
        print(f"Failed to get collection list from the project {org_id}/{project_id}")
        print(error)
    global_collections_items = tmp_items


def _refresh_asset_versions(self, org_id, project_id, asset_id):
    global global_asset_versions_items

    tmp_items = list()
    try:
        asset_versions = uc_asset_manager.get_asset_versions(org_id, project_id, asset_id)
        for asset in asset_versions:
            item_name = f"Ver.{asset.frozen_sequence_number}"
            if asset.parent_frozen_sequence_number != 0 and not asset.is_frozen:
                item_name = f"Ver.{asset.parent_frozen_sequence_number}-Pending-{asset.authoring_info.created}"

            tmp_items.append((asset.version, item_name, f"{asset.name}. v:{asset.version}"))
            tmp_items.sort(key=lambda x: x[1])
            tmp_items.reverse()
    except Exception as error:
        print(f"Failed to get version list for {org_id}/{project_id}/{asset_id}")
        print(error)
    global_asset_versions_items = tmp_items


def _contains_item(lst, item):
    return any(triple[0] == item for triple in lst)


def _publish_content_to_asset(org_id: str, project_id: str, asset_id: str, version: str, file_name: str,
                              embed_textures: bool):
    temp_dir = tempfile.mkdtemp()
    try:
        _publish_fbx_to_asset(temp_dir, org_id, project_id, asset_id, version, file_name, embed_textures)
        _publish_thumbnail_to_asset(temp_dir, org_id, project_id, asset_id, version)
    finally:
        shutil.rmtree(temp_dir)


def _publish_fbx_to_asset(temp_dir: str, org_id: str, project_id: str, asset_id: str, version: str, file_name: str,
                          embed_textures: bool):
    temp_fbx_file = os.path.join(temp_dir, f"{file_name}.fbx")

    path_mode = 'COPY' if embed_textures else 'AUTO'
    bpy.ops.export_scene.fbx(filepath=temp_fbx_file, path_mode=path_mode, embed_textures=embed_textures)

    uc_asset_manager.publish_payload(org_id, project_id, asset_id, version, "Source", file_name, temp_fbx_file)


def _publish_thumbnail_to_asset(temp_dir: str, org_id: str, project_id: str, asset_id: str, version: str):
    temp_thumbnail_file = os.path.join(temp_dir, "thumbnail.png")

    bpy.context.scene.render.resolution_x = 1024
    bpy.context.scene.render.resolution_y = 1024
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = temp_thumbnail_file
    bpy.ops.render.render(write_still=True)

    uc_asset_manager.publish_payload(org_id, project_id, asset_id, version, "Preview", "thumbnail", temp_thumbnail_file)


############### Defining the menus & operators

class LoginOperator(bpy.types.Operator):
    bl_idname = "uc_addon.addon_login"
    bl_label = "Login"
    bl_description = "Login to Asset Manager"

    def execute(self, context):
        uc_asset_manager.login()
        return {'FINISHED'}


class LogoutOperator(bpy.types.Operator):
    bl_idname = "uc_addon.addon_logout"
    bl_label = "Logout"
    bl_description = "Logout from Asset Manager"

    def execute(self, context):
        try:
            uc_asset_manager.logout()
        finally:
            global_previous_org_id = None
            global_previous_project_id = None
            global_previous_asset_id = None
            global_previous_asset_version_id = None
        return {'FINISHED'}


class UploadOperator(bpy.types.Operator):
    bl_idname = "uc_addon.addon_dialog"
    bl_label = "Upload FBX to Asset Manager"
    bl_description = "Create a new asset and upload current scene as *.fbx to Asset Manager"

    org_dropdown: bpy.props.EnumProperty(
        items=get_organizations,
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
        update=on_selected_asset_changed,
    )

    version_dropdown: bpy.props.EnumProperty(
        items=get_asset_versions,
        name="Version:",
        description="Select an asset version. If the selected version is frozen, a new one will be created",

    )

    name_input: bpy.props.StringProperty(name="Asset name:", default=DEFAULT_ASSET_NAME)
    description_input: bpy.props.StringProperty(name="Asset description:", default="")

    collection_dropdown: bpy.props.EnumProperty(
        items=get_collections,
        name="Collection:",
        description="Select a collection",
    )

    tags_input: bpy.props.StringProperty(name="Tags:", description="Asset tags separated by spaces: tag1 tag2",
                                         default="")

    embed_textures: bpy.props.BoolProperty(name="Embed textures",
                                           description="Embed texture in exported model and set path mode to COPY.",
                                           default=True)

    def execute(self, context):
        try:
            name = self.name_input.strip()
            tags = self.tags_input.split()
            collection = self.collection_dropdown
            if collection == NO_COLLECTION_VALUE:
                collection = None

            if (self.asset_dropdown == CREATE_NEW_ASSET_VALUE):
                asset = uc_asset_manager.create_asset(self.org_dropdown, self.project_dropdown, name)
            else:
                asset = uc_asset_manager.create_asset_version(self.org_dropdown, self.project_dropdown,
                                                              self.asset_dropdown, self.version_dropdown)

            uc_asset_manager.update_asset(self.org_dropdown, self.project_dropdown, asset.id, asset.version, name,
                                          self.description_input, tags, collection)
            _publish_content_to_asset(self.org_dropdown, self.project_dropdown, asset.id, asset.version, name,
                                      self.embed_textures)

            uc_asset_manager.freeze_asset(self.org_dropdown, self.project_dropdown, asset.id, asset.version)

            uc_asset_manager.open_asset_details(self.org_dropdown, self.project_dropdown, asset.id, asset.version)
        except Exception:
            self.report({'WARNING'}, "Failed to upload asset to Unity Cloud Asset Manager")
            raise
        finally:
            global global_previous_org_id, global_previous_project_id, global_previous_asset_id, global_previous_asset_version_id
            global_previous_org_id = self.org_dropdown
            global_previous_project_id = self.project_dropdown
            global_previous_asset_id = self.asset_dropdown
            global_previous_asset_version_id = self.version_dropdown
        return {'FINISHED'}

    def invoke(self, context, event):
        _refresh_orgs(self)

        # Try reuse the cached options from last session
        if _contains_item(global_organization_items, global_previous_org_id):
            self.org_dropdown = global_previous_org_id

            if _contains_item(global_project_items, global_previous_project_id):
                self.project_dropdown = global_previous_project_id

                if _contains_item(global_assets_items, global_previous_asset_id):
                    self.asset_dropdown = global_previous_asset_id

                    if _contains_item(global_asset_versions_items, global_previous_asset_version_id):
                        self.version_dropdown = global_previous_asset_version_id
        else:
            self.org_dropdown = global_organization_items[0][0]

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "org_dropdown", text="Organization")

        if (self.org_dropdown != None):
            layout.prop(self, "project_dropdown", text="Project")

            if (self.project_dropdown != None and self.project_dropdown != NO_PROJECT_VALUE):
                layout.prop(self, "asset_dropdown", text="Asset")

                if self.asset_dropdown != CREATE_NEW_ASSET_VALUE and len(global_asset_versions_items) > 0:
                    layout.prop(self, "version_dropdown", text="Version")

                layout.prop(self, "name_input", text="Asset name")
                layout.prop(self, "description_input", text="Asset description")
                layout.prop(self, "collection_dropdown", text="Collection")
                layout.prop(self, "tags_input", text="Tags")
                layout.prop(self, "embed_textures", text="Embed textures")


class DispatcherMenu(Menu):
    bl_idname = "VIEW3D_MT_UC_dispatcher"
    bl_label = "Unity Cloud"

    def draw(self, context):
        layout = self.layout

        if uc_asset_manager.is_logged_in():
            layout.operator(UploadOperator.bl_idname, text=UploadOperator.bl_label)
            layout.operator(LogoutOperator.bl_idname, text=LogoutOperator.bl_label)
        else:
            layout.operator(LoginOperator.bl_idname, text=LoginOperator.bl_label)


############### Registering the menus & operators

bl_info = {
    "name": "Upload FBX to Unity Cloud Asset Manager",
    "blender": (2, 93, 0),
    "description": "Exports current scene to *.fbx and publishes it as a new asset in Unity Cloud Asset Manager",
    "category": "Import-Export"
}

classes = (DispatcherMenu, UploadOperator, LoginOperator, LogoutOperator)


def draw_func(self, context):
    self.layout.menu(DispatcherMenu.bl_idname)


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
