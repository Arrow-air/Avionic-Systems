// Import Class Libraries
import controlP5.*;          //Import: UI Library
import grafica.*;            // Graphing Library
import processing.serial.*;  // Serial Library
import java.nio.charset.StandardCharsets; // Parsing Library

// Initialise Classes
ControlP5 cp5;    // GUI Initialise
Canvas guiIntro, cardSetup, cardMotion, cardIO;    // GUI Tabs Initialise
GPlot plot, plot1, plot2, plot3;    // Encoder Plot Initialise
RadioButton Inputs,Outputs;    // Digital Input Indicators
Serial myPort;    // Serial Port Initialise

Textlabel Voltage, Current, RPM, Throttle;    // Serial Port Output

// Setup Tab Variables
PImage img, img2;

// Motion Tab Variables
int t1 = 0,t2 = 0,t3 = 0,t4 = 0;
float val =  0, val1 = 0,val2 = 0,val3 = 0,val4 = 0;

// IO Variables
int input;
int inputState = 0;

// Serial Read Variables
char[] cmd = new char[2];
String dataArray[];
String dataString = "";

// Control Flag
boolean Flag = false;

void setup() 
{
  size(1800, 1200);      // Window Size in Pixels
  background(50);      // Off-white baground colour
  frameRate(10000); // set frame rate
  smooth();
  
  if (surface != null) 
  {
    surface.setTitle("Arrow ESC Telemetry GUI");
    surface.setResizable(false);
  }
  
  img = loadImage("singer-instruments.png"); // Singer's logo
  PFont font = createFont("helvetica",height/35);          // Display fonts
   
  plot = new GPlot(this);
  plot1 = new GPlot(this);
  plot2 = new GPlot(this);
  plot3 = new GPlot(this);
  
  cp5 = new ControlP5(this);  // Instantiate UI class 
  //cp5.printPublicMethodsFor(ControlP5.class);
  
  cp5.addButton("Start").setPosition(10,18).setSize(width/12,height/18)
       .setFont(font).setOff().setColorBackground((color(255,0,255)));
    
  cp5.addButton("Reset").setPosition(1250,18).setSize(width/12,height/18)
     .setFont(font).setOff().setColorBackground((color(255,0,255)));
     
  cp5.addButton("Close").setPosition(1480,18).setSize(width/12,height/18) // Create Shutdown Button.
     .setFont(font).setOff().setColorBackground((color(255,0,255)));
     
  setupPlot(plot ,200,0 ,200,100,"Voltage"); // call encoder plot setup function
  Voltage = cp5.addTextlabel("Voltage").setFont(font).setPosition(1000,10)
     .setSize(width/4,height/16).setColor(color(255,0,0)).setText("0.0");            // Create output Lable to display serial data on screen
     
  setupPlot(plot1,200,270,200,100,"Current"); // call encoder plot setup function
   Current = cp5.addTextlabel("Current").setFont(font).setPosition(1000,280)
     .setSize(width/4,height/16).setColor(color(255,0,0)).setText("0.0");            // Create output Lable to display serial data on screen
     
  setupPlot(plot2,200,540,200,100,"RPM"); // call encoder plot setup function
  RPM = cp5.addTextlabel("RPM").setFont(font).setPosition(1000,550)
     .setSize(width/4,height/16).setColor(color(255,0,0)).setText("0.0");            // Create output Lable to display serial data on screen
  
  setupPlot(plot3,200,810,200,100,"Throttle"); // call encoder plot setup function
  Throttle = cp5.addTextlabel("Throttle").setFont(font).setPosition(1000,820)
     .setSize(width/4,height/16).setColor(color(255,0,0)).setText("0.0");            // Create output Lable to display serial data on screen
   
  
   img = loadImage("vtol_moving_2.gif"); 
   img2 = loadImage("PT2C.png");
   
    image(img, 10, 150, img.width/2.5, img.height/2.5); // display logo
    image(img2, 1250, 300, img.width/2.5, img.height/2.5); // display logo
    
  myPort = new Serial(this,Serial.list()[0], 115200); // Instantiate Serial class
}

