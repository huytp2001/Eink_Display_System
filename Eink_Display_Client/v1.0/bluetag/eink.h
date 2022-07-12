#ifndef EINK_H
#define EINK_H

#include <GxEPD2_BW.h>
#include <Fonts/FreeSerifBold12pt7b.h>

#define MAX_DISPLAY_BUFFER_SIZE 800
#define MAX_HEIGHT(EPD) (EPD::HEIGHT <= MAX_DISPLAY_BUFFER_SIZE / (EPD::WIDTH / 8) ? EPD::HEIGHT : MAX_DISPLAY_BUFFER_SIZE / (EPD::WIDTH / 8))

class EinkDisplay{
  public:  
    EinkDisplay();
    ~EinkDisplay();
    void Init(); // Khởi tạo module
    void UpdateProduct(String productName, String productPrice); // Cập nhật thông tin hiển thị
    void SetWipeOnUpdate(bool value); // Set chức năng làm mới lúc cập nhật
    bool GetWipeOnUpdate(); // Lây thông tin thiết lập có làm mới lúc cập nhật
    void DrawFrame();
  private:
    bool clearOnUpdate;
};
#endif
