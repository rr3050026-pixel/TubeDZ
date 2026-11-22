import os
import sys
import shutil
import zipfile
import subprocess
from PIL import Image, ImageDraw, ImageFont

WORKSPACE = '/workspace/calm-ramanujan'
BASE_APK = os.path.join(WORKSPACE, 'TubeDZ_backup.apk') if os.path.exists(os.path.join(WORKSPACE, 'TubeDZ_backup.apk')) else (
    os.path.join(WORKSPACE, 'rvx_base.apk') if os.path.exists(os.path.join(WORKSPACE, 'rvx_base.apk')) else os.path.join(WORKSPACE, 'TubeDZ.apk')
)
ICON_SRC = os.path.join(WORKSPACE, 'logo.png')
WORK_DIR = os.path.join(WORKSPACE, 'build_work')
OUTPUT_APK = os.path.join(WORKSPACE, 'TubeDZ.apk')
KEYSTORE = os.path.join(WORKSPACE, 'tubedz.keystore')
FONT_PATH = os.path.join(WORKSPACE, 'apk_decoded/assets/youtube_sans_bold_font.ttf')

if os.path.exists(WORK_DIR):
    shutil.rmtree(WORK_DIR)
os.makedirs(WORK_DIR, exist_ok=True)

print("1. Loading custom icon image and creating smooth transparent emblem...")
icon_img = Image.open(ICON_SRC).convert("RGBA")

# Extract antialiased transparent emblem for header wordmark
datas = icon_img.getdata()
new_data = []
for p in datas:
    b = 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]
    if b < 10:
        new_data.append((0, 0, 0, 0))
    elif b < 30:
        alpha = int((b - 10) / 20 * 255)
        new_data.append((p[0], p[1], p[2], alpha))
    else:
        new_data.append(p)

logo_trans = Image.new("RGBA", icon_img.size)
logo_trans.putdata(new_data)
trans_bbox = logo_trans.getbbox()
logo_emblem = logo_trans.crop(trans_bbox) if trans_bbox else icon_img
emblem_aspect = logo_emblem.width / logo_emblem.height

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

print("2. Generating resized launcher & adaptive icons...")
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

print("3. Generating official TubeDZ header wordmarks & branding...")
wordmark_config = {
    'mdpi': {'logo_h': 19, 'logo_x': 16, 'font_size': 20, 'spacing': 5},
    'hdpi': {'logo_h': 29, 'logo_x': 24, 'font_size': 30, 'spacing': 7},
    'xhdpi': {'logo_h': 39, 'logo_x': 32, 'font_size': 40, 'spacing': 9},
    'xxhdpi': {'logo_h': 58, 'logo_x': 48, 'font_size': 60, 'spacing': 14},
    'xxxhdpi': {'logo_h': 78, 'logo_x': 64, 'font_size': 80, 'spacing': 18},
}

def render_wordmark(width, height, dpi, is_dark):
    canvas = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    cfg = wordmark_config.get(dpi, wordmark_config['xxhdpi'])
    lh = cfg['logo_h']
    lw = int(lh * emblem_aspect)
    logo_res = logo_emblem.resize((lw, lh), Image.LANCZOS)
    ly = (height - lh) // 2
    canvas.paste(logo_res, (cfg['logo_x'], ly), logo_res)

    try:
        font = ImageFont.truetype(FONT_PATH, cfg['font_size'])
    except Exception:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(canvas)
    tx = cfg['logo_x'] + lw + cfg['spacing']
    t_bbox = font.getbbox('TubeDZ')
    target_center_y = ly + lh / 2
    ty = int(target_center_y - (t_bbox[1] + t_bbox[3]) / 2)
    text_color = (255, 255, 255, 255) if is_dark else (33, 33, 33, 255)
    draw.text((tx, ty), 'TubeDZ', font=font, fill=text_color)
    return canvas

