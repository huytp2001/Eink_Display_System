#include "eink.h"
#include "frame.h"

GxEPD2_BW<GxEPD2_290_T5, MAX_HEIGHT(GxEPD2_290_T5)> display(GxEPD2_290_T5(/*CS=10*/ SS, /*DC=*/ 8, /*RST=*/ 9, /*BUSY=*/ 7));

EinkDisplay::~EinkDisplay() {}
EinkDisplay::EinkDisplay() {
  clearOnUpdate = true;
}

void EinkDisplay::Init() {
  display.init();
}

void EinkDisplay::UpdateProduct(String productName, String productPrice) {
  String nameLabel = "";
  String priceLabel = "";
  productName = nameLabel + productName;
  productPrice = priceLabel + productPrice;

  uint16_t x = 10; 
  uint16_t y = 70;

  display.setRotation(1);
  display.setFont(&FreeSerifBold12pt7b);
  display.setTextColor(GxEPD_BLACK);

  int16_t nameBoxX, nameBoxY;
  uint16_t nameBoxW, nameBoxH;
  display.getTextBounds(productName, x, y, &nameBoxX, &nameBoxY, &nameBoxW, &nameBoxH);

  int pricex, pricey, namex, namey;
  namex = x;
  namey = y;
  pricex = x;
  pricey = y + nameBoxH + 10;

  //display.setPartialWindow(x-2, y-15, display.width(), display.height());
  display.setPartialWindow(0, 0, display.width(), display.height());

  if (this->clearOnUpdate) {
    display.firstPage(); do {
      display.fillScreen(GxEPD_BLACK);
    } while (display.nextPage());
    display.firstPage(); do {
      display.fillScreen(GxEPD_WHITE);
    } while (display.nextPage());
  }

  display.firstPage();
  do
  {
    display.drawBitmap(0, 0, frame, display.width(), display.height(), GxEPD_BLACK);
    if (productName.length() != 0) {
      display.setCursor(namex, namey);
      display.print(productName);
    }
    if (productPrice.length() != 0) {
      display.setCursor(pricex, pricey);
      display.print(productPrice);
    }
  }
  while (display.nextPage());
}


void EinkDisplay::SetWipeOnUpdate(bool value) {
  this->clearOnUpdate = value;
}

bool EinkDisplay::GetWipeOnUpdate() {
  return this->clearOnUpdate;
}
