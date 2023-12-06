#ifndef ENNOIDBMS_H
#define ENNOIDBMS_H

#include <Arduino.h>
#include <SPI.h>
#include "mcp_can.h"

#define SPI_CS_PIN  17
 
class EnnoidBMS
{
  public: typedef struct  
  {
    // Voltage
    float currentVoltage;

    // Temperature
    float currentTemp;

    // Current
    float currentAmps;

    // eRPM
    float CellData;

    //Status Flags
    int currentStatus;
  } data_t;

  data_t printdata;
  
  EnnoidBMS();
  ~EnnoidBMS();

  public:
    int HandleCANData(unsigned char * buffer, size_t buffersize,unsigned long ID);
    int PrintDataTable(data_t printdata);
};
#endif