def render_standalone_text(width, height, dpi, is_dark):
    canvas = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    cfg = wordmark_config.get(dpi, wordmark_config['xxhdpi'])
    try:
        font = ImageFont.truetype(FONT_PATH, cfg['font_size'])
    except Exception:
        font = ImageFont.load_default()
    draw = ImageDraw.Draw(canvas)
    t_bbox = font.getbbox('TubeDZ')
    tw = t_bbox[2] - t_bbox[0]
    th = t_bbox[3] - t_bbox[1]
    tx = (width - tw) // 2 - t_bbox[0]
    ty = (height - th) // 2 - t_bbox[1]
    text_color = (255, 255, 255, 255) if is_dark else (33, 33, 33, 255)
    draw.text((tx, ty), 'TubeDZ', font=font, fill=text_color)
    return canvas

# 50 Obfuscated Header Resources
obfuscated_header_drawables = [
    # yt_premium_wordmark_header_dark (PNG)
    ('res/UUQ.png', (129, 48), 'mdpi', True, 'PNG', False),
    ('res/eqG.png', (194, 72), 'hdpi', True, 'PNG', False),
    ('res/MQe.png', (258, 96), 'xhdpi', True, 'PNG', False),
    ('res/cXD.png', (387, 144), 'xxhdpi', True, 'PNG', False),
    ('res/Lgq.png', (516, 192), 'xxxhdpi', True, 'PNG', False),

    # yt_premium_wordmark_header_light (PNG)
    ('res/F0v.png', (129, 48), 'mdpi', False, 'PNG', False),
    ('res/Szm.png', (194, 72), 'hdpi', False, 'PNG', False),
    ('res/BVD.png', (258, 96), 'xhdpi', False, 'PNG', False),
    ('res/f5q.png', (387, 144), 'xxhdpi', False, 'PNG', False),
    ('res/sgg.png', (516, 192), 'xxxhdpi', False, 'PNG', False),

    # yt_ringo2_premium_wordmark_header_dark (WEBP)
    ('res/NwE.webp', (129, 48), 'mdpi', True, 'WEBP', False),
    ('res/IXf.webp', (194, 72), 'hdpi', True, 'WEBP', False),
    ('res/a-o.webp', (258, 96), 'xhdpi', True, 'WEBP', False),
    ('res/eDF.webp', (387, 144), 'xxhdpi', True, 'WEBP', False),
    ('res/HUP.webp', (516, 192), 'xxxhdpi', True, 'WEBP', False),

    # yt_ringo2_premium_wordmark_header_light (WEBP)
    ('res/YwR.webp', (129, 48), 'mdpi', False, 'WEBP', False),
    ('res/dxH.webp', (194, 72), 'hdpi', False, 'WEBP', False),
    ('res/A_0.webp', (258, 96), 'xhdpi', False, 'WEBP', False),
    ('res/GQi.webp', (387, 144), 'xxhdpi', False, 'WEBP', False),
    ('res/SOJ.webp', (516, 192), 'xxxhdpi', False, 'WEBP', False),

    # yt_wordmark_header_dark (PNG)
    ('res/yrm.png', (122, 48), 'mdpi', True, 'PNG', False),
    ('res/0CS.png', (184, 72), 'hdpi', True, 'PNG', False),
    ('res/iWl.png', (244, 96), 'xhdpi', True, 'PNG', False),
    ('res/vDo.png', (366, 144), 'xxhdpi', True, 'PNG', False),
    ('res/uSw.png', (488, 192), 'xxxhdpi', True, 'PNG', False),

    # yt_wordmark_header_light (PNG)
    ('res/3dV.png', (122, 48), 'mdpi', False, 'PNG', False),
    ('res/hiC.png', (184, 72), 'hdpi', False, 'PNG', False),
    ('res/j28.png', (244, 96), 'xhdpi', False, 'PNG', False),
    ('res/ZI5.png', (366, 144), 'xxhdpi', False, 'PNG', False),
    ('res/tM3.png', (488, 192), 'xxxhdpi', False, 'PNG', False),

    # yt_ringo2_wordmark_header_dark (WEBP)
    ('res/3FK.webp', (122, 48), 'mdpi', True, 'WEBP', False),
    ('res/1zM.webp', (183, 72), 'hdpi', True, 'WEBP', False),
    ('res/pxX.webp', (244, 96), 'xhdpi', True, 'WEBP', False),
    ('res/8v1.webp', (366, 144), 'xxhdpi', True, 'WEBP', False),
    ('res/VpS.webp', (488, 192), 'xxxhdpi', True, 'WEBP', False),

    # yt_ringo2_wordmark_header_light (WEBP)
    ('res/2Gx.webp', (122, 48), 'mdpi', False, 'WEBP', False),
    ('res/IrU.webp', (183, 72), 'hdpi', False, 'WEBP', False),
    ('res/vOU.webp', (244, 96), 'xhdpi', False, 'WEBP', False),
    ('res/NDx.webp', (366, 144), 'xxhdpi', False, 'WEBP', False),
    ('res/4GT.webp', (488, 192), 'xxxhdpi', False, 'WEBP', False),

    # yt_premium_logo_text_dark (standalone text PNG)
    ('res/jv3.png', (84, 48), 'mdpi', True, 'PNG', True),
    ('res/ZHp.png', (126, 72), 'hdpi', True, 'PNG', True),
    ('res/-7q.png', (168, 96), 'xhdpi', True, 'PNG', True),
    ('res/aKw.png', (252, 144), 'xxhdpi', True, 'PNG', True),
    ('res/X0-.png', (336, 192), 'xxxhdpi', True, 'PNG', True),

    # yt_premium_logo_text_light (standalone text PNG)
    ('res/OUD.png', (84, 48), 'mdpi', False, 'PNG', True),
    ('res/_Fk.png', (126, 72), 'hdpi', False, 'PNG', True),
    ('res/oDe.png', (168, 96), 'xhdpi', False, 'PNG', True),
    ('res/nVv.png', (252, 144), 'xxhdpi', False, 'PNG', True),
    ('res/xrv.png', (336, 192), 'xxxhdpi', False, 'PNG', True),
]

