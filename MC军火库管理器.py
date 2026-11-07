背包={"红石":384,"铁锭":19,"粘液球":0}
while True:
    print("--红石军火库--");print("1,查看当前库存");print("2，存入物品(增加数量)");print("3，取出物品(减少数量)");print("4，退出")
    输入=input("请输入：")
    if 输入=="1":
        for 名字,数量 in 背包.items():
            print(f"{名字}:{数量}");
        print("")
    if 输入 == "2":
        while True:
