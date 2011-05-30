#include <SPI.h>
#include <Ethernet.h>

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
byte ip[] = {192,168,0,177};
byte gateway[] = {192,168,0,1};
byte subnet[] = {255,255,255,0};

Server server(23);
Client client = 0;

const uint8_t LEFT_MOTOR_BIN1 = 24;
const uint8_t LEFT_MOTOR_BIN2 = 22;
const uint8_t LEFT_MOTOR_PWM  = 2;
//const uint8_t LEFT_MOTOR_FAULT= A0;

const uint8_t RIGHT_MOTOR_BIN1 = 28;
const uint8_t RIGHT_MOTOR_BIN2 = 26;
const uint8_t RIGHT_MOTOR_PWM  = 3;
//const uint8_t RIGHT_MOTOR_FAULT= A1;

const uint8_t FRONT1_MOTOR_BIN1 = 32; //Solid 
const uint8_t FRONT1_MOTOR_BIN2 = 30; //Stripe
const uint8_t FRONT1_MOTOR_PWM  = 5;
//const uint8_t FRONT_MOTOR_FAULT= A2;

const uint8_t REAR1_MOTOR_BIN1 = 34; //Solid
const uint8_t REAR1_MOTOR_BIN2 = 36; //Stripe
const uint8_t REAR1_MOTOR_PWM  = 6;
//const uint8_t REAR_MOTOR_FAULT= A3;

const uint8_t FRONT2_MOTOR_BIN1 = 42; //Solid
const uint8_t FRONT2_MOTOR_BIN2 = 40; //Stripe
const uint8_t FRONT2_MOTOR_PWM  = 7;
//const uint8_t FRONT_MOTOR_FAULT= A2;

const uint8_t REAR2_MOTOR_BIN1 = 44; //Solid
const uint8_t REAR2_MOTOR_BIN2 = 46; //Stripe
const uint8_t REAR2_MOTOR_PWM  = 8;
//const uint8_t REAR_MOTOR_FAULT= A3;

//*************************************
//SOLENOID PINS
const uint8_t SOLENOID_PIN[] = {23, 25, 27, 29, 31,
                                33, 35, 37, 39, 41};
//*************************************

const uint8_t PRESSURE_SENSOR_PIN = A2;

const uint8_t STANDBY_PIN = 38;

const int INSTRUCTION_LENGTH = 11;
const int SENSOR_DATA_LENGTH = 6;
int motor_maxPWM = 255; 

//new PID variables
float KP = 0;
float KI = 0;
float KD = 0;

int iMax = 100;
int iMin = -100;

int lastError = 0;
int sumError = 0;

int pidTarget = 0;
boolean pidOn = false;
boolean hoverOn = true;

boolean pidLock = false;
boolean manualLock = false;
//end new PID variables

