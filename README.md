<div align="center">

# 🖥️ Turin Smart Display RELOADED

> **The Ultimate Next-Generation Open-Source System Monitoring & Display Abstraction Suite for Small USB-C IPS Smart Displays.**

<img src=".github/workflows/split.gif" width="100%" />

</div>

### 🌟 Overview

**Turin Smart Display RELOADED** is a feature-packed, highly customizable open-source system monitoring application and unified display driver abstraction suite engineered specifically for small IPS USB-C smart displays (including Turing, TURZX, XuanFang, UsbPCMonitor, Kipye, and WeAct Studio hardware).

Whether you need a sleek desktop hardware monitor with dynamic themes or a standalone Python SDK to drive mini displays in your own applications, **Turin Smart Display RELOADED** provides zero-latency performance, multi-OS support, keyless open-source weather integration, and deep hardware customization out of the box.

<img src=".github/workflows/split.gif" width="100%" />

### 🛡️ Disclaimer & Legal Notice

> [!WARNING]
> This project is **an independent open-source software project** and is **not affiliated, associated, authorized, endorsed by, or in any way officially connected with Turing / XuanFang / Kipye / TURZX** or any of their subsidiaries, affiliates, manufacturers, or sellers. All product and company names are registered trademarks of their respective owners.
>
> This software is an open-source community alternative, **NOT** the proprietary vendor software (`USBMonitor.exe`, `ExtendScreen.exe`, etc.). Please do **not** open issues here regarding proprietary hardware bugs or vendor software.

<img src=".github/workflows/split.gif" width="100%" />

### 🏷️ Badges & Platform Support

