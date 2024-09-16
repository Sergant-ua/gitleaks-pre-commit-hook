#!/usr/bin/env python3
import os
import platform
import subprocess
import sys
import zipfile
import tarfile
import shutil
import tempfile
import requests


def is_gitleaks_enabled():

    try:
        result = subprocess.run(
            ["git", "config", "--get", "hooks.gitleaks.enable"],
            capture_output=True,
            text=True
        )
        return result.stdout.strip() == "true"
    except Exception as e:
        print(f"Error checking git config: {e}")
        return False

def install_gitleaks():
    system = platform.system().lower()

    gitleaks_version = "8.18.4"
    
    if system == "windows":
        file_format = "zip"
        gitleaks_url = f"https://github.com/gitleaks/gitleaks/releases/download/v{gitleaks_version}/gitleaks_{gitleaks_version}_windows_x64.{file_format}"
        destination = f"gitleaks_{gitleaks_version}_windows_x64.{file_format}"
    elif system == "linux":
        file_format = "tar.gz"
        gitleaks_url = f"https://github.com/gitleaks/gitleaks/releases/download/v{gitleaks_version}/gitleaks_{gitleaks_version}_linux_x64.{file_format}"
        destination = f"gitleaks_{gitleaks_version}_linux_x64.{file_format}"
    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)

    temp_dir = tempfile.mkdtemp()
    gitleaks_path = os.path.join(temp_dir, destination)


    try:
        print(f"Downloading Gitleaks from {gitleaks_url}...")
        response = requests.get(gitleaks_url, stream=True)
        if response.status_code == 200:
            with open(gitleaks_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=128):
                    f.write(chunk)
        else:
            print(f"Failed to download Gitleaks: HTTP {response.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"Failed to download Gitleaks: {e}")
        sys.exit(1)


    if system == "windows":
        with zipfile.ZipFile(gitleaks_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
    elif system == "linux":
        with tarfile.open(gitleaks_path, 'r:gz') as tar_ref:
            tar_ref.extractall(temp_dir)


    gitleaks_bin = os.path.join(temp_dir, 'gitleaks')
    if system == "windows":
        gitleaks_bin += ".exe"
        install_path = os.path.join(os.environ['USERPROFILE'], 'bin')
    else:
        install_path = "/usr/local/bin"
    
    if not os.path.exists(install_path):
        os.makedirs(install_path)

    shutil.move(gitleaks_bin, install_path)
    print(f"Gitleaks installed successfully at {install_path}")


def run_gitleaks():
    try:
        print("Running Gitleaks...")

        subprocess.run(["gitleaks", "detect", "--report-path=leaks-report.json", "--report-format=json"], check=True)
        print("Gitleaks scan completed. Report saved as leaks-report.json")
    except subprocess.CalledProcessError:
        print("Gitleaks detected sensitive data!")
        sys.exit(1)

def main():
    if not is_gitleaks_enabled():
        print("Gitleaks is disabled. Skipping check.")
        sys.exit(0)

    if subprocess.call(["which", "gitleaks"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
        install_gitleaks()

    run_gitleaks()

if __name__ == "__main__":
    main()
