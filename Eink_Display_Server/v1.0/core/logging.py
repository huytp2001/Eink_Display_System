import traceback
import datetime

def event(msg):
    '''
    Log Sự kiện
    '''
    
    print(msg)
    print(datetime.datetime.utcnow())
    
    
def error(msg):
    '''
    Log Lỗi
    '''
    
    print(msg)
    print(datetime.datetime.utcnow())
    print(traceback.format_exc())

# def add_event(created, name, loc, desc, level):
#     events = get_events()
#     if len(events) >= MAX_EVENTS: 
#         rm_event(events[0]['created'])

#     desc = desc.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+\"\'"})
#     conn = sqlite3.connect(DBNAME)
#     conn.execute(queries.INSERT_EVENT_LOG(created, name, loc, desc, level))
#     conn.commit()
#     conn.close()

# def rm_event(created):
#     conn = sqlite3.connect(DBNAME)
#     conn.execute(queries.DELETE_EVENT_LOG(created))
#     conn.commit()
#     conn.close()

# def get_events():
#     events = []
#     conn = sqlite3.connect(DBNAME)
#     resp = conn.execute(queries.GET_ALL_EVENT_LOG)
#     for item in resp:
#         events.append({'created': datetime.strptime(item[0], '%Y-%m-%d %H:%M:%S.%f'), 'name': item[1], 'loc': item[2], 'description': item[3], 'level': item[4]})

#     conn.close()
#     return sorted(events,key= lambda k: k['created'])