void draw() 
{ 
  background(50); // Reset background
  
  image(img, 10, 150, img.width/2.5, img.height/2.5); // display logo
  image(img2, 1250, 300, img2.width/2.5, img2.height/2.5); // display logo
  
  runPlot(plot ,width*1.5/3,height*0.5/3);    // Draws X-Axis encoder reading on graph
  runPlot(plot1,width*1.5/3,height*0.5/3);    // Draws Y-Axis encoder reading on graph
  runPlot(plot2,width*1.5/3,height*0.5/3);    // Draws Z-Axis encoder reading on graph
  runPlot(plot3,width*1.5/3,height*0.5/3);    // Draws Z-Axis encoder reading on graph
  
  // Parse Motor Card serial comms to extract encoder reading if button clicked and plot values
  if (myPort.available() > 0)
  {
    // read entire serial output line as a massive string
    dataString = new String(myPort.readBytes(),StandardCharsets.UTF_8).replaceAll("\r","").replaceAll("\n","");
    
    dataArray = dataString.split(","); // convert massive string into individual strings
    
    if (dataArray[0].charAt(0) == '1' || dataArray[0].charAt(0) == '3') // If MOTOR CARD, Read Encoder Inputs
    {
      if(dataArray.length == 7 && Flag == true ) // filter serial outputs by their fixed length
      {
        if(dataArray[3].charAt(0) == '0') // filter serial outputs by their fixed length
        {
          encoderPlot(plot,Voltage,dataString,dataArray,t1,val1);
          t1++;
        }
        if(dataArray[3].charAt(0) == '1') // filter serial outputs by their fixed length
        {
          encoderPlot(plot1,Current,dataString,dataArray,t2,val2);
          t2++;
        }
        if(dataArray[3].charAt(0) == '2') // filter serial outputs by their fixed length
        {
          encoderPlot(plot2,RPM,dataString,dataArray,t3,val3);
          t3++;
        }
        if(dataArray[3].charAt(0) == '4') // filter serial outputs by their fixed length
        {
          encoderPlot(plot3,Throttle,dataString,dataArray,t4,val4);
          t4++;
        }
      }
    }
  }
}

public void controlEvent(ControlEvent theEvent) // Event Handler for UI Inputs
{
  println(theEvent.getController().getName());
}


// Motion Functions
public void Start() 
{
   Flag = true;
}

public void encoderPlot(GPlot plotn,Textlabel label,String dataString,String[] dataArray,int t,float val) // Setup Axes
{
  for(int j = 0 ; j < dataArray[1].length(); j++ )// Read the command characters
  {
    cmd[j] = dataArray[1].charAt(j);
  }
  if((cmd[0] == 'E') && (cmd[1] == 'P'))
  {
    if (!Float.isNaN(float(dataArray[4])))
    {
      label.setText(dataString);
      val = float(dataArray[4]);
      plotn.addPoint(t,val);
    }
  }
}

public void setupPlot(GPlot plotn,float posx,float posy,float dimx,float dimy, String Title) // Setup Axes
{ 
  plotn.setPos(posx, posy);
  plotn.setDim(dimx,dimy);
  plotn.setTitleText(Title);
  plotn.getXAxis().setAxisLabelText("Time");
  plotn.getYAxis().setAxisLabelText("Amplitude");
  plotn.drawBackground();
  plotn.drawGridLines(GPlot.BOTH);
  plotn.getMainLayer().setLineColor(color(255, 5, 5));
  plotn.activatePanning();
}

public void runPlot(GPlot plotn,float dimx,float dimy) // Setup Axes
{
  plotn.beginDraw();
  plotn.setDim(dimx,dimy);
  plotn.drawBackground();
  plotn.drawBox();
  plotn.drawXAxis();
  plotn.drawYAxis();
  plotn.drawGridLines(GPlot.BOTH); // Draws encoder reading on graph
  plotn.drawLines();
  plotn.drawLabels();
  plotn.drawTitle();
  plotn.endDraw();
}

// Program Functions
public void Reset() 
{
  Flag = false;
  
  Voltage.setText("0.0");
  Current.setText("0.0");
  RPM.setText("0.0");
  Throttle.setText("0.0");
  
  t1 = 0;t2 = 1;t3 = 0;t4 = 0;
  
  val1 = 0;val2 = 0;val3 = 0;val4 = 0;
  
  myPort.stop();
  myPort.clear();
  myPort = new Serial(this,Serial.list()[0], 115200);
  
  background(190);
 
  setupPlot(plot ,550, height/12               ,width*1.5/3,height*0.5/3,"X - Axis"); // call encoder plot setup function
  setupPlot(plot1,550, height/12 + height*0.9/3,width*1.5/3,height*0.5/3,"Y - Axis"); // call encoder plot setup function
  setupPlot(plot2,550, height/12 + height*1.8/3,width*1.5/3,height*0.5/3,"Z - Axis"); // call encoder plot setup function 
  setupPlot(plot3,550, height/12 + height*1.8/3,width*1.5/3,height*0.5/3,"Z - Axis"); // call encoder plot setup function 
}
public void Close() // close program, disble motors, stop encoder read
{
  Flag = false;
  exit();
}
