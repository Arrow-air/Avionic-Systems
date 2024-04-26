// Import Class Libraries
import controlP5.*;          //Import: UI Library
import grafica.*;            // Graphing Library
import processing.serial.*;  // Serial Library
import java.nio.charset.StandardCharsets; // Parsing Library

// Initialise Classes
ControlP5 cp5;    // GUI Initialise
Canvas guiIntro, cardSetup, cardMotion, cardIO;    // GUI Tabs Initialise
GPlot plot, plot1, plot2, plot3, plot4, plot5;    // Encoder Plot Initialise
RadioButton Inputs,Outputs;    // Digital Input Indicators
Serial myPort;    // Serial Port Initialise

Textlabel Voltage, Current, RPM, Throttle, Thrust, Torque;    // Serial Port Output

// Setup Tab Variables
PImage img, img2, img3, img4;

// Motion Tab Variables
int t1 = 0,t2 = 0,t3 = 0,t4 = 0,t5 = 0,t6 = 0;
int Manual = 0;

// Serial Read Variables
String dataArray[];
String dataString = "";
float datain[];

// Control Flag
boolean Flag = false;

void setup() 
{
  size(1916, 1200);      // Window Size in Pixels
  background(50);      // Off-white baground colour
  frameRate(10000); // set frame rate
  smooth();
  
  if (surface != null) 
  {
    surface.setTitle("MOTOR TEST SYSTEM");
    surface.setResizable(false);
  }
  
  PFont font = createFont("helvetica",height/50);          // Display fonts
  
  plot = new GPlot(this);
  plot1 = new GPlot(this);
  plot2 = new GPlot(this);
  plot3 = new GPlot(this);
  plot4 = new GPlot(this);
  plot5 = new GPlot(this);
  
  cp5 = new ControlP5(this);  // Instantiate UI class 
  //cp5.printPublicMethodsFor(ControlP5.class);
  
  cp5.addButton("Start").setPosition(10,298).setSize(width/14,height/18)
       .setFont(font).setOff().setColorBackground((color(255,0,255)));
  
   cp5.addButton("Reset").setPosition(10,368).setSize(width/14,height/18)
     .setFont(font).setOff().setColorBackground((color(255,0,255)));
  
  cp5.addButton("Close").setPosition(10,438).setSize(width/14,height/18) // Create Shutdown Button.
     .setFont(font).setOff().setColorBackground((color(255,0,255)));
     
  
  cp5.addButton("Step").setPosition(460,900).setSize(width/14,height/18) // Create Shutdown Button.
     .setFont(font).setOff().setColorBackground((color(255,0,255)));
  
  cp5.addButton("Routine").setPosition(960,900).setSize(width/14,height/18) // Create Shutdown Button.
     .setFont(font).setOff().setColorBackground((color(255,0,255)));
  
  cp5.addSlider("Manual").setPosition(165,980).setSize(300,50).setRange(0,100)
     .setValue(0).setBroadcast(true).setFont(font).setColorBackground((color(255,0,255)));
     
  setupPlot(plot ,165,5  ,200,100,"Voltage"); // call encoder plot setup function
  Voltage = cp5.addTextlabel("Voltage").setFont(font).setPosition(850,10)
     .setSize(width/4,height/16).setColor(color(255,0,0)).setText("0.0");            // Create output Lable to display serial data on screen
     
  setupPlot(plot1,165,255,200,100,"Current"); // call encoder plot setup function
  Current = cp5.addTextlabel("Current").setFont(font).setPosition(850,260)
     .setSize(width/4,height/16).setColor(color(255,0,0)).setText("0.0");            // Create output Lable to display serial data on screen
     
  setupPlot(plot2,165,505,200,100,"RPM"); // call encoder plot setup function
  RPM = cp5.addTextlabel("RPM").setFont(font).setPosition(850,510)
     .setSize(width/4,height/16).setColor(color(255,0,0)).setText("0.0");            // Create output Lable to display serial data on screen
     
  setupPlot(plot3,1000,5,200,100,"Throttle"); // call encoder plot setup function
  Throttle = cp5.addTextlabel("Throttle").setFont(font).setPosition(1700,10)
     .setSize(width/4,height/16).setColor(color(255,0,0)).setText("0.0");            // Create output Lable to display serial data on screen
  
  setupPlot(plot4,1000,255,200,100,"Thrust"); // call encoder plot setup function
  Thrust = cp5.addTextlabel("Thrust").setFont(font).setPosition(1700,260)
     .setSize(width/4,height/16).setColor(color(255,0,0)).setText("0.0");            // Create output Lable to display serial data on screen
  
  setupPlot(plot5,1000,505,200,100,"Torque"); // call encoder plot setup function
  Torque = cp5.addTextlabel("Torque").setFont(font).setPosition(1700,510)
     .setSize(width/4,height/16).setColor(color(255,0,0)).setText("0.0");            // Create output Lable to display serial data on screen
     
  img = loadImage("vtol_moving_2.gif"); 
  img2 = loadImage("ThrustStand.png");
  img3 = loadImage("StepResponse.png"); 
  img4 = loadImage("MultiStepResponse.png");
  
  image(img, 10, 10, img.width/2.5, img.height/2.5); // display logo
  image(img2, 1560, 830, img2.width/5, img2.height/5); // display logo
  image(img3, 600, 830, img2.width/5, img2.height/5); // display logo
  image(img4, 1100, 830, img2.width/5, img2.height/5); // display logo
  
  myPort = new Serial(this,Serial.list()[0], 115200); // Instantiate Serial class Serial.list()[0]
}

