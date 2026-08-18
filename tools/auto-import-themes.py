#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Turin Smart Display RELOADED - Automated Community Theme Importer
# Scrapes GitHub Discussions (Themes Category) and imports newly posted community themes.

import os
import re
import sys
import io
import urllib.request
import zipfile
import shutil
import yaml
import subprocess

# Ensure UTF-8 stdout output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

THEMES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'res', 'themes')
PREVIEW_GENERATOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'theme-preview-generator.py')
BASE_DISCUSSIONS_URL = "https://github.com/mathoudebine/turing-smart-screen-python/discussions/categories/themes"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}


def fetch_all_discussion_urls():
    urls = set()
    for page in range(1, 15):
        page_url = f"{BASE_DISCUSSIONS_URL}?page={page}"
        try:
            req = urllib.request.Request(page_url, headers=HEADERS)
            with urllib.request.urlopen(req) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                matches = re.findall(r'href="(/mathoudebine/turing-smart-screen-python/discussions/\d+)"', html)
                if not matches:
                    break
                prev_len = len(urls)
                for m in matches:
                    urls.add("https://github.com" + m)
                if len(urls) == prev_len:
                    break
        except Exception as e:
            print(f"Warning: Failed to fetch discussions page {page}: {e}")
            break
    return sorted(list(urls), key=lambda x: int(x.split('/')[-1]))


def import_themes():
    discussions = fetch_all_discussion_urls()
    print(f"Discovered {len(discussions)} theme discussions to audit.")

    existing_themes = set(os.listdir(THEMES_DIR)) if os.path.exists(THEMES_DIR) else set()
    imported_themes = []

    for idx, disc_url in enumerate(discussions, 1):
        disc_id = disc_url.split('/')[-1]
        try:
            req = urllib.request.Request(disc_url, headers=HEADERS)
            with urllib.request.urlopen(req) as resp:
                html = resp.read().decode('utf-8', errors='ignore')

            file_urls = re.findall(r'href="([^"]+(?:user-attachments/files/\d+/[^"]+|\.zip|\.rar|\.7z))"', html, re.IGNORECASE)
            clean_urls = list(set(['https://github.com' + fu if not fu.startswith('http') else fu for fu in file_urls]))

            if not clean_urls:
                continue

            for file_url in clean_urls:
                filename = file_url.split('/')[-1]
                if not (filename.endswith('.zip') or filename.endswith('.rar') or 'files/' in file_url):
                    continue

                try:
                    f_req = urllib.request.Request(file_url, headers=HEADERS)
                    with urllib.request.urlopen(f_req) as f_resp:
                        content = f_resp.read()

                    if content.startswith(b'PK\x03\x04'):
                        z = zipfile.ZipFile(io.BytesIO(content))
                        namelist = z.namelist()

                        yaml_files = [n for n in namelist if n.endswith('theme.yaml')]
                        if not yaml_files:
                            continue

                        for yaml_path in yaml_files:
                            dir_prefix = os.path.dirname(yaml_path)
                            if dir_prefix:
                                theme_name = os.path.basename(dir_prefix)
                            else:
                                theme_name = filename.replace('.zip', '').replace('.rar', '').strip()

                            theme_name = re.sub(r'[\\/:*?"<>|]', '_', theme_name)
                            target_dir = os.path.join(THEMES_DIR, theme_name)

                            if os.path.exists(target_dir) and os.path.isfile(os.path.join(target_dir, 'theme.yaml')):
                                continue

                            os.makedirs(target_dir, exist_ok=True)

                            for item in namelist:
                                if dir_prefix:
                                    if item.startswith(dir_prefix + '/') or item == dir_prefix:
                                        rel_path = os.path.relpath(item, dir_prefix)
                                        if rel_path == '.':
                                            continue
                                        out_path = os.path.join(target_dir, rel_path)
                                        if item.endswith('/'):
                                            os.makedirs(out_path, exist_ok=True)
                                        else:
                                            os.makedirs(os.path.dirname(out_path), exist_ok=True)
                                            with open(out_path, 'wb') as out_f:
                                                out_f.write(z.read(item))
                                else:
                                    out_path = os.path.join(target_dir, item)
                                    if item.endswith('/'):
                                        os.makedirs(out_path, exist_ok=True)
                                    else:
                                        os.makedirs(os.path.dirname(out_path), exist_ok=True)
                                        with open(out_path, 'wb') as out_f:
                                            out_f.write(z.read(item))

                            # Un-nest single subfolder if present
                            subdirs = [d for d in os.listdir(target_dir) if os.path.isdir(os.path.join(target_dir, d))]
                            if len(subdirs) == 1 and not os.path.isfile(os.path.join(target_dir, 'theme.yaml')):
                                sub_path = os.path.join(target_dir, subdirs[0])
                                for sf in os.listdir(sub_path):
                                    shutil.move(os.path.join(sub_path, sf), os.path.join(target_dir, sf))
                                os.rmdir(sub_path)

                            print(f"[NEW THEME IMPORTED] '{theme_name}' from Discussion #{disc_id}")
                            imported_themes.append(theme_name)

                except Exception as fe:
                    pass

        except Exception as de:
            pass

    print(f"\nAudit complete. Imported {len(imported_themes)} new theme(s).")
    if imported_themes:
        print("Imported:", ", ".join(imported_themes))
        # Regenerate theme preview gallery markdown
        if os.path.exists(PREVIEW_GENERATOR):
            print("Regenerating themes.md preview gallery...")
            subprocess.run([sys.executable, PREVIEW_GENERATOR], check=False)

    return len(imported_themes)


if __name__ == "__main__":
    count = import_themes()
    sys.exit(0)
