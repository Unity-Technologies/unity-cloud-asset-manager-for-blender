import argparse
import os
import sys
import zipfile
import shutil
from log_utils import *


default_output = "../Dist"
default_name = "UCAM4Blender"
source_folder = "../Source"
wheels_path = "../Source/wheels"
addon_files = [
    '__init__.py',
    'uc_blender_utils.py',
    'uc_asset_manager.py',
    'uc_wheel_installation.py',
    'wheels',
]


def add_file_to_zip(file_path, addon_folder, zip_file):
    if os.path.isdir(file_path):
        directory_path = file_path
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                full_file_path = os.path.join(root, file)
                if os.path.exists(full_file_path):
                    add_file_to_zip(full_file_path, addon_folder, zip_file)
    else:
        if os.path.exists(file_path):
            relative_path = os.path.relpath(file_path, start=source_folder)
            arc_file_name = os.path.join(addon_folder, relative_path)
            zip_file.write(file_path, arc_file_name)


def create_zip(files, output_directory, addon_name, zip_file_name):
    output_zip = os.path.join(output_directory, f"{zip_file_name}.zip")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    if os.path.exists(output_zip):
        os.remove(output_zip)
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files:
            source_file = os.path.join(source_folder, file_path)
            add_file_to_zip(source_file, addon_name, zipf)
    return output_zip


all_systems = "all"


def read_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', default=default_output, help='Specify a folder to save the addon archive in. By default, will create a `Dist` folder at the root of the repository.')
    return parser.parse_args()


if __name__ == '__main__':
    arguments = read_arguments()
    zip_name = default_name
    current_directory = os.getcwd()
    my_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(my_directory)
    try:
        result = create_zip(addon_files, arguments.output, default_name, zip_name)
        log_ok(f"Addon zip file created: \"{os.path.abspath(result)}\"")
    finally:
        os.chdir(current_directory)