import tkinter as tk
from tkinter import ttk
import sys
from adb_utils import check_adb, get_connected_devices, get_users, install_apk, uninstall_apk, check_monitor_type, get_monitor_type_name, disable_launchers, disable_qrcode, start_box715, set_timezone_baku
from app_utils import get_apps, get_app_path
from logger import logger, log

def update_monitor_label():
    """Updates the monitor type label."""
    user_count = check_monitor_type(users)
    monitor_type = get_monitor_type_name(user_count)
    monitor_label.config(text=f"Current monitor: {monitor_type}")
    log("Info updated.")

def install_selected_app():
    selected_app = app_var.get()
    selected_device = device_var.get()
    selected_users = [user_id for user_id, var in user_checkboxes.items() if var.get()]
    install_permission = install_permission_var.get()
    grant_permission = permission_var.get()
    grant_screen = screen_var.get()
    whitelist_doze = doze_var.get()

    if not selected_app or not selected_device or not selected_users:
        log("Please select an app, a device, and at least one user")
        return

    app_data = apps.get(selected_app, None)
    if not app_data:
        log(f"APK not found for {selected_app}")
        return

    apk_path = app_data["apk"]
    package_name = app_data["package"]

    install_apk(apk_path, selected_app, selected_device, selected_users, package_name, install_permission, grant_permission, grant_screen, whitelist_doze)

    install_permission_var.set(False)
    permission_var.set(False)
    screen_var.set(False)
    doze_var.set(False)

def install_store():
    log("Installing app store...")
    apk_path, package_name = get_app_path("LiAppStore")
    if apk_path and package_name:
        install_apk(apk_path, "LiAppStore", device_var.get(), users, package_name, True, False, False, False)
    else:
        log("Folder not found: LiAppStore")

    apk_path, package_name = get_app_path("Apkpure")
    if apk_path and package_name:
        install_apk(apk_path, "Apkpure", device_var.get(), users, package_name, True, False, False, False)
    else:
        log("Folder not found: Apkpure")

def install_buttons():
    log("Installing buttons...")
    apk_path, package_name = get_app_path("LiSWMB___Кнопки")
    if apk_path and package_name:
        if user_count > 1:
            install_apk(apk_path, "LiSWMB___Кнопки", device_var.get(), ["0"], package_name, True, True, False, False)
        else:
            log("Cannot install Buttons on the rear screen.")
    else:
        log("Folder not found: LiSWMB___Кнопки")

def install_hud():
    log("Installing HUD...")
    apk_path, package_name = get_app_path("Lixiang_Tweaks")
    if apk_path and package_name:
        if user_count > 1:
            install_apk(apk_path, "Lixiang_Tweaks", device_var.get(), ["0"], package_name, False, False, False, False)
        else:
            log("Cannot install Lixiang_Tweaks on the rear screen.")
    else:
        log("Folder not found: Lixiang_Tweaks")

def install_patch():
    log(f"Installing patch 7.0 ({monitor_type}) ...")
    if user_count == 3:
        apk_path, package_name = get_app_path("Patch_Rest")
        if apk_path and package_name:
                install_apk(apk_path, "Patch_Rest", device_var.get(), ["0"], package_name, False, False, False, False)
        else:
            log("Folder not found: Patch_Rest")
    else:
        apk_path, package_name = get_app_path("Patch_Dorest")
        if apk_path and package_name:
                install_apk(apk_path, "Patch_Dorest", device_var.get(), ["0"], package_name, False, False, False, False)
        else:
            log("Folder not found: Patch_Dorest")

def install_swiftkey():
    log("Installing Microsoft_SwiftKey...")
    apk_path, package_name = get_app_path("Microsoft_SwiftKey")
    if apk_path and package_name:
        install_apk(apk_path, "Microsoft_SwiftKey", device_var.get(), users, package_name, False, False, False, False)
    else:
        log("Folder not found: Microsoft_SwiftKey")

def install_trash():
    log("Installing Корзина...")
    apk_path, package_name = get_app_path("Корзина")
    if apk_path and package_name:
        install_apk(apk_path, "Корзина", device_var.get(), users, package_name, False, False, False, False)
    else:
        log("Folder not found: Корзина")

def install_messages():
    log("Installing Messages...")
    apk_path, package_name = get_app_path("Messages")
    if apk_path and package_name:
        if user_count > 1:
            install_apk(apk_path, "Messages", device_var.get(), ["0"], package_name, False, False, False, False)
        else:
            log("Cannot install Messages on the rear screen.")
    else:
        log("Folder not found: Messages")

