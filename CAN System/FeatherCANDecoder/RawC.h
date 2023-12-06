/**
 * Telemetry Read Example for UART HV Pro Units v2.0
 * 21st Sept 2021
 * Vanja Videnovic
 * Tony Bazouni
 * [SEC=UNCLASSIFIED]
 */
/*
telem_t telemdata; //Telemetry format struct
*/
/*Data buffer format
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
21: Stop Byte High*/
/*

void HandleSerialData(int buffer[]) {
    if(sizeof(buffer) != 22) {
        return; //Ignore malformed packets
    }

    if (buffer[20] != 255 || buffer[21] != 255) {
        return; //Stop byte of 65535 not recieved
    }

    //Check the fletcher checksum
    int checkFletch = CheckFlectcher16(buffer);
    
    // checksum
    telemdata.CSUM_HI = buffer[19];
    telemdata.CSUM_LO = buffer[18];

    int checkCalc = (int)(((telemdata.CSUM_HI << 8) + telemdata.CSUM_LO));
    
    //Checksums do not match
    if (checkFletch != checkCalc) {
        return;
    }
    // Voltage
    telemdata.V_HI = buffer[1];
    telemdata.V_LO = buffer[0];

    float voltage = (float)((telemdata.V_HI << 8) + telemdata.V_LO);
    float currentVoltage = voltage / 100; //Voltage


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
    if (temperature < 0 || temperature > 200){
        temperature = 0;
    }

    temperature = (float)trunc(temperature * 100) / 100;                    // 2 decimal places
    float currentTemp = temperature; //Temperature

    // Current
    telemdata.I_HI = buffer[5];
    telemdata.I_LO = buffer[4];

    int currentAmpsInput = (int)((telemdata.I_HI << 8) + telemdata.I_LO);
    currentAmpsInput = (currentAmpsInput / 12.5); //Input current

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

    // Input Duty
    telemdata.DUTYIN_HI = buffer[13];
    telemdata.DUTYIN_LO = buffer[12];

    int throttleDuty = (int)(((telemdata.DUTYIN_HI << 8) + telemdata.DUTYIN_LO)/10);
    int currentThrottle = (throttleDuty / 10); //Input throttle

    // Motor Duty
    telemdata.MOTORDUTY_HI = buffer[15];
    telemdata.MOTORDUTY_LO = buffer[14];

    int motorDuty = (int)(((telemdata.MOTORDUTY_HI << 8) + telemdata.MOTORDUTY_LO)/10);
    int currentMotorDuty = (motorDuty / 10); //Motor duty cycle

    // Reserved
    telemdata.R1 = buffer[17];

    int currentPowerInput = currentVoltage * currentAmpsInput; //Input power

    int currentPhase = currentAmpsInput / currentMotorDuty; //Phase current

    /* Status Flags
    # Bit position in byte indicates flag set, 1 is set, 0 is default
    # Bit 0: Motor Started, set when motor is running as expected
    # Bit 1: Motor Saturation Event, set when saturation detected and power is reduced for desync protection
    # Bit 2: ESC Over temperature event occuring, shut down method as per configuration
    # Bit 3: ESC Overvoltage event occuring, shut down method as per configuration
    # Bit 4: ESC Undervoltage event occuring, shut down method as per configuration
    # Bit 5: Startup error detected, motor stall detected upon trying to start*/
    //telemdata.statusFlag = buffer[16];
//}
/*
int CheckFlectcher16(int byteBuffer[]) {
    int fCCRC16;
    int i;
    int c0 = 0;
    int c1 = 0;

    // Calculate checksum intermediate bytesUInt16
    for (i = 0; i < 18; i++) //Check only first 18 bytes, skip crc bytes
    {
        c0 = (int)(c0 + ((int)byteBuffer[i])) % 255;
        c1 = (int)(c1 + c0) % 255;
    }
    // Assemble the 16-bit checksum value
    fCCRC16 = ( c1 << 8 ) | c0;
    return (int)fCCRC16;
}

typedef struct  {
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
} telem_t;*/