import sys
import subprocess


def install_unity_cloud():
    sdk_version = "0.10.3"
    install_command = [sys.executable, "-m", "pip", "install", "--index-url",
                        "https://unity3ddist.jfrog.io/artifactory/api/pypi/am-pypi-prod-local/simple",
                        f"unity-cloud=={sdk_version}"]
    subprocess.run(install_command, check=True)