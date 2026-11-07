import  time
hw="print(\"Hello_World!\")"
for i in hw:
    time.sleep(1)
    print(i,end="",flush=True)
for a in hw:
    time.sleep(0.2)
    print("\b \b", end="", flush=True)