![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Windows 10/11](https://img.shields.io/badge/Windows-10%2F11-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![macOS](https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=apple&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue?style=for-the-badge)](./LICENSE)

<img src=".github/workflows/split.gif" width="100%" />

### ✨ Key Features

- 🖥️ **Unified Display Abstraction**: Single unified interface to control Turing, TURZX, XuanFang, Kipye, UsbPCMonitor, and WeAct smart screens.
- 📊 **Comprehensive System Monitoring**: Live CPU, GPU, RAM, VRAM, Disk, Network, Temperatures, Fan Speeds, and custom telemetry integration.
- 🌦️ **Built-in Open-Source Weather**: Powered by keyless Open-Meteo API out-of-the-box (no API keys required!).
- 🎨 **Dynamic Theme Engine & Visual Theme Editor**: Custom theme creation tool (`theme-editor.py`) with support for graphics, gauges, progress bars, and custom layouts.
- 💡 **Hardware LED & Brightness Control**: Native control for backplate RGB LEDs and display backlight intensity on supported models.
- 🖥️ **Simulated LCD Mode**: Develop, test, and design custom themes on your computer display even without physical hardware plugged in.
- ⚙️ **Graphical Setup Wizard**: User-friendly GUI setup wizard (`configure.py`) alongside easy `config.yaml` file management.
- 🔌 **Python SDK & Abstraction Layer**: Import directly into your Python scripts (`library/`) for custom UI drawing, text formatting, progress bars, and display commands.
- 📌 **System Tray Control**: Runs cleanly in the background with quick tray menu options.

<img src=".github/workflows/split.gif" width="100%" />

### 📺 Supported Hardware Matrix

#### ✅ Verified & Fully Supported Models

| Turing Smart Screen / TURZX (All Revisions) |
|:---:|
| <img src="res/docs/turing.webp" width="28%"/> <img src="res/docs/turing46inch.png" width="28%"/> <img src="res/docs/turing5inch.png" width="28%"/> <br/> <img src="res/docs/turing2inch.webp" width="28%"/> <img src="res/docs/turing8inch.png" width="28%"/> <img src="res/docs/turing8inch.webp" width="28%"/> |
| **All Sizes Supported:** `2.1"` \| `2.8"` \| `3.5"` \| `4.6"` \| `5.0"` \| `5.2"` \| `8.0"` \| `8.8"` \| `9.2"` \| `12.3"` <br/> Supports **USB** & **UART** protocols. Includes RGB LED backplate lighting control. |

| XuanFang 3.5" | UsbPCMonitor 3.5" / 5.0" | Kipye Qiye Smart Display 3.5" |
|:---:|:---:|:---:|
| <img src="res/docs/xuanfang.webp" width="70%"/> | <img src="res/docs/UsbPCMonitor_5inch.webp" width="70%"/> | <img src="res/docs/kipye-qiye-35.webp" width="70%"/> |
| Revision B & Flagship (with RGB LEDs) | Original software: `UsbPCMonitor.exe` | Front panel inscription "奇叶智显" Qiye |

| WeAct Studio Display FS V1 0.96" | WeAct Studio Display FS V1 3.5" |
|:---:|:---:|
| <img src="res/docs/weact_0.96.jpg" width="60%"/> | <img src="res/docs/weact_3.5.png" width="60%"/> |

<details>
<summary><b>🔍 View Unsupported or Untested Smart Screen Models</b></summary>

<br/>

| Model | Status & Details | Image |
|:---|:---|:---:|
| **AX206 / AIDA64 / USB2LCD** | Unsupported (Appotech AX206 hacked photo frame firmware). | <img src="res/docs/ax206.jpg" width="130"/> |
| **ACEMAGIC S1 Mini PC (1.9")** | Untested / Integration candidate (protocol decoded). | <img src="res/docs/acemagic-s1-mini.jpg" width="130"/> |
| **NXElec BeadaPanel (3/4/5/6/7)** | Untested / Integration candidate (Panel-Link protocol). | <img src="res/docs/beadapanel-3.jpg" width="130"/> |
| **Waveshare USB-Monitor** | Unsupported (Requires proprietary firmware lock). | <img src="res/docs/waveshare-21inch-28inch.png" width="130"/> |
| **GUITION Smart Screen 3.5"** | Unsupported (Requires proprietary vendor software lock). | <img src="res/docs/guition.webp" width="130"/> |
| **Fuldho 3.5" IPS Screen** | Unsupported (Requires `SmartMonitor.exe` vendor app). | <img src="res/docs/fuldho_3.5.jpg" width="130"/> |

</details>

<img src=".github/workflows/split.gif" width="100%" />

### 🚀 Quick Start Guide

#### 1️⃣ Prerequisites
Make sure you have **Python 3.9 or higher** installed on your system.

#### 2️⃣ Installation & Setup

Clone the repository and set up your Python environment:

```bash
git clone https://github.com/mathoudebine/turing-smart-screen-python.git Turin-Smart-Display-RELOADED
cd Turin-Smart-Display-RELOADED

# Recommended: Create virtual environment
python -m venv venv

# Activate Virtual Environment
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3️⃣ Launch Setup Wizard
Configure your display hardware model, serial COM port, and select your default theme:

```bash
python configure.py
```

<div align="center">
  <img src="res/docs/config_wizard.png" alt="Configuration Wizard Setup" width="75%"/>
</div>

#### 4️⃣ Start the System Monitor
Launch **Turin Smart Display RELOADED**:

```bash
python main.py
```

<img src=".github/workflows/split.gif" width="100%" />

### 🎨 Themes & Visual Customization

**Turin Smart Display RELOADED** provides an extensive theme engine and an intuitive desktop theme editor.

#### 🖌️ Interactive Theme Editor
Design and modify themes without editing raw code:

```bash
python theme-editor.py
```

#### 🖼️ Included Themes Gallery

<div align="center">
  <img src="res/themes/3.5inchTheme2/preview.png" height="140"/>
  <img src="res/themes/Terminal/preview.png" height="140"/>
  <img src="res/themes/Cyberpunk-net/preview.png" height="140"/>
  <img src="res/themes/bash-dark-green-gpu/preview.png" height="140"/>
  <img src="res/themes/Landscape6Grid/preview.png" height="140"/>
  <img src="res/themes/LandscapeMagicBlue/preview.png" height="140"/>
</div>

> 📁 Explore all included themes in [res/themes/themes.md](res/themes/themes.md).

<img src=".github/workflows/split.gif" width="100%" />

### 💻 Developer SDK & Library Usage

Directly integrate **Turin Smart Display RELOADED** driver abstractions into your own Python projects:

```python
from library.lcd.lcd_comm_rev_a import LcdCommRevA

# Initialize display communication
lcd = LcdCommRevA(port="COM3")
lcd.Reset()
lcd.SetBacklight(100)

# Render images and custom text
lcd.DisplayBitmap("path/to/image.png")
lcd.DisplayText("Turin Display Active", x=15, y=15, font_size=20)
```

Run `simple-program.py` for a complete demonstration:
```bash
python simple-program.py
```

<img src=".github/workflows/split.gif" width="100%" />

### 📁 Repository Structure

```
Turin-Smart-Display-RELOADED/
├── library/             # Unified Display Drivers & Abstraction Protocols
├── res/                 # Documentation assets, icons & themes
│   ├── docs/            # Hardware reference photos & screenshots
│   └── themes/          # Theme YAML configurations & graphic assets
├── tools/               # Auxiliary scripts and utilities
├── config.yaml          # Main configuration file
├── configure.py         # Graphical configuration wizard
├── main.py              # System Monitor main entry point
├── theme-editor.py      # Visual Theme Editor tool
├── simple-program.py    # Python SDK example script
└── requirements.txt     # Python dependency list
```

<img src=".github/workflows/split.gif" width="100%" />

### 📰 Media & References

- ⚡ **Hackaday**: [Cheap LCD Uses USB Serial](https://hackaday.com/2023/09/11/cheap-lcd-uses-usb-serial/)
- 🌐 **CNX Software**: [Turing Smart Screen – A low-cost 3.5-inch USB Type-C information display](https://www.cnx-software.com/2022/04/29/turing-smart-screen-a-low-cost-3-5-inch-usb-type-c-information-display/)
- 🛠️ **Phazer Tech**: [Turing Smart Screen Python Tutorial](https://phazertech.com/tutorials/turing-smart-screen.html)
<img src=".github/workflows/split.gif" width="100%" />

### 🌟 Special Thanks & Acknowledgments

Special thanks and credit to **[Matthieu Houdebine](https://github.com/mathoudebine)** (`@mathoudebine`), the original author and primary developer of [`turing-smart-screen-python`](https://github.com/mathoudebine/turing-smart-screen-python). His work on reverse-engineering smart display USB/UART protocols and building the foundation of this ecosystem made this RELOADED project possible!

<img src=".github/workflows/split.gif" width="100%" />

### 📜 License

Distributed under the **GNU General Public License v3.0**. See [`LICENSE`](./LICENSE) for full details.
