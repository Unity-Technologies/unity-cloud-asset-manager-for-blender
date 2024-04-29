import argparse
import os
import sys
import zipfile
from utils import *
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
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-dw', '--download', action="store_true", help='Download Unity Cloud Python SDK dependency')
    group.add_argument('-lw', '--local', default=wheels_path, nargs='?', help='Specify a local folder to copy the Unity Cloud Python SDK dependency from')
    parser.add_argument('-o', '--output', default=default_output, help='Specify a folder to save the addon archive in. By default, will create a `Dist` folder at the root of the repository.')
    systems_choices = ["windows", "macos", all_systems]
    parser.add_argument('-os', '--system', choices=systems_choices, required=False, default=all_systems, help='Specify target platform. By default "all".')
    return parser.parse_args()


if __name__ == '__main__':
    arguments = read_arguments()
    systems = list[OperationSystem]()
    zip_name: str
    if arguments.system == all_systems:
        systems.extend(list(OperationSystem))
        zip_name = default_name
    else:
        systems.append(OperationSystem[arguments.system])
        zip_name = f"{default_name}_{arguments.system}"

    current_directory = os.getcwd()
    my_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(my_directory)
    try:
        if os.path.exists(wheels_path) and (arguments.download or (arguments.local != wheels_path and arguments.local is not None)):
            shutil.rmtree(wheels_path)

        if arguments.download:
            if not download_wheels(wheels_path, systems, False):
                log_error("Failed to pack addon file: Could not download wheel files.");
                sys.exit(1)
        else:
            copy_from: str
            if arguments.local is None:
                copy_from = wheels_path
            else:
                copy_from = arguments.local

            full_copy_from = os.path.abspath(copy_from)
            if copy_from and not os.path.exists(full_copy_from):
                log_error(f"Failed to pack addon: The folder '{copy_from}' does not exist.")
                sys.exit(1)

            full_destination_path = os.path.abspath(wheels_path)
            if not copy_wheels(full_copy_from, full_destination_path, systems, True):
                log_error(f"Failed to pack addon: Not all wheel files can be found.")
                sys.exit(1)

        result = create_zip(addon_files, arguments.output, default_name, zip_name)
        log_ok(f"Addon zip file created: \"{os.path.abspath(result)}\"")
    finally:
        os.chdir(current_directory)
