from os import system
import tkinter as tk
import traceback
from PIL import (Image, ImageDraw, ImageFont, ImageTk)
system("") # 强制唤醒 Windows 的控制台颜色支持

字体 = ImageFont.truetype(r"C:\Windows\Boot\Fonts\segoe_slboot.ttf", 140)

根 = tk.Tk()
根.title("真·bootmgr 转圈（测试版结构）")
画布 = tk.Canvas(根, bg="black", highlightthickness=0)
画布.pack(fill="both", expand=True)
图 = 画布.create_image(400, 350)

def 重排(事件):
    if 事件.widget == 画布:
        画布.coords(图, 画布.winfo_width() // 2, int(画布.winfo_height() * 0.72))

根.bind("<Configure>", 重排)

帧们 = []
for i in range(119):
    画 = Image.new("RGB", (280, 280), "black")
    笔 = ImageDraw.Draw(画)
    笔.text((70, 70), chr(0xE100 + i), font=字体, fill="white")
    帧们.append(ImageTk.PhotoImage(画))

帧 = 0
def 转():
    global 帧
    try:
        画布.itemconfig(图, image=帧们[帧 % 119])
        帧 += 1
        根.after(33, 转)
    except Exception:
        traceback.print_exc()

根.bind("<Escape>", lambda e: 根.destroy())
转()
根.mainloop()