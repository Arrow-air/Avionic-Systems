#include <Servo.h>
#include "HX711.h"
#include "APDESC.h"

////////////////////// PPM CONFIGURATION//////////////////////////
#define channel_number 6  //set the number of channels
#define sigPin 2  //set PPM signal output pin on the arduino
#define PPM_FrLen 27000  //set the PPM frame length in microseconds (1ms = 1000µs)
#define PPM_PulseLen 400  //set the pulse length
//////////////////////////////////////////////////////////////////

const int LOADCELL_DOUT_PIN = {3,4,5,6,7,8};
const int LOADCELL_SCK_PIN = {9,10,11,12,13,14};

APDESC ESC;
HX711 Thrust[4], Torque[2];
Servo Motor;

int ppm[channel_number];

char a;
int c[25];
int n = 0;
int P,R,T,Y;

struct JoystickData 
{
  byte ButtonsA;
  byte ButtonsB;
  byte Throttle;
  byte Yaw;
  byte Roll;
  byte Pitch;
};

JoystickData data;

void setup()
{
  setupPPM();
  myServo.attach(16);
  
  for(int i = 0; i < 3; i++)
  {
    Thrust[i].begin(LOADCELL_DOUT_PIN[i], LOADCELL_SCK_PIN[i]);
  }
  for(int i = 4; i < 6; i++)
  {
    Torque[i - 4].begin(LOADCELL_DOUT_PIN[i], LOADCELL_SCK_PIN[i]);
  }
  Serial.begin(115200);
  Serial1.begin(115200);
  resetData();
}

void loop()
{
  if(Serial.available())
  {
     a = Serial.read();
     c[n] = (int) a - 48;
     n++;
        
     if (a == '>')
     {
        n = 0;

        T = c[1]*100;
        T += c[2]*10;
        T += c[3]*1;
        data.Throttle = map(T,100,355,0,255);

        R = c[5]*100;
        R += c[6]*10;
        R += c[7]*1;
        data.Roll = map(R,100,355,0,255);
          
        P = c[9]*100;
        P += c[10]*10;
        P += c[11]*1;
        data.Pitch = map(P,100,355,0,255);
        
        Y = c[13]*100;
        Y += c[14]*10;
        Y += c[15]*1;
        data.Yaw = map(Y,100,355,0,255);

        data.ButtonsA = c[17]*100;
        data.ButtonsA += c[18]*10;
        data.ButtonsA += c[19]*1;
          
        data.ButtonsB = c[21]*100;
        data.ButtonsB += c[22]*10;
        data.ButtonsB += c[23]*1;

        setPPMValuesFromData();
      }
   }
}

/**************************************************/

void resetData() 
{
  data.Throttle = 128;
  data.Roll = 128;
  data.Pitch = 128;
  data.Yaw = 128;
  data.ButtonsA = 0;
  data.ButtonsB = 0;
  setPPMValuesFromData();
}

void setPPMValuesFromData()
{
  ppm[0] = map(data.Throttle, 0, 255, 1000, 2000);
  ppm[1] = map(data.Yaw, 0, 255, 1000, 2000);
  ppm[2] = map(data.Pitch, 0, 255, 1000, 2000);
  ppm[3] = map(data.Roll, 0, 255, 1000, 2000);  
  ppm[4] = map(data.ButtonsA, 0, 12, 1000, 2000);
  ppm[5] = map(data.ButtonsB, 0, 12, 1000, 2000);
}

void setupPPM()
{
  pinMode(sigPin, OUTPUT);
  digitalWrite(sigPin, 0);  //set the PPM signal pin to the default state (off)

  cli();
  TCCR1A = 0; // set entire TCCR1 register to 0
  TCCR1B = 0;

  OCR1A = 100;  // compare match register (not very important, sets the timeout for the first interrupt)
  TCCR1B |= (1 << WGM12);  // turn on CTC mode
  TCCR1B |= (1 << CS11);  // 8 prescaler: 0,5 microseconds at 16mhz
  TIMSK1 |= (1 << OCIE1A); // enable timer compare interrupt
  sei();
}

//#error This line is here to intentionally cause a compile error. Please make sure you set clockMultiplier below as appropriate, then delete this line.
#define clockMultiplier 2 // set this to 2 if you are using a 16MHz arduino, leave as 1 for an 8MHz arduino

ISR(TIMER1_COMPA_vect)
{
  static boolean state = true;

  TCNT1 = 0;

  if ( state ) 
  {
    //end pulse
    PORTD = PORTD & ~B00000100; // turn pin 2 off. Could also use: digitalWrite(sigPin,0)
    OCR1A = PPM_PulseLen * clockMultiplier;
    state = false;
  }
  else 
  {
    //start pulse
    static byte cur_chan_numb;
    static unsigned int calc_rest;

    PORTD = PORTD | B00000100; // turn pin 2 on. Could also use: digitalWrite(sigPin,1)
    state = true;

    if(cur_chan_numb >= channel_number) 
    {
      cur_chan_numb = 0;
      calc_rest += PPM_PulseLen;
      OCR1A = (PPM_FrLen - calc_rest) * clockMultiplier;
      calc_rest = 0;
    }
    else 
    {
      OCR1A = (ppm[cur_chan_numb] - PPM_PulseLen) * clockMultiplier;
      calc_rest += ppm[cur_chan_numb];
      cur_chan_numb++;
    }     
  }
}
