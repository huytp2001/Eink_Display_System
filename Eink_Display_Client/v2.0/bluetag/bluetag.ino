#include "LowPower.h"
#include <SoftwareSerial.h>
#include "frame.h"
#include <EEPROM.h>

#include <GxEPD2_BW.h>
#include <Fonts/FreeSerifBold12pt7b.h>

#define MAX_DISPLAY_BUFFER_SIZE 800
#define MAX_HEIGHT(EPD) (EPD::HEIGHT <= MAX_DISPLAY_BUFFER_SIZE / (EPD::WIDTH / 8) ? EPD::HEIGHT : MAX_DISPLAY_BUFFER_SIZE / (EPD::WIDTH / 8))  

SoftwareSerial bluetoothSerial(6, 5);

GxEPD2_BW<GxEPD2_290_T5, MAX_HEIGHT(GxEPD2_290_T5)> display(GxEPD2_290_T5(/*CS=10*/ SS, /*DC=*/ 8, /*RST=*/ 9, /*BUSY=*/ 7));

class EinkDisplay {
    String sName;
    String sPrice;
    
    public:
        void Init() { 
            display.init();
            display.setRotation(3);
            display.setFont(&FreeSerifBold12pt7b);
            display.setTextColor(GxEPD_BLACK);
            display.setPartialWindow(0, 0, display.width(), display.height());
        }

    void UpdateProduct(String UpName, String UpPrice) {
      display.firstPage();
      do
      {
        display.drawBitmap(0, 0, frame, display.width(), display.height(), GxEPD_BLACK);

        display.setCursor(10,75);
        if (UpName.length() != 0) {
            display.print(UpName);
            sName.reserve(UpName.length());
            sName = UpName;
          } else {
            display.print(sName);    
          }

        display.setCursor(10,110);
        if (UpPrice.length() != 0) {
            display.print(UpPrice);
            sPrice.reserve(UpPrice.length());
            sPrice = UpPrice;
          } else {
            display.print(sPrice);
            }

    }
    while (display.nextPage());
  }

  void Refresh() {
        display.firstPage(); do {
        display.fillScreen(GxEPD_BLACK);
        } while (display.nextPage());
        display.firstPage(); do {
        display.fillScreen(GxEPD_WHITE);
        } while (display.nextPage());
        display.drawBitmap(0, 0, frame, display.width(), display.height(), GxEPD_BLACK);
    }
};

class BLE_Serial {
    public:
        void Init() {
            bluetoothSerial.begin(9600); 
            while (!bluetoothSerial) {}
        }

        bool GetStatus() {
            return bluetoothSerial.available();    
        }

        void Sleep() {
            bluetoothSerial.println("AT+SLEEP2");
        }
  
        void GetSerialData(String* Name, String* Price, String* Command) {              
            if (GetStatus()) {
                String BleData = bluetoothSerial.readString();    
                if (BleData.indexOf("@s") != -1 && BleData.indexOf("@e") != -1 && BleData.indexOf("|") != -1) {
                    String sName, sPrice;
                    sName = BleData.substring(BleData.indexOf("@s")+2, BleData.indexOf("|"));
                    sPrice = BleData.substring(BleData.indexOf("|")+1, BleData.indexOf("@e"));
                    *Name = sName;
                    *Price = sPrice;
                }
                else if (BleData.indexOf("@s") != -1 && BleData.indexOf("@e") != -1 && BleData.indexOf("|") == -1) {
                    String sCommand;
                    sCommand = BleData.substring(BleData.indexOf("@s")+2, BleData.indexOf("@e"));
                    *Command = sCommand;
                  }
            }
        }
};


EinkDisplay eink;
BLE_Serial ble;

void setup() {
    Serial.begin(9600);
    while (!Serial) {}

    eink.Init();
    eink.Refresh();
    
    ble.Init();
}

void loop() {
    
    String sName, sPrice, sCommand;    
    ble.GetSerialData(&sName, &sPrice, &sCommand);
    
    if (sName.length() != 0 || sPrice.length() != 0) {
        eink.UpdateProduct(sName, sPrice);
    }

    if (sCommand.length() != 0) {
        if (sCommand == "refresh") {
            eink.Refresh();
         }
    }

    //ble.Sleep();
    // delay(3000);
    // LowPower.powerDown(SLEEP_FOREVER, ADC_OFF, BOD_OFF);
    // delay(3000);
}
