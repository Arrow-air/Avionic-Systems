#ifndef APDESC_H
#define APDESC_H

#include <Arduino.h>
#include <SPI.h>

using namespace std;

/* APD ESC Data buffer format
  0: Voltage Low 
  1: Voltage High
  2: Temperature Low 
  3: Temperature High
  4: Bus Current Low
  5: Bus Current High
  6: Reserved (Not Used)
  7: Reserved (Not Used)
  8: ERPM 1
  9: ERPM 2
  10: ERPM 3
  11: ERPM 4
  12: Throttle Duty Low
  13: Throttle Duty High
  14: Motor Duty Low
  15: Motor Duty High
  16: Status Flags
  17: Reserved (Not Used)
  18: Fletcher Checksum Low
  19: Fletcher Checksum High
  20: Stop Byte Low
  21: Stop Byte High
*/

class APDESC
{
 typedef struct  
  {
    // Voltage
    int V_HI;
    int V_LO;

    // Temperature
    int T_HI;
    int T_LO;

    // Current
    int I_HI;
    int I_LO;

    // Reserved
    int R0_HI;
    int R0_LO;

    // eRPM
    int RPM0;
    int RPM1;
    int RPM2;
    int RPM3;

    // Input Duty
    int DUTYIN_HI;
    int DUTYIN_LO;

    // Motor Duty
    int MOTORDUTY_HI;
    int MOTORDUTY_LO;

    // Reserved
    int R1;

    //Status Flags
    int statusFlag;

    // checksum
    int CSUM_HI;
    int CSUM_LO;
  } telem_t;

  public: typedef struct  
  {
    // Voltage
    float currentVoltage;

    // Temperature
    float currentTemp;

    // Current
    int currentAmpsInput;

    // eRPM
    int currentRPM;

    // Input Duty
    int currentThrottle;

    // Motor Duty
    int currentMotorDuty;

    //Status Flags
    int currentStatus;
  } data_t;

  telem_t telemdata; //APD ESC Telemetry format struct
  data_t printdata;

  int i = 0;
  int j = 0;
  unsigned char len = 0;
  unsigned char CANbuf[8] = {0};

  public:
    APDESC();
    ~APDESC();
    int HandleSerialData(unsigned char * buffer, size_t buffersize);
    int CheckFlectcher16(unsigned char * buffer);
    int PrintDataTable(data_t printdata);
};
#endif