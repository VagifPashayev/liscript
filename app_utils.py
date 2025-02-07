import os
import sys
import json

# Resolve base path for app assets
BASE_PATH = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
APPS_PATH = os.path.join(BASE_PATH, "apps")

def get_apps():
    """Scans the apps/ directory and returns a dict of app metadata."""
    apps = {}
    for app_folder in os.listdir(APPS_PATH):
        app_path = os.path.join(APPS_PATH, app_folder)
        if os.path.isdir(app_path):
            apk_files = [f for f in os.listdir(app_path) if f.endswith(".apk")]
            json_files = [f for f in os.listdir(app_path) if f.endswith(".txt")]
            if apk_files and json_files:
                json_path = os.path.join(app_path, json_files[0])
                with open(json_path, "r", encoding="utf-8") as json_file:
                    package_data = json.load(json_file)
                apps[app_folder] = {
                    "apk": os.path.join(app_path, apk_files[0]),
                    "package": package_data.get("package", "")
                }
    return apps

def get_app_path(app_name):
    """Returns the APK path and package name for a given app."""
    apps_data = get_apps()
    if app_name in apps_data:
        return apps_data[app_name]["apk"], apps_data[app_name]["package"]
    return None, None
