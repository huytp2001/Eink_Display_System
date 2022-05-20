from flask import request, Blueprint, current_app
import datetime
from functools import wraps
from core.data import responses as resp
from core.cypherutil import *
from core.datetimeutil import *
from core import logging as log

from core.data.database import * 
from core.data import querry as dbquerry

bp = Blueprint("api/auth", __name__, url_prefix="/api/auth")

def authorize(f): 
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            token=None
            if 'access-token' in request.headers: token = request.headers['access-token']
            if not token: return resp.create('-2', 'Token is missing') 
             
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            
            db= dbconnect()
            user = db.execute(dbquerry.get_user()).fetchone()
            dbclose(db)
            
            if user['login_name'] != data['login_name']:
                return resp.create('-2', 'Wrong user name')
            
            if data['expired'] < datenum(datetime.datetime.utcnow()):
                return resp.create('-2', 'Token expired')

            return f(*args,  **kwargs)
        except:
            log.error("Authorize error")
            return resp.create('-2', 'Authorize error')
    return decorator

@bp.route('/login', methods=['POST'])  
def login():
    request_data = request.get_json()
    
    if not request_data: return resp.create('-1', 'Missing request body')
    if not 'name' in request_data: return resp.create('-1', 'The field \'name\' is required')
    if not 'pwd' in request_data: return resp.create('-1', 'The field \'pwd\' is required')
    
    hashpwd = create_hash(request_data['pwd'])
    
    login_name= request_data['name']
    login_pwd= hashpwd
     
    db= dbconnect()
    user = db.execute(dbquerry.get_user()).fetchone()
    dbclose(db)
    
    if user['login_name'] != login_name: return resp.create('-1', 'Wrong user name')
    if user['login_pwd'] != login_pwd: return resp.create('-1', 'Wrong password login')
    
    
    # todo: login with real info
    now= datetime.datetime.utcnow() + datetime.timedelta(minutes= 30)
    ip= request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    token_data= {
        'login_name': login_name,
        'ip': ip,
        'expired' : datenum(now)
    }
    
    tokenBytes = token_encode(token_data, current_app.config['SECRET_KEY']) 
    token = tokenBytes.decode('utf-8')   
    
    log.event(f'{login_name} logged in, loc: {ip}')
    return resp.create('0', 'Login success', {
        'token': token,
        'expired': formatted_date_str(now)
    })