void setup()
{
  pinMode(LEFT_MOTOR_BIN1,OUTPUT);
  pinMode(LEFT_MOTOR_BIN2,OUTPUT);
  pinMode(LEFT_MOTOR_PWM,OUTPUT);
  //pinMode(LEFT_MOTOR_FAULT,INPUT);
  
  pinMode(RIGHT_MOTOR_BIN1,OUTPUT);
  pinMode(RIGHT_MOTOR_BIN2,OUTPUT);
  pinMode(RIGHT_MOTOR_PWM,OUTPUT);
  //pinMode(RIGHT_MOTOR_FAULT,INPUT);
  
  pinMode(FRONT1_MOTOR_BIN1,OUTPUT);
  pinMode(FRONT1_MOTOR_BIN2,OUTPUT);
  pinMode(FRONT1_MOTOR_PWM,OUTPUT);
  //pinMode(FRONT_MOTOR_FAULT,INPUT);
  
  pinMode(REAR1_MOTOR_BIN1,OUTPUT);
  pinMode(REAR1_MOTOR_BIN2,OUTPUT);
  pinMode(REAR1_MOTOR_PWM,OUTPUT);
  //pinMode(REAR_MOTOR_FAULT,INPUT);
  
  pinMode(FRONT2_MOTOR_BIN1,OUTPUT);
  pinMode(FRONT2_MOTOR_BIN2,OUTPUT);
  pinMode(FRONT2_MOTOR_PWM,OUTPUT);
  //pinMode(FRONT_MOTOR_FAULT,INPUT);
  
  pinMode(REAR2_MOTOR_BIN1,OUTPUT);
  pinMode(REAR2_MOTOR_BIN2,OUTPUT);
  pinMode(REAR2_MOTOR_PWM,OUTPUT);
  //pinMode(REAR_MOTOR_FAULT,INPUT);

  for (int i = 0; i < 10; i++)
  {
    pinMode(SOLENOID_PIN[i], OUTPUT);
  }

  pinMode(PRESSURE_SENSOR_PIN,INPUT);
  
  TCCR3B |= _BV(WGM32);  // Force pins 2, 3, and 5 to Fast PWM mode
  TCCR4B |= _BV(WGM42);  // Force pins 6, 7, and 8 to Fast PWM mode
  
  pinMode(STANDBY_PIN, OUTPUT);
  digitalWrite(STANDBY_PIN, HIGH); // enable the H-Bridges

  Ethernet.begin(mac,ip,gateway,subnet);
  Serial.begin(9800);
  server.begin();
  client = server.available();
  
  analogReference(INTERNAL2V56); 
}

void loop()
{ 
  Communications();
}

////----------------------------------------------------------------------------------------------------------------------------------------------------\\\\
///                                                              Communications Functions                                                                \\\
//--------------------------------------------------------------------------------------------------------------------------------------------------------\\
//****************************************************
// Handles all communications between systems        *
// This will almost certainly need to be expanded    *
// into a set of functions, possibly a class         *
// This is a working prototype of the basic functions*
//****************************************************
void Communications()
{    
     static boolean newConnectionFlag = true;
     byte instructionBytes[INSTRUCTION_LENGTH] = {0,0,0,0,0,0,0,0,0,0,0};
     byte sensorData[SENSOR_DATA_LENGTH] = {0,0,0,0,0,0};
     client = server.available(); 
     //Serial.print("Code 5");
     if(client.connected())
     {  
       if(newConnectionFlag)
        {  
           Serial.println("Connected to client");
           newConnectionFlag = false;
        }
        if(client.available() > 0)
        {  
           for(int i = 0; i < INSTRUCTION_LENGTH; i++)
           {  
             instructionBytes[i] = client.read();
           }    
           
           GetSensorData(sensorData);
           //Serial.print("Code 4");
           client.write(sensorData, SENSOR_DATA_LENGTH);      
           // Replace with sending sensor data instead of repeating
           //client.write(instructionBytes, INSTRUCTION_LENGTH);
           DecodeInstruction(instructionBytes);
        }
     }
     GetSensorData(sensorData);
     //Serial.print((int)sensorData[0]);
     //Serial.println((int)sensorData[1]);
}

//*******************************************************************
// Receives a byte array of length INSTRUCTION_LENGTH               *
// First byte of array is OpCode, remaining bytes are operands      *
// Returns nothing, but calls sub-functions based on instruction    *
//*******************************************************************
void DecodeInstruction(byte* instructionArg)
{    byte OpCode = instructionArg[0];
     
     switch (OpCode)
     {  case 'M':
           //Serial.print("Code 1");
            MotorControl(instructionArg);
            break;
        case 'S':
           //Serial.print("Code 2");
            SolenoidCommand(instructionArg);
            break;
        case 'P':
           /*Serial.println("Code 3");
            Serial.print(instructionArg[0]);
            Serial.print(instructionArg[1]);
            Serial.print(instructionArg[2]);
            Serial.print(instructionArg[3]);
            Serial.print(instructionArg[4]);
            Serial.print(instructionArg[5]);*/
            PIDCommand(instructionArg);
            break;
        default:
            Serial.print("Invalid OpCode. Received:");
            Serial.println(OpCode);
            Serial.print(instructionArg[1]);
            Serial.print(instructionArg[2]);
            Serial.print(instructionArg[3]);
            Serial.print(instructionArg[4]);
            Serial.print(instructionArg[5]);
            Serial.print(instructionArg[6]);
            Serial.print(instructionArg[7]);
            Serial.print(instructionArg[8]);
            Serial.print(instructionArg[9]);
            Serial.println(instructionArg[10]);
     }
     //Serial.println(getFeedback());
}

