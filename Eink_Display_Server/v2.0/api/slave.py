from flask import *
import threading
from core.data import responses as resp
from core.data.database import dbconnect
from core.bleutils.ble_linux import BLE_Controller
from core.data.database import *
from core.data import querry as dbquerry
import uuid
import traceback
from api.auth import authorize
from app import get_threads, init_threads, remove_threads 
import time

bp = Blueprint("api/slave", __name__, url_prefix="/api/slave")

ble_control = BLE_Controller()

@bp.route('/all', methods=['GET'])
@authorize
def getall():
    data= []
   
    init_threads()
    db= dbconnect()
    dbdata= db.execute(dbquerry.get_slave())
    for row in dbdata:
        runtime= 0

        def x(y): ble.bleappendthread(y)

        threading.Thread(target=x(row['mac'])).start()
        
        threads= get_threads()
        for thread in threads:
            if thread['mac'] == row['mac']:
                runtime= 1
        
        data.append({
            'mac': row['mac'],
            'device_name': row['device_name'], 
            'product_name': row['product_name'], 
            'product_price': row['product_price'],
            'run_time': runtime
        })
    dbclose(db)
    
    print(get_threads())
    return resp.success(data= data)

@bp.route('/get', methods=['GET'])
@authorize
def get():
    mac = request.args.get('mac')
    
    if mac == None: return resp.create('-1', 'Provide a mac address to peform this action')
    data= None
    db= dbconnect()
    current_slave = db.execute(dbquerry.get_slave(mac)).fetchone()
    if current_slave == None: return resp.create('-1', f'Slave with mac equals to {mac} not found')
    
    data= {
        'mac': current_slave['mac'],
        'device_name': current_slave['device_name'], 
        'product_name': current_slave['product_name'], 
        'product_price': current_slave['product_price']
    }
    dbclose(db)
    
    return resp.success(data= data)

@bp.route('/remove', methods=['POST'])
@authorize
def remove():
    mac = request.args.get('mac')
    
    threads= get_threads()
    if len(threads) != 0:
        for thread in threads:
            if thread['mac'] == mac:
                curr= get_threads(mac)
                remove_threads(curr)

    db= dbconnect()
    current_slave = db.execute(dbquerry.get_slave(mac)).fetchone()
    if current_slave == None: return resp.create('-1', f'Slave with mac equals to {mac} not found')
    db.execute(dbquerry.update_slave(current_slave['uid'], mac= mac, status_code= '-1'))
    db.commit()
    dbclose(db)
    
    return resp.success()

@bp.route('/update', methods=['POST'])
@authorize
def update():
    mac = request.args.get('mac')
    name = request.args.get('name')

    db= dbconnect()
    current_slave = db.execute(dbquerry.get_slave(mac)).fetchone()
    if current_slave == None: return resp.create('-1', f'Slave with mac equals to {mac} not found')
    db.execute(dbquerry.update_slave(current_slave['uid'], device_name = name))
    db.commit()
    dbclose(db)
    
    return resp.success()

@bp.route('/scan', methods=['GET'])
@authorize
def scan():
    device_list= ble.blescan()
    
    db= dbconnect()
    for device in device_list[::-1]:
        current_slave = db.execute(dbquerry.get_slave(device['mac'])).fetchone()
        if current_slave != None: 
            device_list.remove(device)
        
    dbclose(db) 
    
    return resp.success(data= device_list)
    
@bp.route('/add', methods=['POST'])
@authorize
def add():
    req_json = request.get_json()
    mac= req_json['mac']
    device_name= req_json['device_name']
    product_name= req_json['product_name']
    product_price= req_json['product_price']
    
    ble.bleappendthread(mac)

    db= dbconnect()
    current_slave = db.execute(dbquerry.get_slave(mac)).fetchone()
    if current_slave != None: 
        dbclose(db)
        return resp.create('-1', f'Slave with mac {mac} is already exists, remove it first.')
    
    result= db.execute(dbquerry.add_slave(str(uuid.uuid4()), mac, device_name, product_name, product_price, ''))
    db.commit()
    dbclose(db)
    
    return resp.success()

@bp.route('/disp-product', methods=['POST'])
@authorize
def display_product():
    try:
        req_json = request.get_json()
        mac= req_json['mac']
        product_name= req_json['product_name']
        product_price= req_json['product_price']

        # bleclient= ble.bleconnect(mac)
        listble= get_threads()
        # print(listble)
        if len(listble) == 0:
            return resp.failed("No device connected")
            
        for x in listble:
            if x['mac'] == mac:
                bleclient = x['client']
                
                ble.blewrite(bleclient, 'wake')
                
                ble.blewrite(bleclient, f'@s{product_name}|{product_price}@e')  
        
        db= dbconnect()
        current_slave = db.execute(dbquerry.get_slave(mac)).fetchone()
        
        result= db.execute(dbquerry.update_slave(current_slave['uid'], None, None, product_name, product_price, None, None))

        db.commit()
        dbclose(db)
        
        return resp.success()
    except:
        traceback.print_exc()
        return resp.failed()

