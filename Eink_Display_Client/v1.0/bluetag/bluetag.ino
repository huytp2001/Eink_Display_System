/*
 * Thiết bị Bảng giá cho siêu thị sử dụng bluetooth ble
 * Gửi lệnh dưới dạng chuỗi qua port serial PC (hoặc TX, RX)
 *  hoặc qua thiết bị bluetooth ble
 * Các lệnh hiện có:
 * !<Chuỗi>
 * >> !San Pham
 * Cập nhật tên hiển thị
 * 
 * #<Chuỗi>
 * >> #100k
 * Cập nhật giá hiển thị
 * 
 * @dr -
 * >> @dr -
 * Làm mới màn hình
 * 
 * @sduw [1, 0]
 * @sduw 1
 * bật- tắt chúc năng làm mới lúc cập nhật màn hình
 */


#include "LowPower.h"
#include "eink.h"
#include "input.h"
#include "ble.h"

String productName= ""; // Tên sản phẩm
String productPrice= ""; // Giá sản phẩm
EinkDisplay eink;
int cout=0;
void setup() {
  /*
   * Khởi tạo PC serial
   * Khởi tạo màn hình
   * Khởi tạo Serial của BLE
   */
  
  Serial.begin(9600);
  while (!Serial) { }

  // for (byte i = 0; i <= A5; i++){
  //     pinMode (i, OUTPUT);    // changed as per below
  //     digitalWrite (i, LOW);  //     ditto
  //   }

  eink.Init(); 
  eink.UpdateProduct(productName, productPrice);
  eink.SetWipeOnUpdate(false);

  BleInit();

  Serial.println("Ready");
}

void loop() {
  /*
   * Lần lượt lấy dữ liệu từ PC serial và BLE serial
   * Gửi dữ liệu nhận được vào hàm làm việc
   */
  Serial.println(cout);
  cout++;
  if(BleStatus()){
    delay(1000);
    Serial.println("Wake");
    
    
    int cmdSource= 2;
    if(cmdSource == 1){
      String serialData = GetSerialData();
      if(serialData!= ""){
        work(serialData);
      }
    }
    else if (cmdSource == 2){
      String bleSerialData= BleGetSerialData();
      if(bleSerialData!= ""){
        work(bleSerialData);
      }
    }
  }
    Serial.println("Sleep");
    BleSleep();
    delay(3000);
    LowPower.powerDown(SLEEP_FOREVER, ADC_OFF, BOD_OFF);
    delay(3000);
}

void work(String serialData){
  /*
   * Tiền xử lý dư liệu, tìm ra lệnh cần thực hiện
   * Sau đó thực hiện lệnh
   */
  
  char cmdChar= GetCmdChar(serialData);
  bool displayContentChanged= false; // Cờ cho biết có nên cập nhật thông tin hiển thị
  
  if(cmdChar == CMD_SYS){
    // Thực hiện lệnh hệ thống
    
    String sysCmd= GetSysCmd(serialData);
    if(sysCmd == CMD_SYS_DISP_WIPE_UPDATE){
      // Lệnh set chức năng làm mới lúc cập nhật
      String sysCmdData= GetSysCmdData(serialData);
      if(sysCmdData == "0"){
        // Tắt
        
        // Serial.println("Wipe 1");
        eink.SetWipeOnUpdate(false);
      }
      else if (sysCmdData == "1"){
        // Bật
        
        // Serial.println("Wipe 0");
        eink.SetWipeOnUpdate(true);
      }
    }
    else if(sysCmd == CMD_SYS_DISP_REFRESH){
      // Làm mới màn hình
      
       Serial.println("Refresh");
      bool wipeOnUpdate= eink.GetWipeOnUpdate();
      eink.SetWipeOnUpdate(true);
      eink.UpdateProduct(productName, productPrice);
      eink.SetWipeOnUpdate(wipeOnUpdate);
    }
  }
  else{
    // Thực hiện lệnh cập nhật thông tin
    
    String cmdData= GetCmdData(serialData);
    
    if (cmdChar == CMD_DISP_NAME){
       Serial.print("N ");
       Serial.println(cmdData);

      productName= cmdData;
      displayContentChanged= true;
    }
    else if (cmdChar == CMD_DISP_PRICE){
       Serial.print("P ");
       Serial.println(cmdData);

      productPrice= cmdData;
      displayContentChanged= true;
    }
  }

  // Tiến hành cập nhật thông tin hiển thị nếu cần thiết  
  if (displayContentChanged){
    eink.UpdateProduct(productName, productPrice);
  }
}
