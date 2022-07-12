from flask import jsonify

def create(code: str, msg: str, data= None):  
    '''
    create json response with code, message and data
    '''
    
    if data == None: response= { 'code': code, 'msg': msg }
    else: response= { 'code': code, 'msg': msg, 'data': data}

    return jsonify(response)

def success(data= None):
    '''
    create json response with data with default success
    response value
    '''
    
    if data == None: response= { 'code': '0', 'msg': 'Success' }
    else: response= { 'code': '0', 'msg': 'Success', 'data': data}
    
    return jsonify(response)

def failed(data= None):
    '''
    create json response with data with default failed
    response value
    '''
    
    if data == None: response= { 'code': '-1', 'msg': 'Failed' }
    else: response= { 'code': '-1', 'msg': 'Failed', 'data': data}
    
    return jsonify(response)