def install_asupport():
    log("Installing aSupport...")
    apk_path, package_name = get_app_path("aSupport")
    if apk_path and package_name:
        if user_count > 1:
            install_apk(apk_path, "aSupport", device_var.get(), ["0"], package_name, False, False, False, False)
        else:
            log("Cannot install aSupport on the rear screen.")
    else:
        log("Folder not found: aSupport")

def install_passengerscreen():
    log("Installing Экран_пассажира...")
    apk_path, package_name = get_app_path("Экран_пассажира")
    if apk_path and package_name:
        if user_count > 1:
            install_apk(apk_path, "Экран_пассажира", device_var.get(), ["0"], package_name, False, False, False, False)
        else:
            log("Cannot install Экран_пассажира on the rear screen.")
    else:
        log("Folder not found: Экран_пассажира")

def install_youtube():
    log("Installing YouTube_AnyApp...")
    apk_path, package_name = get_app_path("YouTube_AnyApp")
    if apk_path and package_name:
        install_apk(apk_path, "YouTube_AnyApp", device_var.get(), users, package_name, False, False, False, False)
    else:
        log("Folder not found: YouTube_AnyApp")

def install_waze():
    log("Installing Waze...")
    apk_path, package_name = get_app_path("Waze")
    if apk_path and package_name:
        if user_count > 1:
            install_apk(apk_path, "Waze", device_var.get(), ["0"], package_name, False, False, False, False)
        else:
            log("Cannot install Waze on the rear screen.")
    else:
        log("Folder not found: Waze")

def install_lalauncher():
    log("Installing LAAuncher...")
    apk_path, package_name = get_app_path("LAAuncher")
    if apk_path and package_name:
        install_apk(apk_path, "LAAuncher", device_var.get(), ["0"], package_name, False, False, False, False)
        disable_launchers(device_var.get())
    else:
        log("Folder not found: LAAuncher")

def install_additional_apps():
    install_swiftkey()
    install_trash()
    install_messages()
    install_asupport()
    install_passengerscreen()
    install_youtube()
    install_waze()
    install_lalauncher()

def install_standard_set():
    """Installs the standard application package."""
    log("Installing standard application package...")
    install_store()
    install_buttons()
    install_hud()
    install_additional_apps()
    log("✅ Standard package installation complete.")

