import os
import time
import winreg
import qrcode
import sys
sys.stdout.reconfigure(encoding="utf-8")
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
desktop, _ = winreg.QueryValueEx(key, "Desktop")
desktop: str = os.path.expandvars(desktop)
img=qrcode.make("看到的是gay")
img.save(os.path.join(desktop, "二维码.png"))
qr = qrcode.QRCode(border=1)
qr.add_data("看到的是gay")
qr.make()
matrix = qr.get_matrix()
for 行 in matrix:
    for 块 in 行:
        if 块:
            print("\x1b[40m  \x1b[0m", end="")
        else:
            print("\x1b[47m  \x1b[0m", end="")
    print()
print("输出成功，如果无法扫描，可以打开桌面的二维码.png,此窗口2分钟后关闭")
time.sleep(120)