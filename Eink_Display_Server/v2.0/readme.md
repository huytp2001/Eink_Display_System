# Bluetag

## 1. Khởi tạo project
### 1.1 Tạo và sử dụng thư mục chứa project

*Đầu tiên khởi tạo thư mục chứa các thứ*

**Windows, Linux**
> `mkdir` <tên thư mục>  
> `cd` <tên thư mục>   

    mkdir bluetag
    cd bluetag

<br/><br/>

### 1.2 Khởi tạo và kích hoạt môi trường ảo

*Để tiện trong việc di chuyển, sử dụng code, ta cần cài đặt môi trường ảo*

**Windows**`
> `py -m venv `<tên thư mục chứa môi trường>  
> *<tên thư mục chứa môi trường>*`\Scripts\activate.bat`

    py -m venv env
    env\Scripts\activate.bat

<br/>

**Linux**
> `python3 -m venv `*<tên thư mục chứa môi trường>*  
> `source `*<tên thư mục chứa môi trường>*`/bin/activate`

    python3 -m venv env
    source env/bin/activate

<br/><br/>

### 1.3 Cài đặt các packages

*Danh sách package được ghi trong file, cài đặt từ đấy, khỏi mất công nhớ*

**Windows**
> `py -m pip install -r ` *<tên file chứa tên packages>*  

    py -m pip install -r packagewin.cfg


<br/>

**Linux**
> `pip3 install -r ` *<tên file chứa tên packages>*  

    pip3 install -r package.conf

<br/><br/>

## 2.Chạy project

**Windows**
> `set FLASK_APP=` *<file chứa create_app>*  
> `set FLASK_ENV=development`    
> `flask run --host `*<địa chỉ ip>*    

    set FLASK_APP=app.py
    set FLASK_ENV=development
    flask run --host 0.0.0.0

<br/>

**Linux**
> `export  FLASK_APP=` *<file chứa create_app>*  
> `export  FLASK_ENV=development`    
> `flask run --host ` *<địa chỉ ip>*   

    export FLASK_APP=app.py
    export FLASK_ENV=development
    flask run --host 0.0.0.0

## 3. Database

### 3.1 khởi tạo db

**Windows / Linux**

*Lưu ý: cần gọi chạy* `set FLASK_APP=` *<file chứa create_app>* trước, không nó không chạy  

> `flask init-db`  

    flask init-db

