#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把原始 PNG 转成高质量 JPG，微信内置浏览器 100% 兼容。
输出到 images/，覆盖现有 .webp（先删除旧文件再写新 .jpg）。
"""
import os
from PIL import Image

SRC = "../qixi-images-clean"  # 原始无水印 PNG
DST = "images"

os.makedirs(DST, exist_ok=True)

# 先清掉旧的 webp
for f in os.listdir(DST):
    if f.endswith(".webp"):
        os.remove(os.path.join(DST, f))
        print(f"删除 {f}")

ok, fail = 0, 0
for i in range(1, 16):
    src_path = os.path.join(SRC, f"{i}.png")
    dst_path = os.path.join(DST, f"{i}.jpg")
    if not os.path.exists(src_path):
        print(f"❌ 缺源文件 {src_path}")
        fail += 1
        continue
    try:
        im = Image.open(src_path).convert("RGB")
        # 限制最大宽度 750，手机屏够用（2x 屏约需 750-828），大幅降体积
        if im.width > 750:
            ratio = 750 / im.width
            im = im.resize((750, int(im.height * ratio)), Image.LANCZOS)
        # JPG 质量 42，水彩画风手机端几乎无感，继续降体积
        im.save(dst_path, "JPEG", quality=42, optimize=True, progressive=True, subsampling=2)
        size = os.path.getsize(dst_path)
        print(f"[OK] {i}.jpg  {im.width}x{im.height}  {size//1024} KB")
        ok += 1
    except Exception as e:
        print(f"[FAIL] {i}.jpg 失败: {e}")
        fail += 1

print(f"\n完成: {ok} 成功, {fail} 失败")