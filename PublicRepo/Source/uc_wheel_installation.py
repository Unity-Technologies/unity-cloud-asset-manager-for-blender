import pip
import os
import platform
import glob


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


def __get_platform_name():
    system = platform.system().lower()
    machine = platform.machine().lower()
    return get_platform_name(system, machine)


def install_unity_cloud():
    print("Installing unity-cloud package...")

    wheels_folder = f"{os.path.dirname(os.path.abspath(__file__))}/wheels"
    matching_files = glob.glob(f"{wheels_folder}/unity_cloud*-py3-none-{__get_platform_name()}.whl")
    if len(matching_files) == 1:
        if pip.main(['install', matching_files[0], "--force-reinstall"]) == 0:
            print("unity-cloud package installed!")
    else:
        if len(matching_files) == 0:
            print("Failed to install unity-cloud package: wheel file for the current platform was not found")
        else:
            print("Failed to install unity-cloud package: More then one wheel file for the current platform was found")
