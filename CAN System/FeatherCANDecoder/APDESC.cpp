#include "APDESC.h"


APDESC::APDESC()
{
  telem_t telemdata; //APD ESC Telemetry format struct
  data_t printdata;  //APD ESC Serial and CAN Data print struct
}

APDESC::~APDESC()
{
}

APDESC::HandleSerialData(unsigned char * buffer, size_t buffersize)
{
  if(buffersize != 22) 
    {
      Serial.println("hello not 22");
      return; //Ignore malformed packets
    }

    if (buffer[20] != 255 || buffer[21] != 255) 
    {
      Serial.println("No Stop Byte Received");
        return; //Stop byte of 65535 not recieved
    }

    //Check the fletcher checksum
    int checkFletch = CheckFlectcher16(buffer);
    
    // checksum
    telemdata.CSUM_HI = buffer[19];
    telemdata.CSUM_LO = buffer[18];

    int checkCalc = (int)(((telemdata.CSUM_HI << 8) + telemdata.CSUM_LO));
/*
    //Checksums do not match
    if (checkFletch != checkCalc) 
    { 
      Serial.println("No CheckSum");
      return;
    }*/
    // Voltage
    telemdata.V_HI = buffer[1];
    telemdata.V_LO = buffer[0];

    float voltage = (float)((telemdata.V_HI << 8) + telemdata.V_LO);
    float currentVoltage = voltage / 100; //Voltage
    printdata.currentVoltage = currentVoltage;
    
    // Temperature
    telemdata.T_HI = buffer[3];
    telemdata.T_LO = buffer[2];

    float rawVal = (float)((telemdata.T_HI << 8) + telemdata.T_LO);

    int SERIESRESISTOR = 10000;
    int NOMINAL_RESISTANCE = 10000;
    int NOMINAL_TEMPERATURE = 25;
    int BCOEFFICIENT = 3455;

    //convert value to resistance
    float Rntc = (4096 / (float)rawVal) - 1;
    Rntc = SERIESRESISTOR / Rntc;

    // Get the temperature
    float temperature = Rntc / (float)NOMINAL_RESISTANCE;                           // (R/Ro)
    temperature = (float)log(temperature);                                     // ln(R/Ro)
    temperature /= BCOEFFICIENT;                                                    // 1/B * ln(R/Ro)

    temperature += (float)1.0 / ((float)NOMINAL_TEMPERATURE + (float)273.15);       // + (1/To)
    temperature = (float)1.0 / temperature;                                         // Invert
    temperature -= (float)273.15;                                                   // convert to Celcius

    // filter bad values
    if (temperature < 0 || temperature > 200)
    {
        temperature = 0;
    }

    temperature = (float)trunc(temperature * 100) / 100;                    // 2 decimal places
    float currentTemp = temperature; //Temperature
    printdata.currentTemp = currentTemp;

    // Current
    telemdata.I_HI = buffer[5];
    telemdata.I_LO = buffer[4];

    int currentAmpsInput = (int)((telemdata.I_HI << 8) + telemdata.I_LO);
    currentAmpsInput = (currentAmpsInput / 12.5); //Input current
    printdata.currentAmpsInput = currentAmpsInput;

    // Reservedz
    telemdata.R0_HI = buffer[7];
    telemdata.R0_LO = buffer[6];

    // eRPM
    telemdata.RPM0 = buffer[11];
    telemdata.RPM1 = buffer[10];
    telemdata.RPM2 = buffer[9];
    telemdata.RPM3 = buffer[8];
    
    int poleCount = 2; //2 poles by default, change as needed
    int currentERPM = (int)((telemdata.RPM0 << 24) + (telemdata.RPM1 << 16) + (telemdata.RPM2 << 8) + (telemdata.RPM3 << 0)); //ERPM output
    int currentRPM = currentERPM / poleCount; //Real RPM output
    printdata.currentRPM = currentRPM;

    // Input Duty
    telemdata.DUTYIN_HI = buffer[13];
    telemdata.DUTYIN_LO = buffer[12];

    int throttleDuty = (int)(((telemdata.DUTYIN_HI << 8) + telemdata.DUTYIN_LO)/10);
    int currentThrottle = (throttleDuty / 10); //Input throttle
    printdata.currentThrottle = currentThrottle;

    // Motor Duty
    telemdata.MOTORDUTY_HI = buffer[15];
    telemdata.MOTORDUTY_LO = buffer[14];

    int motorDuty = (int)(((telemdata.MOTORDUTY_HI << 8) + telemdata.MOTORDUTY_LO)/10);
    int currentMotorDuty = (motorDuty / 10); //Motor duty cycle
    printdata.currentMotorDuty = currentMotorDuty;

    // Reserved
    telemdata.R1 = buffer[17];

    int currentPowerInput = currentVoltage * currentAmpsInput; //Input power

    int currentPhase = currentAmpsInput / currentMotorDuty; //Phase current
    /* 
    Status Flags
    # Bit position in byte indicates flag set, 1 is set, 0 is default
    # Bit 0: Motor Started, set when motor is running as expected
    # Bit 1: Motor Saturation Event, set when saturation detected and power is reduced for desync protection
    # Bit 2: ESC Over temperature event occuring, shut down method as per configuration
    # Bit 3: ESC Overvoltage event occuring, shut down method as per configuration
    # Bit 4: ESC Undervoltage event occuring, shut down method as per configuration
    # Bit 5: Startup error detected, motor stall detected upon trying to start
    */
    telemdata.statusFlag = buffer[16];
    printdata.currentStatus = telemdata.statusFlag;

    PrintDataTable(printdata);
}

