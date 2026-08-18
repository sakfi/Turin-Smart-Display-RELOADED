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
import sys
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
        return f'{self.value:>5.1f}%'
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




def _read_gpu_power() -> float:
    
    GPU_NAME = "GPU Package"
    
    sensors_backend = sys.modules.get('library.sensors.sensors_librehardwaremonitor')
    if sensors_backend is None:
        return math.nan

    Hardware = getattr(sensors_backend, 'Hardware', None)
    handle = getattr(sensors_backend, 'handle', None)
    get_gpu_name = getattr(sensors_backend, 'get_gpu_name', None)
    get_hw_and_update = getattr(sensors_backend, 'get_hw_and_update', None)
    if Hardware is None or handle is None or get_gpu_name is None or get_hw_and_update is None:
        return math.nan

    gpu_name = get_gpu_name()
    if not gpu_name:
        return math.nan

    # Descobre o tipo da GPU escolhida
    gpu_type = None
    for hw in handle.Hardware:
        if hw.Name == gpu_name:
            gpu_type = hw.HardwareType
            break
    if gpu_type is None:
        return math.nan

    # Pega exatamente essa GPU
    hardware = get_hw_and_update(gpu_type, gpu_name)
    if hardware is None:
        return math.nan

    # 1º: tenta especificamente o sensor "GPU Package"
    for sensor in hardware.Sensors:
        if (sensor.SensorType == Hardware.SensorType.Power
                and sensor.Value is not None
                and str(sensor.Name) == GPU_NAME):
            return float(sensor.Value)

    # 2º: fallback – primeiro sensor de Power disponível
    for sensor in hardware.Sensors:
        if sensor.SensorType == Hardware.SensorType.Power and sensor.Value is not None:
            return float(sensor.Value)

    return math.nan



def debug_list_gpu_power_sensors():
    sensors_backend = sys.modules.get('library.sensors.sensors_librehardwaremonitor')
    if sensors_backend is None:
        print("backend not loaded")
        return

    Hardware = sensors_backend.Hardware
    handle = sensors_backend.handle
    get_gpu_name = sensors_backend.get_gpu_name
    get_hw_and_update = sensors_backend.get_hw_and_update

    gpu_name = get_gpu_name()
    print("Using GPU:", gpu_name)

    gpu_type = None
    for hw in handle.Hardware:
        if hw.Name == gpu_name:
            gpu_type = hw.HardwareType
            break

    hw = get_hw_and_update(gpu_type, gpu_name)
    if hw is None:
        print("GPU not found")
        return

    def dump_hw(node, indent=0):
        prefix = "  " * indent
        try:
            node.Update()
        except Exception:
            pass

        print(f"{prefix}HW: Name={node.Name}, Type={node.HardwareType}, Identifier={node.Identifier}")

        for s in node.Sensors:
            try:
                print(
                    f"{prefix}  SENSOR: "
                    f"Type={s.SensorType}, Name={s.Name}, Value={s.Value}, Identifier={s.Identifier}"
                )
            except Exception as e:
                print(f"{prefix}  SENSOR ERROR: {e}")

        try:
            for sub in node.SubHardware:
                dump_hw(sub, indent + 1)
        except Exception:
            pass

    print("=== GPU TREE ===")
    dump_hw(hw)

class GPU_POWER(CustomDataSource):
    last_val = [math.nan] * 10

    def as_numeric(self) -> float:
        self.value = _read_gpu_power()
        self.last_val.append(self.value)
        self.last_val.pop(0)
        return self.value

    def as_string(self) -> str:
        value = getattr(self, 'value', math.nan)
        if math.isnan(value):
            return '  N/A'
        return f'{int(round(value)):>4d}'

    def last_values(self) -> List[float]:
        return self.last_val

