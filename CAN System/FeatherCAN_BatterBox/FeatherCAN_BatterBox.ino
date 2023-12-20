/* ARROW AIR 2023
  Utilises the CANbed Board as a bus bridge from UART to CAN for ESC and BMS Telemetry
*/

/*
   CAN Baudrate,
    
    #define CAN_5KBPS           1
    #define CAN_10KBPS          2
    #define CAN_20KBPS          3
    #define CAN_25KBPS          4 
    #define CAN_31K25BPS        5
    #define CAN_33KBPS          6
    #define CAN_40KBPS          7
    #define CAN_50KBPS          8
    #define CAN_80KBPS          9
    #define CAN_83K3BPS         10
    #define CAN_95KBPS          11
    #define CAN_100KBPS         12
    #define CAN_125KBPS         13
    #define CAN_200KBPS         14
    #define CAN_250KBPS         15
    #define CAN_500KBPS         16
    #define CAN_666KBPS         17
    #define CAN_1000KBPS        18

    CANBed V1: https://www.longan-labs.cc/1030008.html
    CANBed M0: https://www.longan-labs.cc/1030014.html
    CAN Bus Shield: https://www.longan-labs.cc/1030016.html
    OBD-II CAN Bus GPS Dev Kit: https://www.longan-labs.cc/1030003.html
*/



/* Please modify SPI_CS_PIN to adapt to your board.

   CANBed V1        - 17
   CANBed M0        - 3
   CAN Bus Shield   - 9
   CANBed 2040      - 9
   CANBed Dual      - 9
   OBD-2G Dev Kit   - 9
   OBD-II GPS Kit   - 9
   Hud Dev Kit      - 9

   Seeed Studio CAN-Bus Breakout Board for XIAO and QT Py - D7
*/


#include <SPI.h>
#include "mcp_can.h"
#include "APDESC.h"
#include "EnnoidBMS.h"

#define SPI_CS_PIN  17 

unsigned char serialBuff[22] = {0};
unsigned char CANBuff[22];
unsigned char CANBuffin[2] = {0};

unsigned long CANID = 0x0001040A0000007F;
unsigned char len = 0;

MCP_CAN CAN(SPI_CS_PIN);                                    // Set CS pin
APDESC ESC;
//Ennoid BMS;

void setup()
{
  Serial.begin(115200);
  Serial1.begin(115200);

  pinMode(4, OUTPUT); //precharge pin
  pinMode(5, OUTPUT); //contactor pin

  digitalWrite(4, HIGH);
  delay(3000);
  digitalWrite(5, HIGH);
    
  while (CAN_OK != CAN.begin(CAN_500KBPS))    // init can bus : baudrate = 500k
  {
      Serial.println("CAN BUS FAIL!");
      delay(100);
  }
  Serial.println("CAN BUS OK!");
}

void loop()
{
  /*
  if(CAN_MSGAVAIL == CAN.checkReceive())            // check if data coming
  {
    CAN.readMsgBuf(&len, CANBuffin);    // read data,  len: data length, buf: data buf

    unsigned long canId = CAN.getCanId();

    if(canId == 0x07)
    {
      digitalWrite(4, (int)CANBuffin[0]); // precharcge
      digitalWrite(5, (int)CANBuffin[1]); // contactor

      //Serial.print(" Precharge - Contactor");
      //Serial.print((int)CANBuffin[0]);
      //Serial.print(" \t ");
      //Serial.println((int)CANBuffin[1]);
    }
    //BMS.HandleCANData(CANBuff,sizeof(CANBuff),canId);
  }
  if(Serial1.available())
  {
    Serial1.readBytes(serialBuff,22);
    Serial1.flush();
    ESC.HandleSerialData(serialBuff,sizeof(serialBuff));
    CANDataWrite();
    delay(100); 
  }
  else
  {
    Serial1.flush();
  }*/
}

int CANDataWrite()
{
  ESC.CANbuf[0] = ESC.printdata.currentStatus;
  ESC.CANbuf[1] = (int)ESC.printdata.currentVoltage;
  ESC.CANbuf[2] = ESC.printdata.currentAmpsInput;
  ESC.CANbuf[3] = ESC.printdata.currentMotorDuty;
  ESC.CANbuf[4] = ESC.printdata.currentRPM;
  ESC.CANbuf[5] = ESC.printdata.currentThrottle;
  ESC.CANbuf[6] = ESC.printdata.currentTemp;
  memset(ESC.CANbuf, CANID, sizeof(ESC.CANbuf));
  CAN.sendMsgBuf(CANID, 1, sizeof(ESC.CANbuf), ESC.CANbuf);
}
/*
int CANDataRead()
{
 
}*/