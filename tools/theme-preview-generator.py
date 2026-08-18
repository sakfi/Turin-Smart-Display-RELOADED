#!/usr/bin/env python
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

# theme-preview-generator.py: Run by GitHub actions on new commits, to generate a MarkDown page containing themes list
# and their associated preview

import os

import yaml


def get_all_themes_by_size():
    directory = 'res/themes/'
    size_map = {}
    for filename in sorted(os.listdir(directory), key=str.casefold):
        dir_path = os.path.join(directory, filename)
        if os.path.isdir(dir_path):
            theme = os.path.join(dir_path, 'theme.yaml')
            if os.path.isfile(theme):
                with open(theme, "rt", encoding='utf8') as stream:
                    try:
                        theme_data = yaml.safe_load(stream)
                        size = theme_data.get('display', {}).get("DISPLAY_SIZE", '3.5"')
                    except Exception:
                        size = '3.5"'
                    if size not in size_map:
                        size_map[size] = []
                    size_map[size].append(filename)
    return size_map


def write_theme_previews_to_file(themes, file, size):
    file.write(f"\n## {size} themes\n")
    file.write("<table>")
    i = 0
    for theme in themes:
        file.write(
            f"<td>{theme}<img src=\"https://raw.githubusercontent.com/mathoudebine/turing-smart-screen-python/main/res/themes/{theme}/preview.png\" width=\"150\"/></td>")
        i = i + 1
        if i >= 5:
            file.write("</table><table>")
            i = 0
    file.write("</table>\n")


if __name__ == "__main__":
    size_map = get_all_themes_by_size()

    # Sort sizes numerically if possible
    def parse_size_key(s):
        try:
            return float(s.replace('"', '').strip())
        except ValueError:
            return 999.0

    sorted_sizes = sorted(size_map.keys(), key=parse_size_key)

    with open("res/themes/themes.md", "w", encoding='utf-8') as file:
        file.write("<!--- This file is generated automatically by GitHub Actions, do not edit it! --->\n")
        file.write("\n")
        file.write("# Turin Smart Display Themes Gallery\n")
        file.write("\n")
        file.write("ℹ️ Click on a preview to view full size\n\n")

        for sz in sorted_sizes:
            anchor = sz.replace('"', '').replace('.', '').strip()
            file.write(f"[{sz} themes](#{anchor}-themes)\n\n")

        for sz in sorted_sizes:
            write_theme_previews_to_file(size_map[sz], file, sz)

