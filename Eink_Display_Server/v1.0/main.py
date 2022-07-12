from app import create_app

if __name__ == "__main__": 
    app = create_app()  
    app.run(host='0.0.0.0')

# from functools import wraps
# import traceback

# def log_decorator(retries= 3):
#     def actual_decorator(f):
#         @wraps(f)
#         def wrapper(*args, **kwargs):
#             tries= 0
#             while True:
#                 if tries >= retries: break
                
#                 try: return f(*args,  **kwargs)
#                 except:
#                     tries+=1
#                     print(traceback.format_exc())
#         return wrapper
#     return actual_decorator