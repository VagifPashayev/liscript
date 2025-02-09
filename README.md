# liscript — Lixiang APK Installer

A Python/Tkinter desktop utility for installing and configuring applications on **Lixiang (Li Auto) car infotainment systems** via ADB. Originally built for hands-on fleet preparation and client vehicle setup.

The tool auto-detects the monitor type (pre-facelift rear / pre-facelift dual / restyling triple) from the connected device's user profile, and installs APKs with the correct permissions per user account.

---

## Interface

```
┌─────────────────────────────────────────────────────────────┐
│               Lixiang Script By Vagif                       │
│       Current monitor: Restyling — Main + Passenger + Rear  │
│                   [ Refresh Monitor ]                       │
├────────────────────────┬────────────────────────────────────┤
│  Select device:        │  [ Install Store             ]     │
│  ┌──────────────────┐  │  [ Install Buttons           ]     │
│  │ emulator-5554  ▼ │  │  [ Install HUD               ]     │
│  └──────────────────┘  │  [ Install Standard Package  ]     │
│                        │                                    │
│  Select users:         │  [ Disable QR ] [ Start Box715 ]   │
│  ☑ Main (0)            │  [ Set Timezone to Baku      ]     │
│  ☑ Passenger (21473)   │                                    │
│  ☑ Rear (6174)         │  [ Launcher FIX ] [ Patch 7.0 ]   │
│                        │                                    │
│  Select app:           │                                    │
│  ┌──────────────────┐  │                                    │
│  │  YouTube_AnyApp▼ │  │                                    │
│  └──────────────────┘  │                                    │
│                        │                                    │
│  ☐ Grant install perms │                                    │
│  ☐ Grant system perms  │                                    │
│  ☐ Grant overlay perms │                                    │
│  ☐ Doze whitelist      │                                    │
│                        │                                    │
│       [ Install ]      │                                    │
├────────────────────────┴────────────────────────────────────┤
│ LOG                                                         │
│ ✅ ADB found: Android Debug Bridge version 1.0.41           │
│ ✅ LiAppStore installed successfully for selected users      │
│ ✅ REQUEST_INSTALL_PACKAGES granted for LiAppStore to user 0 │
│ ...                                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Features

- **Auto monitor detection** — identifies pre-facelift rear, pre-facelift dual, or restyling triple display setups from device user count
- **Per-user APK installation** — installs apps to specific Android user profiles (Main / Passenger / Rear)
- **Permission management** — grants `REQUEST_INSTALL_PACKAGES`, `WRITE_SECURE_SETTINGS`, `SYSTEM_ALERT_WINDOW` per app
- **Doze whitelist** — exempts apps from Android battery optimization
- **One-click presets** — Install Store, Install Buttons, Install HUD, Install Standard Package
- **Utility actions** — disable stock launchers, disable QR code provider, launch Box715 diagnostics, set timezone to Baku
- **Live log panel** — all ADB output streamed into the UI in real time

---

## Requirements

- Python 3.8+
- ADB (`adb.exe`) placed in `adb/` subfolder next to the script
- Android device connected via USB with ADB debugging enabled

### Python dependencies

No third-party packages required — uses only the standard library (`tkinter`, `subprocess`, `json`, `os`).

---

## Project structure

```
liscript/
├── main.py          # Tkinter GUI and button handlers
├── adb_utils.py     # ADB command wrappers (install, uninstall, permissions, etc.)
├── app_utils.py     # APK discovery from apps/ folder
├── logger.py        # Tkinter log widget + console mirror
└── apps/            # App bundles (not included — add your own)
    └── <AppName>/
        ├── app.apk
        └── package.txt   # JSON: {"package": "com.example.app"}
```

---

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/VagifPashayev/liscript.git
   cd liscript
   ```

2. Place `adb.exe` (and its dependencies `AdbWinApi.dll`, `AdbWinUsbApi.dll`) in an `adb/` subfolder.

3. Populate the `apps/` directory with your APK bundles (see structure above).

4. Connect a Lixiang infotainment device via USB and enable ADB debugging.

5. Run:
   ```bash
   python main.py
   ```

---

## Monitor types

The tool detects the display setup by counting Android user profiles on the device:

| User count | Monitor type                            |
|------------|-----------------------------------------|
| 1          | Pre-facelift — Rear monitor only        |
| 2          | Pre-facelift — Main + Passenger screens |
| 3          | Restyling — Main + Passenger + Rear     |

Certain apps (Buttons, HUD, Messages, Waze, etc.) are blocked from installation on rear-only devices since they require the main or passenger display.

---

## Building a standalone executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

The output `dist/main.exe` includes all Python code. Place the `adb/` and `apps/` folders next to the `.exe`.

---

## Author

**Vagif Pashayev** — built for personal use during Lixiang vehicle preparation and client installations.
