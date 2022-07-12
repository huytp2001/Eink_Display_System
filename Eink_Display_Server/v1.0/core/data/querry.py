def get_slave(mac= None):
    if mac == None:
        return (f"SELECT uid, mac, device_name, product_name, product_price, device_frame" +
                " FROM 'slave' WHERE status_code <> '-1';")
    
    return f"SELECT * FROM 'slave' WHERE mac = '{mac}' and status_code <> '-1' LIMIT 1;"

def add_slave(uid, mac, device_name, product_name, product_price, device_frame):
    return ("INSERT INTO slave(uid, mac, device_name, product_name, product_price, device_frame, status_code) " +
          f"VALUES('{uid}', '{mac}', '{device_name}', '{product_name}', '{product_price}', '{device_frame}', '0');")
    
def update_slave(uid, mac= None, device_name= None, product_name= None, product_price= None, device_frame= None, status_code=None):
    qmac= f"mac= '{mac}', "
    qdevice_name= f"device_name= '{device_name}', "
    qproduct_name= f"product_name= '{product_name}', "
    qproduct_price= f"product_price= '{product_price}', "
    qdevice_frame= f"device_frame= '{device_frame}', "
    qstatus_code= f"status_code= '{status_code}' "
    
    q= "UPDATE slave SET "
    if mac != None: q+=qmac
    if device_name != None: q+=qdevice_name
    if product_name != None: q+=qproduct_name
    if product_price != None: q+=qproduct_price
    if device_frame != None: q+=qdevice_frame
    if status_code != None: q+=qstatus_code

    if status_code == None: q = q[:-2]
    if status_code == None: q+=" "

    q+= f"WHERE uid = '{uid}';"

    return q

def get_user(): return "SELECT login_name, login_pwd from system LIMIT 1;"

def update_user(name, pwd):
    q= f"UPDATE system SET login_name = '{name}', login_pwd= '{pwd}';"
    return q