APDESC::CheckFlectcher16(unsigned char * buffer) 
{
  int fCCRC16;
  int i;
  int c0 = 0;
  int c1 = 0;

  // Calculate checksum intermediate bytesUInt16
  for (i = 0; i < 18; i++) //Check only first 18 bytes, skip crc bytes
  {
      c0 = (int)(c0 + ((int)buffer[i])) % 255;
      c1 = (int)(c1 + c0) % 255;
  }
  // Assemble the 16-bit checksum value
  fCCRC16 = ( c1 << 8 ) | c0;
  return (int)fCCRC16;
}

APDESC::PrintDataTable(data_t printdata)
{
  Serial.print("currentstatus : \t");
  Serial.print(printdata.currentStatus);
  Serial.print("\t currentVoltage : \t");
  Serial.print(printdata.currentVoltage);
  Serial.print("\t currentAmpsInput : \t");
  Serial.print(printdata.currentAmpsInput);
  Serial.print("\t currentMotorDuty : \t");
  Serial.print(printdata.currentMotorDuty);
  Serial.print("\t currentRPM : \t");
  Serial.print(printdata.currentRPM);
  Serial.print("\t currentThrottle : \t");
  Serial.print(printdata.currentThrottle);
  Serial.print("\t currentTemp : \t");
  Serial.println(printdata.currentTemp);
}

/*
APDESC::apd_esc_telem_update()
{
    for(uint8_t i = 0; i < ARRAY_SIZE(apd_esc_telem); i++)  // check number of escs
    {
        if (apd_esc_telem[i] == nullptr)  // if non continue
        {
            continue;
        }
        ESC_APD_Telem &esc = *apd_esc_telem[i]; // initialise esc one by one

        if (esc.update()) // read esc uart
        {
            const ESC_APD_Telem::telem &t = esc.get_telem(); // return uart telemetry data

            uavcan_equipment_esc_Status pkt {}; // can packet
            static_assert(APD_ESC_INSTANCES <= ARRAY_SIZE(g.esc_number), "There must be an ESC instance number for each APD ESC"); // check numbers esc match esc expected number
            
            pkt.esc_index = g.esc_number[i];
            pkt.voltage = t.voltage;
            pkt.current = t.current;
            pkt.temperature = t.temperature;
            pkt.rpm = t.rpm;
            pkt.power_rating_pct = t.power_rating_pct;
            pkt.error_count = t.error_count;

            uint8_t buffer[UAVCAN_EQUIPMENT_ESC_STATUS_MAX_SIZE] {}; // data buffer to send
            uint16_t total_size = uavcan_equipment_esc_Status_encode(&pkt, buffer, !canfdout()); // canfdout = bool
            canard_broadcast(UAVCAN_EQUIPMENT_ESC_STATUS_SIGNATURE,UAVCAN_EQUIPMENT_ESC_STATUS_ID,CANARD_TRANSFER_PRIORITY_LOW,&buffer[0],total_size);
        }
    }
}

APDESC::canard_broadcast(uint64_t data_type_signature,uint16_t data_type_id,uint8_t priority,const void* payload,uint16_t payload_len)
{
    if (canardGetLocalNodeID(&dronecan.canard) == CANARD_BROADCAST_NODE_ID) 
    {
        return false;
    }

    uint8_t *tid_ptr = get_tid_ptr(MAKE_TRANSFER_DESCRIPTOR(data_type_signature, data_type_id, 0, CANARD_BROADCAST_NODE_ID));
    if (tid_ptr == nullptr) 
    {
        return false;
    }

    const int16_t res = canardBroadcast(&dronecan.canard,data_type_signature,data_type_id,tid_ptr,priority,payload,payload_len
#if CANARD_MULTI_IFACE
                    , IFACE_ALL // send over all ifaces
#endif
#if HAL_CANFD_SUPPORTED
                    , canfdout()
#endif
                    );

#if DEBUG_PKTS
    if (res < 0) 
    {
        can_printf("Tx error %d\n", res);
    }
#endif
#if HAL_ENABLE_SENDING_STATS
    if (res <= 0) 
    {
        protocol_stats.tx_errors++;
    } 
    else 
    {
        protocol_stats.tx_frames += res;
    }
#endif
    return res > 0;
}*/