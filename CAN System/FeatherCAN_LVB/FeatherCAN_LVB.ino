/*  receive a frame from can bus

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

#include <SPI.h>
#include "mcp_can.h"

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

unsigned char CANbuf[2] = {0};
unsigned long CANID = 0x07;
unsigned char len = 0;
long timer = 0;
int ContactorTrigger = 1;
int prevContactorTrigger = 0;

#define SPI_CS_PIN  17 

MCP_CAN CAN(SPI_CS_PIN);                                    // Set CS pin


void setup()
{
   pinMode(6, INPUT); // PixHawk Imput pin
   
    Serial.begin(115200);
    
    // below code need for OBD-II GPS Dev Kit Atemga32U4 version
    // pinMode(A3, OUTPUT);
    // digitalWrite(A3, HIGH);
    
    // below code need for OBD-II GPS Dev Kit RP2040 version
    // pinMode(12, OUTPUT);
    // digitalWrite(12, HIGH);
    
    while (CAN_OK != CAN.begin(CAN_500KBPS))    // init can bus : baudrate = 500k
    {
        Serial.println("CAN BUS FAIL!");
        delay(100);
    }
    Serial.println("CAN BUS OK!");
}


void loop()
{
  //ContactorTrigger = digitalRead(6);

  if(ContactorTrigger == 1 && prevContactorTrigger == 0)
  {
    CANbuf[0] = ContactorTrigger;
    CANbuf[1] = 0;
    CAN.sendMsgBuf(CANID, 1, sizeof(CANbuf), CANbuf);

    delay(4000);

    CANbuf[0] = ContactorTrigger;
    CANbuf[1] = ContactorTrigger;

    CAN.sendMsgBuf(CANID, 1, sizeof(CANbuf), CANbuf);
  }
  else
  {
    CANbuf[0] = ContactorTrigger;
    CANbuf[1] = ContactorTrigger;
    CAN.sendMsgBuf(CANID, 1, sizeof(CANbuf), CANbuf);
  }
  unsigned char len = 0;
  unsigned char buf[12];
  
  if(CAN_MSGAVAIL == CAN.checkReceive())            // check if data coming
  {
    Serial.println("CAN BUS OK!");
      CAN.readMsgBuf(&len, buf);    // read data,  len: data length, buf: data buf

      unsigned long canId = CAN.getCanId();
      
      Serial.println("-----------------------------");
      Serial.print("Get data from ID: ");
      Serial.println(canId, DEC);

      for(int i = 0; i<len; i++)    // print the data
      {
          Serial.print(buf[i], DEC);
          Serial.print("\t");
      }
      Serial.println();
  }
  prevContactorTrigger = ContactorTrigger;
}

// END FILE
