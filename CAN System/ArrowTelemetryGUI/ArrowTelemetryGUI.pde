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

// Serial Read Variables
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
    
  myPort = new Serial(this,Serial.list()[0], 115200); // Instantiate Serial class Serial.list()[0]
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
    
    float datain[] = new float[dataArray.length];
    
    if((dataArray.length == 14) & (Flag == true))
    {
      for (int i = 0; i < dataArray.length; i++)
      {
          datain[i] = float(dataArray[i]);
      }
      plot.addPoint(t1,datain[3]);
      Voltage.setText(str(datain[3]));
      t1++;
      plot1.addPoint(t2,datain[5]);
      Current.setText(str(datain[5]));
      t2++;
      plot2.addPoint(t3,datain[9]);
      RPM.setText(str(datain[9]));
      t3++;
      plot3.addPoint(t4,datain[11]);
      Throttle.setText(str(datain[11]));
      t4++;
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
  
  myPort.stop();
  myPort.clear();
  myPort = new Serial(this,Serial.list()[0], 115200);
  
  background(50); // Reset background
 
  setupPlot(plot ,200,0 ,200,100,"Voltage"); // call encoder plot setup function
  setupPlot(plot1,200,270,200,100,"Current"); // call encoder plot setup function
  setupPlot(plot2,200,540,200,100,"RPM"); // call encoder plot setup function
  setupPlot(plot3,200,810,200,100,"Throttle"); // call encoder plot setup function
}
public void Close() // close program, disble motors, stop encoder read
{
  Flag = false;
  exit();
}
