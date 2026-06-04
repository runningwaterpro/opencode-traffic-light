#!/usr/bin/env python3
"""生成交通灯图标"""

from PIL import Image, ImageDraw

def generate_circle_icon(color, filename):
    """生成圆形图标"""
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, 60, 60], fill=color)
    img.save(filename)
    print(f"生成: {filename}")

if __name__ == "__main__":
    # 颜色定义（接近真实交通灯）
    generate_circle_icon((220, 20, 20), "red.png")      # 红色
    generate_circle_icon((20, 180, 20), "green.png")    # 绿色
    generate_circle_icon((220, 180, 20), "yellow.png")  # 黄色
    generate_circle_icon((128, 128, 128), "gray.png")   # 灰色
