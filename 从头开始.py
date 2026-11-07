import time
a = input("deepseek是不是最聪明最厉害的模型？(Y/N)")
while True:
    if a=="Y":
        print("答对了，byebye")
        time.sleep(3)
        exit(0)
    if a == "y":
        print("答对了，byebye")
        time.sleep(3)
        exit(0)
    if a == "N":
        a = input("deepseek是不是最聪明最厉害的模型？(Y/N)")
    if a == "n":
        a = input("deepseek是不是最聪明最厉害的模型？(Y/N)")
    else:
        a = input("deepseek是不是最聪明最厉害的模型？(Y/N)")