if __name__ == "__main__":
    if not check_adb():
        sys.exit(1)

    devices = get_connected_devices()
    apps = get_apps()
    users = get_users(devices[0]) if devices else {}
    user_count = check_monitor_type(users)
    monitor_type = get_monitor_type_name(user_count)

    root = tk.Tk()
    root.title("APK Installer")
    root.geometry("900x700")
    root.configure(bg="#f0f0f0")

    top_frame = tk.Frame(root, bg="#f0f0f0", height=60)
    top_frame.pack(side=tk.TOP, fill=tk.X)

    tk.Label(top_frame, text="Lixiang Script By Vagif", bg="#f0f0f0", font=("Arial", 14, "bold")).pack(pady=5)

    # Label to display current monitor type
    monitor_label = tk.Label(top_frame, text="", bg="#f0f0f0", font=("Arial", 12))
    monitor_label.pack(pady=5)

    update_monitor_label()  # Initialize on startup

    update_button = tk.Button(top_frame, text="Refresh Monitor", command=update_monitor_label, bg="#CCCCCC", font=("Arial", 10))
    update_button.pack()

    content_frame = tk.Frame(root, bg="#f0f0f0")
    content_frame.pack(fill=tk.BOTH, expand=True)

    left_frame = tk.Frame(content_frame, bg="#f0f0f0")
    left_frame.pack(side=tk.LEFT, padx=10, pady=30, fill=tk.BOTH, expand=True)

    right_frame = tk.Frame(content_frame, bg="#f0f0f0")
    right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    tk.Label(left_frame, text="Select device:", bg="#f0f0f0", font=("Arial", 12)).pack()
    device_var = tk.StringVar()
    device_dropdown = ttk.Combobox(left_frame, textvariable=device_var, values=devices, state="readonly")
    device_dropdown.pack()
    if devices:
        device_dropdown.current(0)

    tk.Label(left_frame, text="Select users:", bg="#f0f0f0", font=("Arial", 12)).pack()
    user_checkboxes = {}
    for user_id, user_label in users.items():
        var = tk.BooleanVar(value=(user_id == "0"))
        chk = tk.Checkbutton(left_frame, text=user_label, variable=var, bg="#f0f0f0")
        chk.pack()
        user_checkboxes[user_id] = var

    tk.Label(left_frame, text="Select app:", bg="#f0f0f0", font=("Arial", 12)).pack()
    app_var = tk.StringVar()
    app_dropdown = ttk.Combobox(left_frame, textvariable=app_var, values=list(apps.keys()), state="readonly")
    app_dropdown.pack()
    if apps:
        app_dropdown.current(0)

    install_permission_var = tk.BooleanVar()
    install_permission_chk = tk.Checkbutton(left_frame, text="Grant install permissions", variable=install_permission_var, bg="#f0f0f0")
    install_permission_chk.pack()

    permission_var = tk.BooleanVar()
    permission_chk = tk.Checkbutton(left_frame, text="Grant system settings permission", variable=permission_var, bg="#f0f0f0")
    permission_chk.pack()

    screen_var = tk.BooleanVar()
    screen_chk = tk.Checkbutton(left_frame, text="Grant overlay permission", variable=screen_var, bg="#f0f0f0")
    screen_chk.pack()

    doze_var = tk.BooleanVar()
    doze_chk = tk.Checkbutton(left_frame, text="Add to Doze whitelist (battery optimization)", variable=doze_var, bg="#f0f0f0")
    doze_chk.pack()

    install_button = tk.Button(left_frame, text="Install", command=install_selected_app, bg="#4CAF50", fg="white", font=("Arial", 12), padx=5, pady=2)
    install_button.pack(pady=5)

    button_frame = tk.Frame(right_frame, bg="#f0f0f0")
    button_frame.pack(fill=tk.BOTH, expand=True)

    store_button = tk.Button(button_frame, text="Install Store", command=install_store, bg="#2196F3", fg="white", font=("Arial", 12), padx=10, pady=5)
    store_button.pack(fill=tk.X, pady=2)

    buttons_button = tk.Button(button_frame, text="Install Buttons", command=install_buttons, bg="#FF9800", fg="white", font=("Arial", 12), padx=10, pady=5)
    buttons_button.pack(fill=tk.X, pady=2)

    hud_button = tk.Button(button_frame, text="Install HUD", command=install_hud, bg="#9C27B0", fg="white", font=("Arial", 12), padx=10, pady=5)
    hud_button.pack(fill=tk.X, pady=2)

    standard_button = tk.Button(button_frame, text="Install Standard Package", command=install_standard_set, bg="#4CAF50", fg="white", font=("Arial", 12), padx=10, pady=5)
    standard_button.pack(fill=tk.X, pady=5)

    # Row frame for side-by-side buttons
    row_frame = tk.Frame(button_frame, bg="#f0f0f0")
    row_frame.pack(fill=tk.X, pady=2)

    disable_qrcode_button = tk.Button(row_frame, text="Disable QR", command=lambda: disable_qrcode(device_var.get()), bg="#FF0000", fg="white", font=("Arial", 12), padx=10, pady=5)
    disable_qrcode_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

    start_box715_button = tk.Button(row_frame, text="Start Box715", command=lambda: start_box715(device_var.get()), bg="#00CC66", fg="white", font=("Arial", 12), padx=10, pady=5)
    start_box715_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

    set_timezone_baku_button = tk.Button(button_frame, text="Set Timezone to Baku", command=lambda: set_timezone_baku(device_var.get()), bg="#0066FF", fg="white", font=("Arial", 12), padx=10, pady=5)
    set_timezone_baku_button.pack(fill=tk.X, pady=2)

    # Row frame for Launcher Fix and Patch 7.0 buttons
    row_frame_patch = tk.Frame(button_frame, bg="#f0f0f0")
    row_frame_patch.pack(fill=tk.X, pady=2)

    fix_launcher_button = tk.Button(row_frame_patch, text="Launcher FIX", command=lambda: disable_launchers(device_var.get()), bg="#FF5733", fg="white", font=("Arial", 12), padx=10, pady=5)
    fix_launcher_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

    install_patch_button = tk.Button(row_frame_patch, text="Patch 7.0", command=install_patch, bg="#FFA500", fg="white", font=("Arial", 12), padx=10, pady=5)
    install_patch_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

    log_frame = tk.Frame(root, bg="#f0f0f0", bd=2, relief="solid")
    log_frame.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.BOTH, expand=True)

    logger.init_gui(log_frame)

    root.mainloop()
