import bpy
import os.path
import tempfile
import shutil
from typing import List


def _export_fbx(file_path):
    bpy.ops.export_scene.fbx(filepath=file_path)


def uc_addon_execute(org_id: str, project_id: str, name: str, description: str, tags_list: List[str]):
    from .uc_asset_manager import export_file
    temp_dir = tempfile.mkdtemp()

    temp_fbx_file = os.path.join(temp_dir, f"{name}.fbx")
    try:
        _export_fbx(temp_fbx_file)
        export_file(temp_fbx_file, name, description, tags_list, org_id, project_id)
    finally:
        shutil.rmtree(temp_dir)
