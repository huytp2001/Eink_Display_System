#include "ble.h"

SoftwareSerial bluetoothSerial(6, 5);
String BleData= "";
bool BleGettingData= false;
bool BleDataRecived= false;

void BleInit(){
  /*
   * Khởi tạo module ble
   */
  
  bluetoothSerial.begin(9600);
  while (!bluetoothSerial) {}
}
bool BleStatus(){
  /*
   * tình trạng ble
   */
  return bluetoothSerial.available();
}
void BleSleep(){
  //Serial.println("Sleep2");
  //bluetoothSerial.println("AT+SLEEP2");
}
String BleGetSerialData(){
  /*
   * Lấy dữ liệu từ serial
   * Dữ liệu có thể là các chuỗi rác, loại bỏ trước khi xử lý
   */
  if (bluetoothSerial.available()) {
    String bleData= bluetoothSerial.readString();

    if(bleData.indexOf("@s") != -1){
      BleData= "";
      bleData= bleData.substring(bleData.indexOf("@s"));
      BleGettingData= true;
      BleDataRecived= false;
    }

    if(BleGettingData){
      BleData+= bleData;
    }

    if(bleData.indexOf("@e") != -1){
      bleData= bleData.substring(bleData.indexOf(0, bleData.indexOf("@e")+2));
      BleGettingData= false;
      BleDataRecived= true;
    }
  }
  
  if(BleDataRecived){
    BleData.replace("@s", "");
    BleData.replace("@e", "");
    
    if(BleData.length()<2){BleDataRecived= false; BleData= ""; return "";}

    int firstCmdCharIndex= -1;
    for(int i=0; i< BleData.length(); i++){
      if(BleData[i] == '!'){ firstCmdCharIndex = i; break; }
      if(BleData[i] == '@'){ firstCmdCharIndex = i; break; }
      if(BleData[i] == '#'){ firstCmdCharIndex = i; break; }
    }

    if(firstCmdCharIndex == -1){BleDataRecived= false; BleData= ""; return "";}
      
    int secondCmdCharIndex= -1;
    for(int i=firstCmdCharIndex+1; i< BleData.length(); i++){
      if(BleData[i] == '!'){ secondCmdCharIndex = i; break; }
      if(BleData[i] == '@'){ secondCmdCharIndex = i; break; }
      if(BleData[i] == '#'){ secondCmdCharIndex = i; break; }
    }
    if(secondCmdCharIndex != -1){
      String crrCmd= BleData.substring(firstCmdCharIndex, secondCmdCharIndex);
      BleData= BleData.substring(secondCmdCharIndex);
      return crrCmd;
    }
    else{
      String cmdString= BleData;
      BleData= "";
      return cmdString;
    }
  }

  return "";
}
