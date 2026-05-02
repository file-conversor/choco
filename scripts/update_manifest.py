#!/usr/bin/env python3
""" update_manifest.py - Update the Chocolatey manifest file """

import shutil 
import requests
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

print("Generating Chocolatey manifest files ...")

ctx = dict(os.environ)

OUTDIR = Path(ctx["OUTDIR_MANIFEST"])
shutil.rmtree(OUTDIR, ignore_errors=True)
OUTDIR.mkdir(parents=True, exist_ok=True)

DOWNLOAD_URL=f'{ctx["HOMEPAGE_SRC"]}/releases/download/{ctx["VERSION"]}'
ctx["INSTALL_EXE_URL"] = f'{DOWNLOAD_URL}/file_conversor-{ctx["VERSION"]}-Win_x64-Installer.exe'
ctx["ICON_URL"] = f'{ctx["HOMEPAGE_RAW"]}/{ctx["VERSION"]}/{ctx["ICON_FILE"]}'
ctx["LICENSE_URL"] = f'{ctx["HOMEPAGE_SRC"]}/{ctx["VERSION"]}/blob/master/LICENSE'
ctx["RELEASE_NOTES_URL"] = f'{ctx["HOMEPAGE_SRC"]}/{ctx["VERSION"]}/releases/tag/{ctx["VERSION"]}'

print(f"""
  ENV:
    NAME: {ctx["NAME"]}
    VERSION_SEMVER: {ctx["VERSION_SEMVER"]}
    CHECKSUMS_FILE: {ctx["CHECKSUMS_FILE"]}
    ICON_FILE: {ctx["ICON_FILE"]}
    OUTDIR_MANIFEST: {ctx["OUTDIR_MANIFEST"]}
    OUTDIR_NUPKG: {ctx["OUTDIR_NUPKG"]}
    INSTALL_EXE_URL: {ctx["INSTALL_EXE_URL"]}
""")

print(f"  1. Fetching installer URL and checksum from {DOWNLOAD_URL} ...")
res = requests.get(f'{DOWNLOAD_URL}/{ctx["CHECKSUMS_FILE"]}', timeout=10    )
res.raise_for_status()

for line in res.text.replace("\r", "\n").replace("\n\n", "\n").split("\n"):
    if line.strip().endswith("-Win_x64-Installer.exe"):
        ctx["CHECKSUM"] = line.strip().split()[0]
        break
assert ctx['CHECKSUM'], "Checksum not found in the checksums file!"
print(f"    CHECKSUM: {ctx['CHECKSUM']} ...")
print()

print("  2. Rendering Jinja2 templates ...")
templates_dir="templates"
env = Environment(loader=FileSystemLoader(templates_dir), undefined=StrictUndefined)
for template_path in Path(templates_dir).rglob("*.j2"):    
    # Render the template and write the output file
    filename = template_path.relative_to(templates_dir)
    outfile = OUTDIR / filename.with_name(filename.name.replace(".j2", ""))
    outfile.parent.mkdir(parents=True, exist_ok=True)
    outfile.write_text(
        env.get_template(filename.as_posix()).render(**ctx)    
    , encoding="utf-8")
    print(f"    Generated {outfile} ...")
print()

print("Generating Chocolatey manifest files ... Done!")
print()
