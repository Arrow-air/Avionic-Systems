#include <mcp_can.h>
#include <SPI.h>

const int CAN0_CS = 17;

MCP_CAN CAN0(CAN0_CS);

void setup() 
{
  Serial.begin(115200);
  while (CAN_OK != CAN0.begin(MCP_STDEXT, CAN_500KBPS, MCP_8MHZ)) 
  {
    Serial.println("CAN BUS Shield init fail");
    Serial.println(" Init CAN BUS Shield again");
    delay(100);
  }
  Serial.println("CAN BUS Shield init ok!");
}

void loop() 
{
  sendCommandControl();
  delay(10);

  sendThrottleData();
  delay(10);

  sendInfoUpload6160();
  delay(10);

  sendInfoUpload6161();
  delay(10);

  sendHeartbeat();
  delay(100); // Send heartbeat
}

void sendCommandControl() 
{
  byte data[3];
  data[0] = 0x01; // Example command
  data[1] = 0x10; // Node ID
  data[2] = 0x00; // Reserved
  CAN0.sendMsgBuf(6144, 1, 3, data);
  Serial.println("Command Control sent");
}

void sendThrottleData() 
{
  byte data[7];
  data[0] = random(0, 256); // Throttle data 1 (low byte)
  data[1] = random(0, 256); // Throttle data 1 (high byte)
  data[2] = random(0, 256); // Throttle data 2 (low byte)
  data[3] = random(0, 256); // Throttle data 2 (high byte)
  data[4] = random(0, 256); // Throttle data 3 (low byte)
  data[5] = random(0, 256); // Throttle data 3 (high byte)
  data[6] = random(0, 256); // Throttle data 4 (14 bits in total)
  CAN0.sendMsgBuf(6152, 1, 7, data);
  Serial.println("Throttle Data sent");
}

void sendInfoUpload6160() 
{
  byte data[6];
  data[0] = random(0, 256); // Electrical speed (low byte)
  data[1] = random(0, 256); // Electrical speed (high byte)
  data[2] = random(0, 256); // Bus current (low byte)
  data[3] = random(0, 256); // Bus current (high byte)
  data[4] = random(0, 256); // Running status (low byte)
  data[5] = random(0, 256); // Running status (high byte)
  CAN0.sendMsgBuf(6160, 1, 6, data);
  Serial.println("Info Upload 6160 sent");
}

void sendInfoUpload6161() 
{
  byte data[7];
  data[0] = random(0, 256); // Output throttle (low byte)
  data[1] = random(0, 256); // Output throttle (high byte)
  data[2] = random(0, 256); // Bus voltage (low byte)
  data[3] = random(0, 256); // Bus voltage (high byte)
  data[4] = random(0, 256); // MOS temperature
  data[5] = random(0, 256); // Capacitance temperature
  data[6] = random(0, 256); // Motor temperature
  CAN0.sendMsgBuf(6161, 1, 7, data);
  Serial.println("Info Upload 6161 sent");
}

void sendHeartbeat() 
{
  byte data[6];
  unsigned long powerOnTime = millis() / 1000;
  data[0] = powerOnTime & 0xFF;
  data[1] = (powerOnTime >> 8) & 0xFF;
  data[2] = (powerOnTime >> 16) & 0xFF;
  data[3] = (powerOnTime >> 24) & 0xFF;
  data[4] = random(0, 4); // Node health status
  data[5] = random(0, 4); // Node current mode
  CAN0.sendMsgBuf(7509, 1, 6, data);
  Serial.println("Heartbeat sent");
}
