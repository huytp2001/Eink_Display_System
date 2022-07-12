from flask import Blueprint, request
from core.data import responses as resp
from core.data.database import *
from core.cypherutil import *
from core.data import querry as dbquerry
from api.auth import authorize

bp = Blueprint("api/sys", __name__, url_prefix="/api/sys")

@bp.route('/sys-info', methods= ['GET'])
@authorize
def sys_info():
    return resp.success()

@bp.route('/update-account', methods=['POST'])
@authorize
def update_account():
    request_data = request.get_json()
    if not request_data: return resp.create('-1', 'Missing request body')
    if not 'name' in request_data: return resp.create('-1', 'The field \'name\' is required')
    if not 'old_pwd' in request_data: return resp.create('-1', 'The field \'old_pwd\' is required')
    if not 'new_pwd' in request_data: return resp.create('-1', 'The field \'new_pwd\' is required')
    
    if not request_data['name'].strip(): return resp.create('-1', 'The field \'name\' can not be empty')
    if not request_data['old_pwd'].strip(): return resp.create('-1', 'The field \'old_pwd\' can not be empty')
    if not request_data['new_pwd'].strip(): return resp.create('-1', 'The field \'new_pwd\' can not be empty')
    
    login_name= request_data['name'].strip()
    old_pwd= create_hash(request_data['old_pwd'].strip())
    new_pwd= create_hash(request_data['new_pwd'].strip())
 
    db= dbconnect()
    user = db.execute(dbquerry.get_user()).fetchone()
    if user['login_pwd'] != old_pwd:
        dbclose(db)
        return resp.create('-1', 'Wrong password')
    
    db.execute(dbquerry.update_user(login_name, new_pwd))
    db.commit()
    dbclose(db)
    
    return resp.success()

@bp.route('/init-db', methods= ['POST'])
def init_db():
    dbinit()
    return resp.success()