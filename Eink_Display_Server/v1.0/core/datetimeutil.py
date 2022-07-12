import datetime

def datenum(dt): 
    '''
    datetime -> int
    '''
    
    return int(dt.strftime("%Y%m%d%H%M%S"))

def formatted_date_str(dt): 
    '''
    datetime -> string in format dd/MM/yyyy HH:mm:ss
    '''
    
    return dt.strftime("%d/%m/%Y %H:%M:%S")