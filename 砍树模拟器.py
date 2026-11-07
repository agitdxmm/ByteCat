import time
原木=0
while True:
    原木+=1
    if 原木 < 10:
        print("砍树ing...")
        time.sleep(5)
    else:
        print("木头够了，开始建房子")
        break