////----------------------------------------------------------------------------------------------------------------------------------------------------\\\\
///                                                                Command Functions                                                                     \\\
//--------------------------------------------------------------------------------------------------------------------------------------------------------\\


//----------------------------------
// Fills the argument array with the
// data from each sensor pin on the board
//-----------------------------------
void GetSensorData(byte* sensorDataArg)
{  // Read the sensor pins and fill the array here
   int first = 0, second = 0;
   //int temp = analogRead(PRESSURE_SENSOR_PIN);
   int temp = random(1023);
   if (temp > 255)
   {
     first = temp / 256;
     second = temp % 256;
   }
   else
     second = temp;
   sensorDataArg[0] = first;
   sensorDataArg[1] = second;
}

void PIDCommand(byte* PIDVals)
{
  //Serial.println(int(PIDVals[1]));
  //Serial.println(int(PIDVals[1]) > 0);
  if (int(PIDVals[1]) > 0)
  {
    if (pidOn == false)
    {
      pidBegin();
      Serial.println(pidTarget);
      Serial.println(getFeedback());
    }
  }
  else
  {
    pidEnd();
  }
  
  if (pidOn == true)
  {
    if (int(PIDVals[1]) == 2)
    {
      pidBegin();
      Serial.println(pidTarget);
      Serial.println(getFeedback());
      hoverOn = true;
    }
    else if (int(PIDVals[1]) == 3)
    {
      pidBegin(int(PIDVals[2]));
      Serial.println(pidTarget);
      Serial.println(getFeedback());
      hoverOn = false;
    }
    KP = (float)((int)PIDVals[3]) / 10.0;
    KI = (float)((int)PIDVals[4]) / 100.0;
    KD = (float)((int)PIDVals[5]) / 10.0;
  }
}

void SolenoidCommand(byte* solVals)
{
   for(int i = 0; i < 10; i++)
   {
     if (solVals[i+1] == 1)
     {
       digitalWrite(SOLENOID_PIN[i], HIGH);
     }
     else
     {
       digitalWrite(SOLENOID_PIN[i], LOW); 
     }
   }       
}

//----------------------------------
// Accepts the full instruction array
// Array holds: OpCode, LeftMotorSpeed,
// RightMotorSpeed, FrontMotorSpeed,
// RearMotorSpeed, Direction bit flags
//-----------------------------------
void MotorControl(byte* motorSpeeds)
{   
    for(int i = 0; i < 4; i++)
    {   if(motorSpeeds[i+1] < 0)
        {  motorSpeeds[i+1] = abs(motorSpeeds[i+1]); } 
        if(motorSpeeds[i+1] >= motor_maxPWM)
        {  motorSpeeds[i+1] = motor_maxPWM; }
    }
    
    boolean D[5] = {0,0,0,0,0};
    D[0] = 0; // Not used, OpCode has no speed
    D[1] = (motorSpeeds[5] >> 3) & 1;
    D[2] = (motorSpeeds[5] >> 2) & 1;
    D[3] = (motorSpeeds[5] >> 1) & 1;
    D[4] = (motorSpeeds[5]) & 1;
    
    digitalWrite(LEFT_MOTOR_BIN1, D[1]);
    digitalWrite(LEFT_MOTOR_BIN2, !D[1]);
    analogWrite(LEFT_MOTOR_PWM, motorSpeeds[1]);
    
    digitalWrite(RIGHT_MOTOR_BIN1, D[2]);
    digitalWrite(RIGHT_MOTOR_BIN2, !D[2]);
    analogWrite(RIGHT_MOTOR_PWM, motorSpeeds[2]);
    
    if (pidOn == true && motorSpeeds[3] == 0 && motorSpeeds[4] == 0)
      pidControl();
    else
      MotorControlVert(D[3],D[4],motorSpeeds[3],motorSpeeds[4]);
}

