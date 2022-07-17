import pexpect
import time

# Basic function include parallel -> Done
# Error Handling -> Working
# Functional -> In queue

macs = []
blue = pexpect.spawn("bluetoothctl", echo=False)
blue.sendline("power on")
blue.expect("succeeded", timeout=3)
blue.sendline("scan on")
blue.expect("bluetooth", timeout=3)
time.sleep(2)
blue.sendline("scan off")
blue.expect("bluetooth", timeout=3)
blue.sendline("devices")
blue.expect("bluetooth", timeout=3)

raw_data = blue.before.split(b"\r\n")
for data in raw_data:

    if b"JDY-23" in data:
        split_data = (data.decode("utf-8")).split()
        if len(split_data) == 4:
            macs.append(split_data[2])
        else:
            macs.append(split_data[1])

dev_list = list()
for idex,mac in enumerate(macs) :
    p = pexpect.spawn("sudo gatttool -I")
    print(f"Creating child process {idex}...")
    p.expect("LE", timeout=3)
    p.sendline(f"connect {mac}")
    p.expect("successful", timeout=3)
    print(f"Create child process {idex} success!")
    dev_list.append({'mac':mac,'cli':p})

while 1:
    data = input("Enter: ")
    if data == "exit":
        blue.sendline("exit")
        blue.expect("$", timeout=3)
        blue.close()
        for idx, dev in enumerate(dev_list):
            dev['cli'].sendline("disconnect")
            dev['cli'].expect("descriptor", timeout=3)
            dev['cli'].sendline("exit")
            dev['cli'].expect("$", timeout=3)
            dev['cli'].close()
            print(f"Kill process {idx}")
        break

    if data == "test":
        for i in range(10):
            print(f"Start round {i}")
            for dev in dev_list:    
                data = f"@s{i}|{i}@e"
                print(f"Write {data} to {dev['mac']}...")
                hex_data = "".join("{:02x}".format(ord(c)) for c in data)
                dev['cli'].sendline(f"char-write-req 0x0000f {hex_data}")
                dev['cli'].expect("successfully", timeout=3)
                print(f"Write {data} to {dev['mac']} done")
            print(f"End round {i}")
            time.sleep(6)

    else:
        for dev in dev_list:
            hex_data = "".join("{:02x}".format(ord(c)) for c in data)
            dev['cli'].sendline(f"char-write-req 0x0000f {hex_data}")
            dev['cli'].expect("successfully", timeout=3)