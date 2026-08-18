price=10
discount=9/10
a=int(input("你有多少元钱？"))  #依旧变量a
count=int(input("你要买多少"))
b=price*count*discount #商品价格
if a < b:
  print("余额不足,呵呵呵，哈哈哈哈哈哈哈哈哈")
elif a > b:
    print(f"收现金{b}，找零{a - b}元")
else:
    print(f"收现金{b}元，正好，无需找零")