void MotorControlVert(boolean mydir, int myspd)
{
    MotorControlVert(mydir, mydir, myspd, myspd);
}

void MotorControlVert(boolean frontdr, boolean reardr, int frontspd, int rearspd)
{
    //Serial.println("MCV");
    digitalWrite(FRONT1_MOTOR_BIN1, frontdr);
    digitalWrite(FRONT1_MOTOR_BIN2, !frontdr);
    analogWrite(FRONT1_MOTOR_PWM, frontspd);
    
    digitalWrite(REAR1_MOTOR_BIN1, reardr);
    digitalWrite(REAR1_MOTOR_BIN2, !reardr);
    analogWrite(REAR1_MOTOR_PWM, rearspd);
    
    digitalWrite(FRONT2_MOTOR_BIN1, frontdr);
    digitalWrite(FRONT2_MOTOR_BIN2, !frontdr);
    analogWrite(FRONT2_MOTOR_PWM, frontspd);
    
    digitalWrite(REAR2_MOTOR_BIN1, reardr);
    digitalWrite(REAR2_MOTOR_BIN2, !reardr);
    analogWrite(REAR2_MOTOR_PWM, rearspd);
}

////----------------------------------------------------------------------------------------------------------------------------------------------------\\\\
///                                                                  PID Functions                                                                       \\\
//--------------------------------------------------------------------------------------------------------------------------------------------------------\\

void setConstants(int myP, int myI, int myD)
{
  KP = myP;
  KI = myI;
  KD = myD;
}

void lockPID()
{
  unlockManual();
  pidLock = true;
}

void lockManual()
{
  unlockPID();
  manualLock = true;
}

void unlockPID()
{
  pidLock = false;
}

void unlockManual()
{
  manualLock = false;
}

int getFeedback()
{
  return analogRead(PRESSURE_SENSOR_PIN);
}

int setPIDTarget(int value)
{
  pidTarget = value;
  lastError = 0;
  sumError = 0; 
}

void pidBegin()
{
  //Serial.println(getFeedback());
  pidBegin(getFeedback());
}

void pidBegin(int targetpressure)
{
  setPIDTarget(targetpressure);
  pidOn = true;
}

void pidEnd()
{
  pidOn = false;
}

void pidControl(int targetpressure)
{
  Serial.print(targetpressure);
  Serial.print(" - ");
  Serial.println(getFeedback());
  pidBegin(targetpressure);
  pidControl();
}

void pidControl()
{
   int feedback = getFeedback();
   
   //determines error
   int error = feedback - pidTarget;
   
   //determines integral error
   sumError += error;
   
   //caps the possible integral error
   if (sumError > iMax)
     sumError = iMax;
   if (sumError < iMin)
     sumError = iMin;
   
   //calculates duty cycle
   int pidDuty = KP*error + KD*(error - lastError) + KI*(sumError);
   
   lastError = error;
   
   //determines direction of the motors
   boolean pidDirection;
   if (pidDuty < 0)
     pidDirection = true;
   else
     pidDirection = false;
     
   //makes sure duty cycle is positive
   pidDuty = abs(pidDuty);
     
   //caps the duty cycle
   if (pidDuty > motor_maxPWM)
     pidDuty = motor_maxPWM;
   
   MotorControlVert(pidDirection, pidDuty);
}
