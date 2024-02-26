import bpy
import os.path
import tempfile
import shutil
from typing import List


def _export_fbx(file_path):
    bpy.ops.export_scene.fbx(filepath=file_path)


def _get_preview_image(file_path):
    bpy.context.scene.render.resolution_x = 1024
    bpy.context.scene.render.resolution_y = 1024
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = file_path
    bpy.ops.render.render(write_still=True)


def uc_create_asset(org_id: str, project_id: str, name: str, description: str, tags_list: List[str]) -> str:
    temp_dir = tempfile.mkdtemp()

    temp_fbx_file = os.path.join(temp_dir, f"{name}.fbx")
    try:
        _export_fbx(temp_fbx_file)

        from .uc_asset_manager import create_asset
        return create_asset(temp_fbx_file, name, description, tags_list, org_id, project_id)
    finally:
        shutil.rmtree(temp_dir)


def uc_update_asset(org_id: str, project_id: str, asset_id: str, name: str, description: str, tags_list: List[str]):
    temp_dir = tempfile.mkdtemp()
    temp_fbx_file = os.path.join(temp_dir, f"{name}.fbx")
    try:
        _export_fbx(temp_fbx_file)

        from . import uc_asset_manager
        uc_asset_manager.update_asset(temp_fbx_file, name, description, tags_list, org_id, project_id, asset_id)
    finally:
        shutil.rmtree(temp_dir)