import pexpect
import asyncio
from bleak import discover
from .bleerror import BLEError
from app import add_threads, get_threads

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

    