import hashlib
import jwt
import datetime

TEXT_ENCODING= 'UTF-8' 

def create_hash(src): 
    '''
    Lấy hash string (SHA256)
    '''
    
    return str(hashlib.sha256(src.encode(TEXT_ENCODING)).hexdigest())

def token_encode(data, key):
    '''
    Tạo jwt token từ obj và key
    '''
    
    return jwt.encode(data, key)

def token_decode(token, key):
    '''
    Lấy token data từ token
    '''
    
    return str(jwt.decode(token, key))

def get_token(request):
    '''
    Lấy access token từ request (nếu có)
    '''
    
    if 'access-token' in request.headers: return request.headers['access-token']
    return ''