for rel_path, (w, h), dpi, is_dark, fmt, is_standalone in obfuscated_header_drawables:
    full_path = os.path.join(WORK_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    if is_standalone:
        img = render_standalone_text(w, h, dpi, is_dark)
    else:
        img = render_wordmark(w, h, dpi, is_dark)
    img.save(full_path, fmt)

# Morphe / ReVanced Extended Custom Branding Headers
morphe_dpi_sizes = {
    'mdpi': (129, 48),
    'hdpi': (194, 72),
    'xhdpi': (258, 96),
    'xxhdpi': (387, 144),
    'xxxhdpi': (516, 192)
}

morphe_count = 0
for name in all_names:
    if name.startswith('res/drawable-') and 'morphe_custom_branding_header' in name and 'wordmark' in name:
        full_path = os.path.join(WORK_DIR, name)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        dpi = name.split('/')[1].replace('drawable-', '')
        w, h = morphe_dpi_sizes.get(dpi, (387, 144))
        is_dark = name.endswith('_dark.png')
        img = render_wordmark(w, h, dpi, is_dark)
        img.save(full_path, 'PNG')
        morphe_count += 1

print(f"Generated 50 native obfuscated wordmarks + {morphe_count} Morphe custom branding headers.")

print("4. Patching AndroidManifest.xml and resources.arsc...")
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

print("5. Updating APK archive...")
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

print(f"Adding {len(res_files)} modified image files to APK...")
cmd = ['zip', '-9', work_apk] + res_files
subprocess.run(cmd, cwd=WORK_DIR, check=True)

print("6. Aligning APK with zipalign...")
aligned_apk = os.path.join(WORKSPACE, 'aligned.apk')
if os.path.exists(aligned_apk):
    os.remove(aligned_apk)

subprocess.run([
    '/root/android-sdk/build-tools/35.0.0/zipalign',
    '-f', '-p', '4',
    work_apk,
    aligned_apk
], check=True)

print("7. Signing APK with apksigner...")
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

print("8. Verifying APK signature...")
subprocess.run([
    '/root/android-sdk/build-tools/35.0.0/apksigner',
    'verify',
    '-v',
    OUTPUT_APK
], check=True)

print("9. Checking badging of final APK...")
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
