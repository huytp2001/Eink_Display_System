#ifndef INPUT_H
#define INPUT_H

#include <Arduino.h>

extern const char CMD_SYS;
extern const char CMD_DISP_NAME;
extern const char CMD_DISP_PRICE;

extern const char* CMD_SYS_DISP_WIPE_UPDATE;
extern const char* CMD_SYS_DISP_REFRESH;

String GetSerialData();
char GetCmdChar(String src);
String GetCmdData(String src);
String GetSysCmd(String src);
String GetSysCmdData(String src);

#endif
