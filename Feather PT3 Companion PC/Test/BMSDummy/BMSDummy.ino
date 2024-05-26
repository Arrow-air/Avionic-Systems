#include <SPI.h>
#include "mcp_can.h"

// Define the CS pin for the CAN module
#define CAN0_CS 17

// Define dummy data for different commands
unsigned long txId;
unsigned char len = 8;
constexpr uint16_t commands[8] = {0x2B1A, 0x260A, 0x271A, 0x280A, 0x291A, 0x2A7A, 0x2D1A, 0x2C1A};
//constexpr byte commands[8] = {11034, 9738, 10010, 10250, 10522, 10874, 11546, 11290};

// Instantiate the CAN object
MCP_CAN CAN0(CAN0_CS);

void setup() 
{
  // Start serial communication
  Serial.begin(115200);

  delay(5000);

  while (!Serial) 
  {
    ;  // wait for serial port to connect. Used in Testing to start routing on opening serial monitor for debug
  }

  // Initialize CAN bus at 500 kbps
  if (CAN0.begin(MCP_STDEXT, CAN_500KBPS, MCP_8MHZ) == CAN_OK) 
  {
    Serial.println("CAN BUS Shield initialized successfully!");
  } 
  else 
  {
    Serial.println("CAN BUS Shield initialization failed...");
    while (1);
  }

  // Set the CAN filter and mask to allow all messages
  CAN0.init_Mask(0, 0, 0x00000000);  // Initialize mask 0
  CAN0.init_Mask(1, 0, 0x00000000);  // Initialize mask 1
  CAN0.init_Filt(0, 0, 0x00000000);  // Initialize filter 0
  CAN0.init_Filt(1, 0, 0x00000000);  // Initialize filter 1
  CAN0.init_Filt(2, 0, 0x00000000);  // Initialize filter 2
  CAN0.init_Filt(3, 0, 0x00000000);  // Initialize filter 3
  CAN0.init_Filt(4, 0, 0x00000000);  // Initialize filter 4
  CAN0.init_Filt(5, 0, 0x00000000);  // Initialize filter 5

  // Set operation mode to normal mode
  CAN0.setMode(MCP_NORMAL);
}

void loop() 
{
  static unsigned long lastSent = 0;

  unsigned long now = millis();
  
  if (now - lastSent >= 1000) 
  { // Send data every second
    for (unsigned char unit_id = 10; unit_id < 16; ++unit_id) 
    {  // Loop through each unit
      for (unsigned char i = 0; i < sizeof(commands); ++i) 
      {
        setCommandData(commands[i], unit_id);
        delay(1000); // Small delay between commands
      }
    }
    lastSent = now;
  }
}

// Function to calculate CAN ID
unsigned long calculateCanId(unsigned char controller_id, byte command) 
{
  uint32_t CAN_ID = (0 << 26) | (((command >> 8) & 0xFF) << 8) | controller_id;
  return CAN_ID;
}

// Function to send CAN frame
void sendDummyData(unsigned long id, unsigned char len, unsigned char *data) 
{
  if (CAN0.sendMsgBuf(id, 1, sizeof(data), data) == CAN_OK) 
  {
    //Serial.print(id);
    Serial.print("\t");
    Serial.print(len);
    Serial.print("\t");
    for(int i = 0; i < sizeof(data); i++)
    {
      Serial.print(data[i]);
      Serial.print("\t");
    }
    
    Serial.println("Message Sent Successfully!");
  } 
  else 
  {
    //Serial.print(id);
    Serial.print("\t");
    Serial.print(len);
    Serial.print("\t");
    for(int i = 0; i < sizeof(data); i++)
    {
      Serial.print(data[i]);
      Serial.print("\t");
    }
    Serial.println("Error Sending Message...");
  }
}

// Function to set data for different commands for a specific unit
void setCommandData(unsigned char command, unsigned char unit_id) 
{
  txId = calculateCanId(unit_id, command);
  Serial.print(command);

  unsigned char data[8];

  switch (command) 
  {
    case commands[0]: // CAN_PACKET_BMS_TEMPS
      len = 8;
      data[0] = 0; data[1] = 24;  // NoOfCells
      data[2] = 0x12; data[3] = 0x34;  // auxVoltagesIndividual1
      data[4] = 0x56; data[5] = 0x78;  // auxVoltagesIndividual2
      data[6] = 0x9A; data[7] = 0xBC;  // auxVoltagesIndividual3
      break;

    case commands[1]: // CAN_PACKET_BMS_V_TOT
      len = 8;
      int32_t packVoltage = 42000;  // 42.0V
      int32_t chargerVoltage = 50000;  // 50.0V
      memcpy(data, &packVoltage, 4);
      memcpy(data + 4, &chargerVoltage, 4);
      break;

    case commands[2]: // CAN_PACKET_BMS_I
      len = 8;
      int32_t packCurrent1 = 1000;  // 10.0A
      int32_t packCurrent2 = 2000;  // 20.0A
      memcpy(data, &packCurrent1, 4);
      memcpy(data + 4, &packCurrent2, 4);
      break;

    case commands[3]: // CAN_PACKET_BMS_AH_WH
      len = 8;
      int32_t Ah_Counter = 500;  // 0.5 Ah
      int32_t Wh_Counter = 1000;  // 1.0 Wh
      memcpy(data, &Ah_Counter, 4);
      memcpy(data + 4, &Wh_Counter, 4);
      break;

    case commands[4]: // CAN_PACKET_BMS_V_CELL
      len = 8;
      data[0] = 24;  // cellPoint
      data[1] = 24;  // NoOfCells
      data[2] = 0x12; data[3] = 0x34;  // cellVoltage10
      data[4] = 0x56; data[5] = 0x78;  // cellVoltage11
      data[6] = 0x9A; data[7] = 0xBC;  // cellVoltage12
      break;

    case commands[5]: // CAN_PACKET_BMS_BAL
      len = 8;
      data[0] = NULL;  // NoOfCells
      uint64_t bal_state = 0x123456789ABCDEF0;
      memcpy(data + 1, &bal_state, 7);
      break;

    case commands[6]: // CAN_PACKET_BMS_SOC_SOH_TEMP_STAT
      len = 8;
      int16_t cellVoltageLow = 3000;  // 3.0V
      int16_t cellVoltageHigh = 4200;  // 4.2V
      data[0] = (cellVoltageLow >> 8) & 0xFF; data[1] = cellVoltageLow & 0xFF;
      data[2] = (cellVoltageHigh >> 8) & 0xFF; data[3] = cellVoltageHigh & 0xFF;
      data[4] = 80;  // SOC 80%
      data[5] = 90;  // SOH 90%
      data[6] = 30;  // tBattHi 30°C
      data[7] = 0;  // BitF
      break;

    case commands[7]: // CAN_PACKET_BMS_HUM
      len = 6;
      int16_t CAN_PACKET_BMS_TEMP0 = 2500;  // 25.0°C
      int16_t CAN_PACKET_BMS_HUM_HUM = 5000;  // 50.0%
      int16_t CAN_PACKET_BMS_HUM_TEMP1 = 2600;  // 26.0°C
      memcpy(data, &CAN_PACKET_BMS_TEMP0, 2);
      memcpy(data + 2, &CAN_PACKET_BMS_HUM_HUM, 2);
      memcpy(data + 4, &CAN_PACKET_BMS_HUM_TEMP1, 2);
      break;

    default:
      Serial.println("Unknown Command");
      return;
  }
  sendDummyData(txId, len, data);
}
