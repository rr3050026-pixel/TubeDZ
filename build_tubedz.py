import os
import sys
import shutil
import zipfile
import subprocess
from PIL import Image

WORKSPACE = '/workspace/calm-ramanujan'
BASE_APK = os.path.join(WORKSPACE, 'rvx_base.apk')
ICON_SRC = os.path.join(WORKSPACE, 'attachments/f7fa7a71-5dde-455f-9ac7-fcca4f48cbb0/file_00000000798882129f02fd6bf345ba60.png')
WORK_DIR = os.path.join(WORKSPACE, 'build_work')
OUTPUT_APK = os.path.join(WORKSPACE, 'TubeDZ.apk')
KEYSTORE = os.path.join(WORKSPACE, 'tubedz.keystore')

if os.path.exists(WORK_DIR):
    shutil.rmtree(WORK_DIR)
os.makedirs(WORK_DIR, exist_ok=True)

print("1. Loading custom icon image...")
icon_img = Image.open(ICON_SRC).convert("RGBA")

# Map of legacy launcher icons
legacy_icons = {
    'res/9wU.png': (48, 48),
    'res/ynk.png': (72, 72),
    'res/FSV.png': (96, 96),
    'res/RJS.png': (144, 144),
    'res/o-_.png': (192, 192),
}

# Map of adaptive foreground icons
adaptive_fg_icons = {
    'res/N5z.png': (108, 108),
    'res/wI5.png': (162, 162),
    'res/Eo-.png': (216, 216),
    'res/9Gt.png': (324, 324),
    'res/_nh.png': (432, 432),
    'res/fIv.png': (108, 108),
    'res/kDT.png': (162, 162),
    'res/v1R.png': (216, 216),
    'res/tsU.png': (324, 324),
    'res/Vd3.png': (432, 432),
}

# Adaptive background: dark/black background
adaptive_bg_icons = {
    'res/b5J.png': (108, 108),
    'res/LYP.png': (162, 162),
    'res/lqg.png': (216, 216),
    'res/wDF.png': (324, 324),
    'res/W_K.png': (432, 432),
    'res/eiq.png': (108, 108),
    'res/rbD.png': (162, 162),
    'res/9fn.png': (216, 216),
    'res/wAv.png': (324, 324),
    'res/jzc.png': (432, 432),
}

dpi_sizes = {
    'mdpi': (108, 108),
    'hdpi': (162, 162),
    'xhdpi': (216, 216),
    'xxhdpi': (324, 324),
    'xxxhdpi': (432, 432),
}

