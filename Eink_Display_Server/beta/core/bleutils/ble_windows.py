def blescan():
    '''
    Lấy danh sách thiết bị bluetooth ble xung quanh
    '''
    
    data= [
        {'mac': '21:22:34:45:56:1', 'network_name': 'Brand new device 1'},
        {'mac': '21:22:34:45:56:2', 'network_name': 'Brand new device 2'},
        {'mac': '21:22:34:45:56:3', 'network_name': 'Brand new device 3'},
    ]
    
    return data

def bleconnect(mac):
    '''
    Kết nối với thiết bị ble theo mã mac, trả về đối tượng client (pexpect)
    '''
    pass

def bledisconnect(client):
    '''
    Đóng kết nối với thiết bị ble
    '''
    pass
    
def blewrite(client, data):
    '''
    Gửi chuỗi đến thiết bị ble
    '''
    pass