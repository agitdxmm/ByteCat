if __name__=="__main__":
    while True:
        a = input("请输入数字：")
        if a.isdigit():
            a = int(a)
            for i in range(1, a + 1):
                print(f"{i}的平方：{i * i}")
            break
        else:
            print("这不是数字，重新来")