print("2. Generating resized icons...")
# Write legacy icons
for path, size in legacy_icons.items():
    full_path = os.path.join(WORK_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    resized = icon_img.resize(size, Image.LANCZOS)
    resized.save(full_path, "PNG")

# Write adaptive foreground icons
for path, size in adaptive_fg_icons.items():
    full_path = os.path.join(WORK_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    resized = icon_img.resize(size, Image.LANCZOS)
    resized.save(full_path, "PNG")

# Write adaptive background icons (pure dark to complement the icon)
for path, size in adaptive_bg_icons.items():
    full_path = os.path.join(WORK_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    bg = Image.new("RGBA", size, (18, 18, 18, 255))
    bg.save(full_path, "PNG")

# Also find and replace all morphe_adaptive_* icons in the zip
with zipfile.ZipFile(BASE_APK, 'r') as zin:
    all_names = zin.namelist()

for name in all_names:
    if name.startswith('res/mipmap-') and name.endswith('.png'):
        full_path = os.path.join(WORK_DIR, name)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        dpi = name.split('/')[1].replace('mipmap-', '')
        size = dpi_sizes.get(dpi, (162, 162))
        if 'background' in name:
            bg = Image.new("RGBA", size, (18, 18, 18, 255))
            bg.save(full_path, "PNG")
        else:
            resized = icon_img.resize(size, Image.LANCZOS)
            resized.save(full_path, "PNG")

print("3. Patching AndroidManifest.xml and resources.arsc...")
with zipfile.ZipFile(BASE_APK, 'r') as zin:
    manifest = bytearray(zin.read('AndroidManifest.xml'))
    arsc = bytearray(zin.read('resources.arsc'))

# Replace in manifest: UTF-16LE 'YouTube' -> 'TubeDZ'
orig_m = b'\x07\x00Y\x00o\x00u\x00T\x00u\x00b\x00e\x00\x00\x00'
repl_m = b'\x06\x00T\x00u\x00b\x00e\x00D\x00Z\x00\x00\x00\x00\x00'
manifest_mod = manifest.replace(orig_m, repl_m)
with open(os.path.join(WORK_DIR, 'AndroidManifest.xml'), 'wb') as f:
    f.write(manifest_mod)

# Replace in resources.arsc: UTF-8 'YouTube' -> 'TubeDZ'
orig_a = b'\x07\x07YouTube\x00'
repl_a = b'\x06\x06TubeDZ\x00\x00'
arsc_mod = arsc.replace(orig_a, repl_a)
with open(os.path.join(WORK_DIR, 'resources.arsc'), 'wb') as f:
    f.write(arsc_mod)

print("4. Updating APK archive...")
work_apk = os.path.join(WORKSPACE, 'work.apk')
if os.path.exists(work_apk):
    os.remove(work_apk)
shutil.copyfile(BASE_APK, work_apk)

# Add resources.arsc with -0 (stored)
subprocess.run(['zip', '-0', work_apk, 'resources.arsc'], cwd=WORK_DIR, check=True)

# Add AndroidManifest.xml with -9 (deflated)
subprocess.run(['zip', '-9', work_apk, 'AndroidManifest.xml'], cwd=WORK_DIR, check=True)

# Add all res files
res_files = []
for root, _, files in os.walk(os.path.join(WORK_DIR, 'res')):
    for file in files:
        rel = os.path.relpath(os.path.join(root, file), WORK_DIR)
        res_files.append(rel)

print(f"Adding {len(res_files)} modified image files...")
cmd = ['zip', '-9', work_apk] + res_files
subprocess.run(cmd, cwd=WORK_DIR, check=True)

print("5. Aligning APK with zipalign...")
aligned_apk = os.path.join(WORKSPACE, 'aligned.apk')
if os.path.exists(aligned_apk):
    os.remove(aligned_apk)

subprocess.run([
    '/root/android-sdk/build-tools/35.0.0/zipalign',
    '-f', '-p', '4',
    work_apk,
    aligned_apk
], check=True)

print("6. Signing APK with apksigner...")
if os.path.exists(OUTPUT_APK):
    os.remove(OUTPUT_APK)
shutil.copyfile(aligned_apk, OUTPUT_APK)

subprocess.run([
    '/root/android-sdk/build-tools/35.0.0/apksigner',
    'sign',
    '--ks', KEYSTORE,
    '--ks-key-alias', 'tubedz',
    '--ks-pass', 'pass:123456',
    '--key-pass', 'pass:123456',
    OUTPUT_APK
], check=True)

print("7. Verifying APK signature...")
subprocess.run([
    '/root/android-sdk/build-tools/35.0.0/apksigner',
    'verify',
    '-v',
    OUTPUT_APK
], check=True)

print("8. Checking badging of final APK...")
proc = subprocess.run([
    '/root/android-sdk/build-tools/35.0.0/aapt',
    'dump', 'badging',
    OUTPUT_APK
], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env={'ANDROID_DATA': '/tmp'})

for line in proc.stdout.splitlines():
    if any(k in line for k in ['package:', 'application-label', 'application:', 'launchable-activity']):
        print(line)

print("Cleaning temporary files...")
if os.path.exists(work_apk): os.remove(work_apk)
if os.path.exists(aligned_apk): os.remove(aligned_apk)
shutil.rmtree(WORK_DIR)
print(f"SUCCESS: Generated {OUTPUT_APK}")
