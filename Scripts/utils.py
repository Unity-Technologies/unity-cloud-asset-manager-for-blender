import os.path
import shutil
import urllib.request
import re
import glob
from enum import Enum
from log_utils import *


class OperationSystem(Enum):
    windows = 'windows'
    macos = 'macos'


def get_platform_name(system: str, machine: str) -> str:
    name: str
    if system == "windows":
        if machine == "amd64" or machine == "x86_64":
            name = "win_amd64"
        elif machine == "arm64":
            name = "win_arm64"
    elif system == "darwin":
        name = "macosx_13_0_universal2"
    else:
        raise Exception(f"Unsupported configuration: {system}-{machine}")
    return name


operation_systems: dict[OperationSystem, dict[str, str]] = {
    OperationSystem.macos: {
        get_platform_name("darwin", ""):
        "https://drive.google.com/uc?id=1HLg8wfs7GZxzJkFgKZ8Mfi00ggbfkfd7&export=download",
    },

    OperationSystem.windows: {
        get_platform_name("windows", "amd64"):
        "https://drive.google.com/uc?id=1HWGO9Fp1-OcXdaCfPjQfjBcBZ3ur1EXM&export=download",

        get_platform_name("windows", "arm64"):
        "https://drive.google.com/uc?id=1HLpJ-SDXGzOhQinleyuNPXDufNrzEW2G&export=download"
    }
}


def copy_wheels(source_folder: str, destination_folder: str, systems: list[OperationSystem],
                skip_missing: bool) -> bool:
    if not os.path.exists(source_folder):
        return False
    else:
        os.makedirs(destination_folder, exist_ok=True)
        for system in systems:
            wheel_details = operation_systems[system]
            for platform_name in wheel_details:
                matching_files = glob.glob(f"{source_folder}/unity_cloud*-py3-none-{platform_name}.whl")
                if len(matching_files) == 0:
                    msg = f"Could not find wheel file for {platform_name}"
                    if skip_missing:
                        log_warning(msg)
                    else:
                        log_error(msg)
                        return False
                for source_file in matching_files:
                    destination_file = os.path.join(destination_folder, os.path.basename(source_file))
                    if source_file != destination_file:
                        shutil.copy(source_file, destination_file)
                        print(f"\"{source_file}\" copied to \"{destination_file}\"")
    return True


def __download_file(download_path: str, file_url: str) -> bool:
    try:
        response = urllib.request.urlopen(file_url)
    except Exception as err:
        log_error(f"Failed to download from {file_url}. Exception: {err}")
        return False

    if response.code != 200:
        log_error(f"Failed to download from {file_url}. Status code: {response.code}")
        return False

    if 'Content-Disposition' not in response.headers:
        log_error(f"Failed to download from {file_url}: Downloaded data has unexpected format")
        return False

    content_disposition = response.headers['Content-Disposition']
    filename_match = re.search(r'filename\*=(?:UTF-8\'\'|utf-8\'\'|\'\'|"")?([^\'"]+)', content_disposition)

    if not filename_match:
        log_error(f"Failed to download from {file_url}: Downloaded data has unexpected format")
        return False

    utf8_encoded_filename = filename_match.group(1)
    decoded_filename = utf8_encoded_filename
    with open(os.path.join(download_path, decoded_filename), "wb") as file:
        file.write(response.read())
    return True




def download_wheels(download_path: str, systems: list[OperationSystem], skip_missing: bool,
                    overwrite=False, write_log=True,) -> bool:
    os.makedirs(download_path, exist_ok=True)
    if write_log:
        print("Downloading unity-cloud wheel files...")
    for system in systems:
        wheel_details = operation_systems[system]
        for wheel_name in wheel_details:
            path = os.path.join(download_path, wheel_name)
            if not os.path.exists(path) or overwrite:
                if write_log:
                    print(f"Downloading wheel file for {wheel_name}...")
                if not __download_file(download_path,  wheel_details[wheel_name]):
                    if skip_missing:
                        continue
                    else:
                        return False
            else:
                print(f"Skipping \"{path}\". The file already exists")
    return True
