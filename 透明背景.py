from PIL import Image, ImageDraw, ImageFont
from rembg import remove
import os

# 1. 设置路径（注意改成你自己的图片路径）
input_path = r"C:\Users\Administrator\Downloads\1791709242047_transparent.png"
output_path = r"E:\xmmxpy\cat_watermark.png"

print("正在动用AI进行抠图...")
# 2. 抠图（AI自动去除绿色背景，输出带透明通道的PNG）
input_img = Image.open(input_path)
output_img = remove(input_img)

# 3. 加水印
print("正在加上专属水印...")
draw = ImageDraw.Draw(output_img)

# 设置水印文字（你可以换成自己的ID）
watermark_text = "@爱玩的小喵咪"

# 加载字体（Windows系统一般都有微软雅黑）
# 如果报错找不到字体，可以把这一行改成绝对路径，比如 C:\Windows\Fonts\msyh.ttc
try:
    font = ImageFont.truetype("msyh.ttc", 30)
except IOError:
    font = ImageFont.load_default()

# 计算文字大小，放到右下角
bbox = draw.textbbox((0, 0), watermark_text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x = output_img.width - text_width - 20
y = output_img.height - text_height - 20

# 画一个黑色的半透明阴影，再加白色文字（这样在浅色背景上也能看清）
draw.text((x+2, y+2), watermark_text, font=font, fill=(0, 0, 0, 150))
draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 255))

# 4. 保存最终成果
output_img.save(output_path, "PNG")
print(f"搞定！文件已保存到：{output_path}")