@bp.route('/disp-product-name', methods=['POST'])
@authorize
def display_product_name():
    try:
        req_json = request.get_json()
        mac= req_json['mac']
        product_name= req_json['product_name']
        type_func= req_json['type']
        
        if type_func == 'test':
            bleclient= ble.bleconnect(mac)      
            
            ble.blewrite(bleclient, 'wake')
            ble.blewrite(bleclient, f'@s{product_name}|@e')
            ble.bledisconnect(bleclient)

        if type_func == 'notest':
            listble= get_threads()
            # print(listble)
            if len(listble) == 0:
                return resp.failed()
            for x in listble: 
                if x['mac'] == mac:
                    bleclient = x['client']

                    ble.blewrite(bleclient, f'@s{product_name}|@e')

            db= dbconnect()
            current_slave = db.execute(dbquerry.get_slave(mac)).fetchone()
            
            result= db.execute(dbquerry.update_slave(current_slave['uid'], None, None, product_name, None, None, None))

            db.commit()
            dbclose(db)
        
        return resp.success()
    except:
        traceback.print_exc()
        return resp.failed()

@bp.route('/disp-product-price', methods=['POST'])
@authorize
def display_product_price():
    try:
        req_json = request.get_json()
        mac= req_json['mac']
        product_price= req_json['product_price']
        type_func= req_json['type']

        if type_func == 'test':
            bleclient= ble.bleconnect(mac)
            ble.blewrite(bleclient, 'wake')
            ble.blewrite(bleclient, f'@s|{product_price}@e')
            ble.bledisconnect(bleclient)
 
        if type_func == 'notest':     
            # bleclient= ble.bleconnect(mac)
            listble= get_threads()
            if len(listble) == 0:
                return resp.failed()
            # print(listble)
            for x in listble: 
                if x['mac'] == mac:
                    bleclient = x['client']
                    ble.blewrite(bleclient, f'@s|{product_price}@e')
            # ble.bledisconnect(bleclient)   
            db= dbconnect()
            current_slave = db.execute(dbquerry.get_slave(mac)).fetchone()
            
            result= db.execute(dbquerry.update_slave(current_slave['uid'], None, None, None, product_price, None, None))

            db.commit()
            dbclose(db)
        
        return resp.success()
    except:
        return resp.failed()

@bp.route('/disp-refresh', methods=['POST'])
@authorize
def display_refresh():
    try:
        req_json = request.get_json()
        mac= req_json['mac']
        type_func= req_json['type']

        if type_func == 'test':
            bleclient= ble.bleconnect(mac)
            ble.blewrite(bleclient, '@s')
            ble.blewrite(bleclient, '@dr -')
            ble.blewrite(bleclient, '@e')
            ble.bledisconnect(bleclient)
        
        if type_func == 'notest':
            # bleclient= ble.bleconnect(mac)
            listble= get_threads()
            if len(listble) == 0:
                return resp.failed()
            # print(listble)
            for x in listble: 
                if x['mac'] == mac:
                    bleclient = x['client']
                    ble.blewrite(bleclient, 'wake')
                    ble.blewrite(bleclient, '@srefresh@e')
        
        return resp.success()
    except:
        return resp.failed()

@bp.route('/disp-refresh-all', methods=['POST'])
@authorize
def display_refresh_all():
    try:
        db= dbconnect()
        all_slave = db.execute(dbquerry.get_slave()).fetchall()

        dbclose(db)  
        for slave in all_slave:
            # bleclient= ble.bleconnect(slave['mac'])
            listble= get_threads()
            if len(listble) == 0:
                return resp.failed("No device connected")
            # print(listble)
            for x in listble: 
                if x['mac'] == slave['mac']:
                    bleclient = x['client']
                    ble.blewrite(bleclient, 'wake')
                    ble.blewrite(bleclient, '@srefresh@e')

        return resp.success()
    except:
        return resp.failed()

@bp.route('/connect', methods=['POST'])
@authorize
def connectSlave():
    try:
        mac= request.args.get('mac')
        bleclient= ble.bleappendthread(mac)

        if bleclient is None:
            return resp.failed()

        return resp.success()
    except:
        return resp.failed()
