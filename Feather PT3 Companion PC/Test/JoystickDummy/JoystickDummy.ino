#include <mcp_can.h>
#include <SPI.h>

const int SPI_CS_PIN = 17;
MCP_CAN CAN(SPI_CS_PIN);

void setup() 
{
  Serial.begin(115200);
  
  // Initialize CAN bus at 500 kbps
  if (CAN.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) == CAN_OK) 
  {
    Serial.println("CAN BUS Shield init ok!");
  } 
  else 
  {
    Serial.println("CAN BUS Shield init fail");
    while (1);
  }
  
  CAN.setMode(MCP_NORMAL);
}

void loop() 
{
  // Data for joystick 1
  byte joystick1_data[8] = {0x00, 0x10, 0x00, 0x20, 0x01, 0x00, 0x00, 0x00};
  
  // Data for joystick 2
  byte joystick2_data[8] = {0x00, 0x30, 0x00, 0x40, 0x02, 0x00, 0x00, 0x00};

  // Send joystick 1 data
  CAN.sendMsgBuf(0x00FDD6, 1, 8, joystick1_data);
  delay(100);
  
  // Send joystick 2 data
  CAN.sendMsgBuf(0x00FDD8, 1, 8, joystick2_data);
  delay(100);
}
