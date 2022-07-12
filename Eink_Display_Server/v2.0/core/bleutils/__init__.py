# không tìm thấy thư viện ble hoạt động trên windows
# nếu chạy code trên windows, chạy dữ liệu mẫu
# nếu chạy trên linux, có cài sẵn gatttool, chạy code thật

#usage: import package hiện tại, xong <bleutils>.???

import os 
if os.name != 'nt': from .ble_linux import * # import code nếu chạy trên linux
else: from .ble_windows import * # code nếu chạy trên windows