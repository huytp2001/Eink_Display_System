class BLEError(Exception):
    def __init__(self, msg): 
        super().__init__(f'BLE Error: {msg}')