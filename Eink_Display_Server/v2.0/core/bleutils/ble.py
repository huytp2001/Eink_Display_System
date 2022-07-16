import pexpect
import time
import os


class BLE_Error(Exception):
    pass


class BLE_Controller():
    def __init__(self):
        self.bluectl = pexpect.spawn("bluetoothctl", echo=False)
        self.gatttool = pexpect.spawn("sudo gatttool -I", echo=False)

    def SentCommand(self, child: str, command: str, expect: str, timeout=3, attempts=5):
        attempt = 0
        success = False
        while not success and attempt < attempts:
            try:
                if child == "bluectl":
                    self.bluectl.sendline(command)
                    self.bluectl.expect(expect, timeout=timeout)
                if child == "gatttool":
                    self.gatttool.sendline(command)
                    self.gatttool.expect(expect, timeout=timeout)
                success = True
            except:
                attempt += 1
                if attempt >= attempts:
                    raise BLE_Error("BLE_Error!!")

    def Scan(self, scan_time: int):
        # Return a list of Eink device
        devs = []

        self.SentCommand("bluectl", "power on", "succeeded")
        self.SentCommand("bluectl", "scan on", "bluetooth")
        time.sleep(scan_time)
        self.SentCommand("bluectl", "scan off", "bluetooth")
        self.SentCommand("bluectl", "devices", "bluetooth")

        raw_data = self.bluectl.before.split(b"\r\n")
        for data in raw_data:
            if b"JDY-23" in data:
                split_data = (data.decode("utf-8")).split()
                if len(split_data) == 4:
                    devs.append({"mac": split_data[2], "name": split_data[3]})
                else:
                    devs.append({"mac": split_data[1], "name": split_data[2]})
        return devs

    def SentData(self, mac: str, data: str, attempts: int):
        # Send data to exactly one Eink specficy by mac address

        self.SentCommand("gatttool", f"connect {mac}", "successful")
        hex_data = "".join("{:02x}".format(ord(c)) for c in data)
        self.SentCommand(
            "gatttool", f"char-write-req 0x0000f {hex_data}", "successfully")
        self.SentCommand("gatttool", "disconnect", "descriptor")


if __name__ == "__main__":
    devs = []
    ble = BLE_Controller()
    while 1:
        command = input("Enter: ")
        command_list = command.split()
        if command_list[0] == "scan":
            devs = ble.Scan(2)
            for dev in devs:
                print(dev['mac'], dev['name'])

        if command_list[0] == "send":
            ble.SentData(command_list[1], command_list[2], 5)

        if command_list[0] == "refresh":
            devs = ble.Scan(2)
            for dev in devs:
                ble.SentData(dev['mac'], "@srefresh@e", 5)

        if command_list[0] == "send_all":
            devs = ble.Scan(2)
            for dev in devs:
                ble.SentData(dev['mac'], command_list[1], 5)

        if command_list[0] == "exit":
            break

        if command_list[0] == "clear":
            os.system("clear")

        if command_list[0] == "help":
            print("scan:              Scan for nearby Eink device\nsend {mac} {data}: Send {data} to Eink device with {mac} address\nrefresh:           Refresh all Eink devices\nsend_all {data}:   Send {data} to all Eink devices nearby\nclear:             Clear screen\nexit:              Exit this CLI\nhelp:              Show this help")




