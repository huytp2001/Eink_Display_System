import pexpect
import asyncio
from bleak import discover
from .bleerror import BLEError
from app import add_threads, get_threads
import time

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
                    raise BLE_Error(f"BLE_Error in command {command}")

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


# ==================================================================================================


def blescan():
    '''
    Lấy danh sách thiết bị bluetooth ble xung quanh
    '''
    
    data= []
    devices= [None]
    async def run(): devices[0] = await discover()

    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(run())
    
    for d in devices[0]: data.append({'mac': d.address, 'network_name': d.name})
    
    return data    

# mac= '20:05:11:11:11:C1'

def bleconnect(mac, timeout= 2):
    client= pexpect.spawn('sudo gatttool -I')
    try:
        # client.sendline(f'letmein')
        client.expect('LE', timeout= timeout)
        client.sendline(f'connect {mac}')
        client.expect('successful', timeout= timeout)
    except: raise BLEError(f'Connect to {mac} failed')

    return client

def bleappendthread(mac, timeout= 2):
    try:
        listthreads= get_threads()
        if len(listthreads) != 0:
            for t in listthreads:
                if t['mac'] == mac:
                    return
        
        bleclient= bleconnect(mac)
        add_threads({
            'mac': mac,
            'client': bleclient
        })
        
        return bleclient
    except: pass
    

def blewrite(client, data: str, timeout= 2):
    try:
        hex_data= "".join("{:02x}".format(ord(c)) for c in data)

        client.sendline(f'char-write-req 0x0000f {hex_data}')
        client.expect('successfully', timeout= timeout)
    except: raise BLEError(f'Write data failed')

def bledisconnect(client, timeout= 2):
    try:
        client.sendline(f'exit')
        # client.expect('descriptor', timeout= timeout)
        client.close()
    except: pass # raise BLEError(f'Disconnect failed')

    