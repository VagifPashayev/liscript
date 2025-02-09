import os
import sys
import subprocess
from logger import log

# Resolve ADB path (adb.exe is expected in an "adb" subfolder next to the script)
BASE_PATH = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
ADB_PATH = os.path.join(BASE_PATH, "adb", "adb.exe")

def check_adb():
    """Checks whether ADB is available and working."""
    try:
        result = subprocess.run(
            [ADB_PATH, "version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        log(f"ADB found: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        log(f"Error starting ADB: {e.stderr.strip()}")
        return False
    except FileNotFoundError:
        log(f"File {ADB_PATH} not found. Check the path.")
        return False

def get_connected_devices():
    """Returns a list of connected ADB device serial numbers."""
    result = subprocess.run(f'"{ADB_PATH}" devices', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    lines = result.stdout.strip().split("\n")[1:]  # Skip the header line
    devices = [line.split("\t")[0] for line in lines if "device" in line]
    return devices

def get_users(device):
    """Returns a dict of user IDs and their display names for a device."""
    result = subprocess.run(f'"{ADB_PATH}" -s {device} shell pm list users', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    user_labels = {"0": "Main", "21473": "Passenger", "6174": "Rear"}
    users = {}
    for line in result.stdout.split("\n"):
        if "UserInfo{" in line and "}" in line:
            try:
                user_id = line.split("UserInfo{")[1].split(":")[0]  # Extract user ID only
                users[user_id] = user_labels.get(user_id, f"User {user_id}")
            except IndexError:
                log(f"Failed to parse line: {line}")
    return users

def check_monitor_type(users=None):
    """Detects monitor type from connected device and returns user count."""
    if users is None:
        devices = get_connected_devices()
        if not devices:
            log("No connected devices found")
            return 0
        users = get_users(devices[0])

    user_count = len(users)
    monitor_type = get_monitor_type_name(user_count)
    return user_count

def get_monitor_type_name(user_count):
    """Returns the monitor type name based on the number of users."""
    monitor_types = {
        1: "Pre-facelift — Rear monitor",
        2: "Pre-facelift — Main + Passenger",
        3: "Restyling — Main + Passenger + Rear"
    }
    return monitor_types.get(user_count, "Unknown monitor type")

def install_apk(apk_path, apk_name, device, users, package_name, install_permission, grant_permission, grant_screen, whitelist_doze):
    """Installs an APK on the specified device for the selected users."""
    log(f"Checking installation of {apk_name} on {device}...")
    uninstall_apk(device, package_name)
    log(f"Installing {apk_name} on {device} for selected users...")
    for user in users:
        command = f'"{ADB_PATH}" -s {device} install -r -g --user {user} "{apk_path}"'
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        log(result.stdout.strip())
        if result.stderr.strip():
            return log(f"Error: {result.stderr.strip()}")

    log(f"✅ {apk_name} installed successfully for selected users")

    if install_permission:
        for user in users:
            install_permission_command = f'"{ADB_PATH}" -s {device} shell appops set --user {user} {package_name} REQUEST_INSTALL_PACKAGES allow'
            subprocess.run(install_permission_command, shell=True)
            log(f"✅ REQUEST_INSTALL_PACKAGES permission granted for {apk_name} to user {user}")

    if grant_permission:
        permission_command = f'"{ADB_PATH}" -s {device} shell pm grant {package_name} android.permission.WRITE_SECURE_SETTINGS'
        subprocess.run(permission_command, shell=True)
        log(f"✅ WRITE_SECURE_SETTINGS permission granted for {apk_name}")

    if grant_screen:
        screen_command = f'"{ADB_PATH}" -s {device} shell pm grant {package_name} android.permission.SYSTEM_ALERT_WINDOW'
        subprocess.run(screen_command, shell=True)
        log(f"✅ SYSTEM_ALERT_WINDOW permission granted for {apk_name}")

    if whitelist_doze:
        whitelist_command = f'"{ADB_PATH}" -s {device} shell dumpsys deviceidle whitelist +{package_name}'
        subprocess.run(whitelist_command, shell=True)
        log(f"✅ {apk_name} added to Doze whitelist")

def uninstall_apk(device, package_name):
    """Checks if the app is installed; if so, stops, clears data, and uninstalls it."""

    # Check if the app is installed
    check_command = f'"{ADB_PATH}" -s {device} shell pm list packages | findstr {package_name}'
    result = subprocess.run(check_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if package_name in result.stdout:
        log(f"Package {package_name} found. Removing...")

        # Force-stop the process
        stop_command = f'"{ADB_PATH}" -s {device} shell am force-stop {package_name}'
        subprocess.run(stop_command, shell=True)

        # Clear app data
        clear_command = f'"{ADB_PATH}" -s {device} shell pm clear {package_name}'
        subprocess.run(clear_command, shell=True)

        # Uninstall the package
        uninstall_command = f'"{ADB_PATH}" -s {device} shell pm uninstall {package_name}'
        subprocess.run(uninstall_command, shell=True)

        log(f"Package {package_name} removed.")
        return True

    log(f"Package {package_name} is not installed.")
    return False

def disable_launchers(device):
    """Disables the Lixiang stock launchers on the device."""
    launchers = ["com.lixiang.psglauncher", "com.lixiang.newlauncher"]
    for launcher in launchers:
        disable_command = f'"{ADB_PATH}" -s {device} shell pm disable-user --user 0 {launcher}'
        subprocess.run(disable_command, shell=True)
        log(f"✅ {launcher} disabled for user 0")

def disable_qrcode(device):
    """Disables com.lixiang.provision for user 0."""
    disable_command = f'"{ADB_PATH}" -s {device} shell pm disable-user --user 0 com.lixiang.provision'
    subprocess.run(disable_command, shell=True)
    log("✅ com.lixiang.provision disabled for user 0")

def start_box715(device):
    """Launches box715 (LCT) on the device."""
    start_command = f'"{ADB_PATH}" -s {device} shell am start -n com.lixiang.car.lct/.MainActivity'
    subprocess.run(start_command, shell=True)
    log("✅ box715 started")

def set_timezone_baku(device):
    """Sets the device timezone to Asia/Baku."""
    timezone_command = f'"{ADB_PATH}" -s {device} shell service call alarm 3 s16 Asia/Baku'
    subprocess.run(timezone_command, shell=True)
    log("✅ Timezone set to Baku")
