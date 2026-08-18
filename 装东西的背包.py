import time
a=["花岗岩","闪白岩","凝灰岩"]
a[1]= "钻石"
a.append("绿宝石")
for b in range(len(a)):
    print(a[b],end="  ")
print()
c=input("你要找什么：")
if c in a:
    print("有的,兄弟有的")
    time.sleep(1)
    exit(0)
else:
    print("不好意思，没有")
    time.sleep(1)
    exit(0)