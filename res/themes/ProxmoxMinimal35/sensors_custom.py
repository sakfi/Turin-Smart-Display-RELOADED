# SPDX-License-Identifier: GPL-3.0-or-later
#
# turing-smart-screen-python - a Python system monitor and library for USB-C displays like Turing Smart Screen or XuanFang
# https://github.com/mathoudebine/turing-smart-screen-python/
#
# Copyright (C) 2021 Matthieu Houdebine (mathoudebine)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# This file allows to add custom data source as sensors and display them in System Monitor themes
# There is no limitation on how much custom data source classes can be added to this file
# See CustomDataExample theme for the theme implementation part

import math
import platform
import json
import subprocess
import psutil
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List


# Custom data classes must be implemented in this file, inherit the CustomDataSource and implement its 2 methods
class CustomDataSource(ABC):
    @abstractmethod
    def as_numeric(self) -> float:
        # Numeric value will be used for graph and radial progress bars
        # If there is no numeric value, keep this function empty
        pass

    @abstractmethod
    def as_string(self) -> str:
        # Text value will be used for text display and radial progress bar inner text
        # Numeric value can be formatted here to be displayed as expected
        # It is also possible to return a text unrelated to the numeric value
        # If this function is empty, the numeric value will be used as string without formatting
        pass

    @abstractmethod
    def last_values(self) -> List[float]:
        # List of last numeric values will be used for plot graph
        # If you do not want to draw a line graph or if your custom data has no numeric values, keep this function empty
        pass


# Example for a custom data class that has numeric and text values
class ExampleCustomNumericData(CustomDataSource):
    # This list is used to store the last 10 values to display a line graph
    last_val = [math.nan] * 10  # By default, it is filed with math.nan values to indicate there is no data stored

    def as_numeric(self) -> float:
        # Numeric value will be used for graph and radial progress bars
        # Here a Python function from another module can be called to get data
        # Example: self.value = my_module.get_rgb_led_brightness() / audio.system_volume() ...
        self.value = 75.845

        # Store the value to the history list that will be used for line graph
        self.last_val.append(self.value)
        # Also remove the oldest value from history list
        self.last_val.pop(0)

        return self.value

    def as_string(self) -> str:
        # Text value will be used for text display and radial progress bar inner text.
        # Numeric value can be formatted here to be displayed as expected
        # It is also possible to return a text unrelated to the numeric value
        # If this function is empty, the numeric value will be used as string without formatting
        # Example here: format numeric value: add unit as a suffix, and keep 1 digit decimal precision
        return f"{self.value:>5.1f}%"
        # Important note! If your numeric value can vary in size, be sure to display it with a default size.
        # E.g. if your value can range from 0 to 9999, you need to display it with at least 4 characters every time.
        # --> return f'{self.as_numeric():>4}%'
        # Otherwise, part of the previous value can stay displayed ("ghosting") after a refresh

    def last_values(self) -> List[float]:
        # List of last numeric values will be used for plot graph
        return self.last_val


# Example for a custom data class that only has text values
class ExampleCustomTextOnlyData(CustomDataSource):
    def as_numeric(self) -> float:
        # If there is no numeric value, keep this function empty
        pass

    def as_string(self) -> str:
        # If a custom data class only has text values, it won't be possible to display graph or radial bars
        return "Python: " + platform.python_version()

    def last_values(self) -> List[float]:
        # If a custom data class only has text values, it won't be possible to display line graph
        pass


# --- Proxmox custom data: VMs running / total ---
class ProxmoxVMRunningTotal(CustomDataSource):
    """
    Proxmox QEMU VMs: returns a fixed-width string like ' 5 /  8' (running / total).
    Works when this program runs on the Proxmox node (uses pvesh).
    """

    def __init__(self):
        # Fixed-width default avoids ghosting right away
        self._last_str = " 0 /  0"

    def as_numeric(self) -> float:
        # No numeric value needed for this use-case
        pass

    def as_string(self) -> str:
        try:
            node = platform.node()  # usually hostname, e.g. "pve"
            cmd = ["pvesh", "get", f"/nodes/{node}/qemu", "--output-format", "json"]
            out = subprocess.check_output(cmd, text=True, timeout=2)
            data = json.loads(out)

            total = len(data)
            running = sum(1 for vm in data if vm.get("status") == "running")

            # Fixed-width formatting to avoid ghosting when numbers change digits
            self._last_str = f"{running:>2} /{total:>2}"
        except Exception:
            # Keep last good value if something goes wrong
            pass

        return self._last_str

    def last_values(self) -> List[float]:
        # No graph history
        pass


# --- Proxmox custom data: Date + Time ---
class ProxmoxDateTime(CustomDataSource):
    """
    Returns current date/time as a string.
    Change the strftime format to your preferred layout.
    """

    def as_numeric(self) -> float:
        pass

    def as_string(self) -> str:
        # Example output: "02/03/2026 - 21:45:18"
        return datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

    def last_values(self) -> List[float]:
        pass

class ProxmoxCpuFanRPM(CustomDataSource):
    """
    Returns CPU fan RPM as numeric (for bar/graph) and as string "1234 RPM".
    Uses psutil.sensors_fans() on Linux.
    """

    last_val = [math.nan] * 50  # per eventuale line graph (se vuoi)

    def __init__(self):
        self._rpm = math.nan

    def as_numeric(self) -> float:
        try:
            fans = psutil.sensors_fans() or {}
            # Prendo il primo valore disponibile (di solito basta su Proxmox)
            for _, entries in fans.items():
                for e in entries:
                    # e.current è RPM
                    if getattr(e, "current", None) is not None:
                        rpm = float(e.current)
                        if rpm >= 0:
                            self._rpm = rpm
                            break
                if not math.isnan(self._rpm):
                    break

            # Storico (se poi vuoi un line-graph)
            self.last_val.append(self._rpm)
            self.last_val.pop(0)

        except Exception:
            pass

        return self._rpm

    def as_string(self) -> str:
        # Fixed-width per evitare ghosting
        if self._rpm is None or (isinstance(self._rpm, float) and math.isnan(self._rpm)):
            return " ---- RPM"
        return f"{int(self._rpm):>4} RPM"

    def last_values(self) -> List[float]:
        return self.last_val