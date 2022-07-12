#include "input.h"

const String CMD_CHARS = "@#!";

const char CMD_SYS= CMD_CHARS[0];
const char CMD_DISP_NAME = CMD_CHARS[1];
const char CMD_DISP_PRICE= CMD_CHARS[2];

const char* CMD_SYS_DISP_WIPE_UPDATE= "sduw";
const char* CMD_SYS_DISP_REFRESH= "dr";

String GetSerialData(){
  if (Serial.available() > 0) {
    String serialData= Serial.readString();
    serialData.replace("\n", "");
    return serialData;
  }

  return "";
}

bool IsValidCmd(String src){
  if (src == ""){
    return false;
  }
  
  if(src.length() < 2){
    return false;
  }

  char cmdChar= src[0];
  int loops=  CMD_CHARS.length();
  int failures= 0;
  for(int i=0; i< loops; i++){
    if (cmdChar != CMD_CHARS[i]){
      failures+=1;
    }
  }
  if(failures == loops){return false;}

  return true;
}

bool IsValidSysCmd(String src){
  if(src.length() < 4){
    return false;
  }

  if(src[0] != CMD_SYS){
    return false;
  }

  if(src.indexOf(' ') == -1){
    return false;
  }

  return true;
}

char GetCmdChar(String src){
  if(!IsValidCmd(src)){
    return 0x00;
  }

  return src.substring(0, 1)[0];
}

String GetCmdData(String src){
  if(!IsValidCmd(src)){
    return "";
  }

  return src.substring(1);
}

String GetSysCmd(String src){
  if(!IsValidSysCmd(src)){
    return "";
  }

  String cmdData= GetCmdData(src);
  int spacingIndex= cmdData.indexOf(' ', spacingIndex);
  return cmdData.substring(0, spacingIndex);
}

String GetSysCmdData(String src){
  if(!IsValidSysCmd(src)){
    return "";
  }

  String cmdData= GetCmdData(src);
  int spacingIndex= cmdData.indexOf(' ', spacingIndex);
  return cmdData.substring(spacingIndex+1);
}