void draw() 
{ 
  background(50); // Reset background
  
  image(img, 10, 10, img.width/2.5, img.height/2.5); // display logo
  image(img2, 1560, 830, img2.width/5, img2.height/5); // display logo
  image(img3, 600, 830, img2.width/5, img2.height/5); // display logo
  image(img4, 1100, 830, img2.width/5, img2.height/5); // display logo
  
  runPlot(plot ,width*1.5/4.2,height*0.5/4.2);    // Draws X-Axis encoder reading on graph
  runPlot(plot1,width*1.5/4.2,height*0.5/4.2);    // Draws Y-Axis encoder reading on graph
  runPlot(plot2,width*1.5/4.2,height*0.5/4.2);    // Draws Z-Axis encoder reading on graph
  runPlot(plot3,width*1.5/4.2,height*0.5/4.2);    // Draws Z-Axis encoder reading on graph
  runPlot(plot4,width*1.5/4.2,height*0.5/4.2);    // Draws Z-Axis encoder reading on graph
  runPlot(plot5,width*1.5/4.2,height*0.5/4.2);    // Draws Z-Axis encoder reading on graph
  
  // Parse Motor Card serial comms to extract encoder reading if button clicked and plot values
  if (myPort.available() > 0)
  {
    // read entire serial output line as a massive string
    dataString = new String(myPort.readBytes(),StandardCharsets.UTF_8).replaceAll("\r","").replaceAll("\n","");
    //myPort.write("<"+dataArray[0].charAt(0)+",RI>");
    
    dataArray = dataString.split(","); // convert massive string into individual strings
    
    datain = new float[dataArray.length];
    
    if((dataArray.length == 16) & (Flag == true))
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
      plot4.addPoint(t5,datain[11]);
      Thrust.setText(str(datain[11]));
      t5++;
      plot5.addPoint(t5,datain[11]);
      Torque.setText(str(datain[11]));
      t5++;
     }
  }
}

public void controlEvent(ControlEvent theEvent) // Event Handler for UI Inputs
{
  println(theEvent.getController().getName());
  if(theEvent.getController().getName() == "Manual")
  {
    Manual(Manual);
  }
}


// Motion Functions
public void Start() 
{
   Flag = true;
}

public void Step() // Setup Axes
{ 
  myPort.write("<C,200>");
  println(200);
}

public void Routine() // Setup Axes
{ 
  myPort.write("<C,300>");
  println(300);
}

public void Manual(int output)
{
  myPort.write("<C,"+output+">");
  println(output);
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
  Thrust.setText("0.0");
  Torque.setText("0.0");
  
  t1 = 0;t2 = 0;t3 = 0;t4 = 0;t5 = 0;t6 = 0;
  
  myPort.stop();
  myPort.clear();
  myPort = new Serial(this,Serial.list()[0], 115200);
  
  background(50); // Reset background
 
  setupPlot(plot ,165,5  ,200,100,"Voltage"); // call encoder plot setup function
  setupPlot(plot1,165,255,200,100,"Current"); // call encoder plot setup function
  setupPlot(plot2,165,505,200,100,"RPM"); // call encoder plot setup function
  setupPlot(plot3,1000,5,200,100,"Throttle"); // call encoder plot setup function
  setupPlot(plot4,1000,255,200,100,"Thrust"); // call encoder plot setup function
  setupPlot(plot5,1000,505,200,100,"Torque"); // call encoder plot setup function
}
public void Close() // close program, disble motors, stop encoder read
{
  Flag = false;
  exit();
}
