/*
  Outputs Telemetry Data Emulating an APD ESC
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
#include <SoftwareSerial.h>


// Voltage
    int V_HI = 255;
    int V_LO = 255;

    // Temperature
    int T_HI = 255;
    int T_LO = 255;

    // Current
    int I_HI = 255;
    int I_LO = 255;

    // Reserved
    int R0_HI = 255;
    int R0_LO = 255;

    // eRPM
    int RPM0 = 255;
    int RPM1 = 255;
    int RPM2 = 255;
    int RPM3 = 255;

    // Input Duty
    int DUTYIN_HI = 255;
    int DUTYIN_LO = 255;

    // Motor Duty
    int MOTORDUTY_HI = 255;
    int MOTORDUTY_LO = 255;

    // Reserved
    int R1 = 255;

    //Status Flags
    int statusFlag = 255;

    // checksum
    int CSUM_HI = 255;
    int CSUM_LO = 255;

    int Stop_HI = 255;
    int Stop_LO = 255;

    int Buffer[22] = {V_HI,V_LO,T_HI,T_LO,I_HI,I_LO,R0_HI,R0_LO,RPM0,RPM1,RPM2,RPM3,DUTYIN_HI,DUTYIN_LO,MOTORDUTY_HI,MOTORDUTY_LO,R1,statusFlag,CSUM_HI,CSUM_LO,Stop_HI,Stop_LO};

SoftwareSerial mySerial(10, 11); // RX, TX

void setup() 
{
  pinMode(9, OUTPUT); //contactor pin
  Serial.begin(9600);
  mySerial.begin(115200);
}

void loop() {

  if (Serial.available()) 
  {
    for(int i = 0; i < sizeof(Buffer)/2; i++)
    {
      mySerial.write(Buffer[i]);  // read it and send it out Serial1 (pins 0 & 1)
      Serial.println(Buffer[i]);
      digitalWrite(9, 1);
      delay(1);
    }  
  }
}
