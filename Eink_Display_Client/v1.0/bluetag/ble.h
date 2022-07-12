#ifndef BLE_H
#define BLE_H

#include <SoftwareSerial.h>
#include <Arduino.h>

void BleInit(); // Khởi tạo thiết bị
String BleGetSerialData(); // Lấy thông tin từ serial
bool BleStatus(); //Kiểm tra kết nối
void BleSleep();//Ngủ Ble
#endif
