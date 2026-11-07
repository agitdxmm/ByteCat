箱子 = ["泥土", "泥土", "钻石", "泥土", "铁锭"]
新箱子 = []
for a in 箱子:
    if a == "泥土":
        continue
    else:
        新箱子.append(a)
print(新箱子)