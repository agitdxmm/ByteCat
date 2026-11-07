import time
try:
    while True:
        print(r"正在删除系统(C:\Windows)，进度:█",end="",flush=True)
        for i in range(32):
            time.sleep(1)
            print("█",end="",flush=True)
        break
except KeyboardInterrupt:
    print("")
    print("行家来了，跑了")
    exit(14909570)