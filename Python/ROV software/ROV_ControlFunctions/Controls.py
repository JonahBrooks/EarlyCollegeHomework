import pygame, math, sys, socket
from numpy import interp
from pygame.locals import *
from visual import *
from pgu import gui

Joy = False

Motorval = ['M',0,0,0,0,0]
Solval = ['S',0,0,0,0,0,0,0,0,0,0,0]

Motormax = 127
Motormin = -128
pitchFlag = False
Buttonflag = False
Buttonflag2 = False
theta = 0

XS1_val = 0
YS1_val = 0
YS2_val = 0
XS2_val = 0

hat_val = (0,0)
CG_arm = False
WC_arm = False
CandT_arm = False
PID_arm = False
PID_hover_flag = False
PID_godepth_flag = False
depth = 0
targetdepth = 0
kP = 0
kI = 0
kD = 0

### Temp code May 18th
sensorData = 0

PIDdata = ['P', PID_arm, depth, kP, kI, kD]
speedFlag = 0
speedVal = 1

speedLbl = None

#------------------------------------------------------------------------------
# Methods of this class.
#------------------------------------------------------------------------------
def emergeClick():
    print "hello"

def pidHover():
    global PID_hover_flag
    PID_hover_flag = True

def pidGoDepth():
    global targetdepth, depInput, PID_godepth_flag
    targetdepth = depToPresConv(depInput.value)
    PID_godepth_flag = True

def depToPresConv(value):
    return value

def pidDefault():
    print "PID DEFAULT"
    setP(0)
    setI(0)
    setD(0)

def pidCalibrate():
    print "CALIBRATE"

def operateWC():
    print "operateWC"
    
def makeAngle (x,y):
    try:
        beta = degrees(atan(y/x))
        if(x < 0): #quad 2 and 3
            beta += 180

        elif(x >= 0 and YS1_val < 0): # Quad 4
            beta += 360

    except:
        if(y > 0):
            beta = 90
        else:
            beta = 270

    return beta

#--------------------------------------------------------------------------------
#Getters and setters.
#--------------------------------------------------------------------------------
def getP():
    global P
    return P

def getI():
    global I
    return I

def getD():
    global D
    return D

def setP(x):
    global P
    P = x

def setI(x):
    global I
    I = x

def setD(x):
    global D
    D = x

### Temp code May 18th
def setSensorData(x):
    global sensorData
    sensorData = x
    ###print "Set sensor data: ", x ### Test code
#--------------------------------------------------------------------------------

def getPitchFlag ():
    global pitchFlag
    return pitchFlag

def setPitchFlag(x):
    global pitchFlag
    pitchFlag = x
    
#-------------------------------------------------------------------------------

def getCG_arm():
    global CG_arm
    return CG_arm

def setCG_arm(x):
    global CG_arm
    CG_arm = x
    
#-------------------------------------------------------------------------------

def getWC_arm():
    global WC_arm
    return WC_arm

def setWC_arm(x):
    global WC_arm
    WC_arm = x
    
#-------------------------------------------------------------------------------

def getCandT_arm():
    global CandT_arm
    return CandT_arm

def setCandT_arm(x):
    global CandT_arm
    CandT_arm = x
    
#-------------------------------------------------------------------------------

def getPID_arm():
    global PID_arm
    return PID_arm
    
def getPID_command():
    global PID_arm, PID_hover_flag
    if(PID_arm):
        if(PID_hover_flag):
            return 2
        if(PID_godepth_flag):
            return 3
        else:
            return 1
    else:
        return 0 

def setPID_arm(x):
    global PID_arm
    PID_arm = x
    
#-------------------------------------------------------------------------------

def getspeedVal():
    global speedVal
    return speedVal

def setspeedVal(x):
    global speedVal
    speedVal = x
    
#-------------------------------------------------------------------------------

def getMotormax ():
    global Motormax
    return Motormax
    
#-------------------------------------------------------------------------------

def getMotormin():
    global Motormin
    return Motormin


#-------------------------------------------------------------------------------

def getDepth():
    global depth
    #Fill this method with the requirements to calculate depth.

#-------------------------------------------------------------------------------
#Real methods.
def operateComp (n): # Activates the nth component if it's armed. n must be an int
        if(n == 1):
            if(CG_arm == True):
                print "Collecting Critters"
            else:
                print "The Critter Getter is disarmed"

        elif(n == 2):
            if(WC_arm == True):
                print "Collecting Water"
            else:
                print "The Water Collector is disarmed"

        elif(n == 3):
            if(CandC_arm == True):
                print "Deploying Cap"
            else:
                print "The Cap is disarmed"

        elif(n == 0):
            if(PID_arm == True):
                print "PID loop is active"
            else:
                print "The PID loop is disarmed"

#-------------------------------------------------------------------------------

def fireSol(n):
    global Solval

    if(Solval[n+1] == 0):
        Solval[n+1] = 1
        print "Solonioid "+str(n)+" is on"
    else:
        Solval[n+1] = 0
        print "Solonioid "+str(n)+" is off"
        
#------------------------------------------------------------------------------

def setMotorMax (Max): #changes the motor max and min that are referenced for the interp function
    Motormax = Max.value
    Motormin = -(Max.value + 1)
    print(Motormax)
    print(Motormin)

#------------------------------------------------------------------------------

def speedCycle():
    global speedVal, Motormax, Motormin
    global app, speedLbl
    speedVal = speedVal * 2
    if(speedVal > 4):
        speedVal = 1

    speedLbl.value = "1/" + str(speedVal)


#-------------------------------------------------------------------------------
# Arm and Use Subsystems.
#-------------------------------------------------------------------------------
def joySubCheck():
    global hat_val, Joysticks, WC_arm, CandT_arm, pitchFlag
    hat_val = Joysticks.get_hat(0)
            
    if(hat_val == (-1,0)):
        CC_arm = arm_disarm_Component(CC_arm)
            
    elif(hat_val == (0,-1)):
        WC_arm = arm_disarm_Component(WC_arm)
            
    elif(hat_val == (1,0)):
        CandT_arm = arm_disarm_Component(CandT_arm)

    if(Joysticks.get_button(0)):
        operateComp(0)

    if(Joysticks.get_button(1)):
        operateComp(1)

    if(Joysticks.get_button(2)):
        operateComp(2)

    if(Joysticks.get_button(3)):
        operateComp(3)
        
    if(Joysticks.get_button(4)):
        speedCycle()

    if(Joysticks.get_button(5)):
      arm_disarm_Component(pitchFlag)

#-------------------------------------------------------------------------------        

def setMotorValLR(x, y):# Sets the value for the motors depending on where the position of the joystick.
    global speedVal, Motormax, Motormin, Motorval
    
    motor1 = 0
    motor2 = 0

    # Dead zone ---------------------------------
    if(abs(x) < 16): 
        x = 0

    if(abs(y) < 16):
        y = 0
    
    VecA = (x, y)
    value = mag(VecA)

    if(value > Motormax):
        value = Motormax
        
    alpha = makeAngle(x,y)
    
        
    # Forward ------------------------------------
    if(alpha >= 80 and alpha <= 100): 
        motor1 = value
        motor2 = value

    #alpha goes from -90 to 270, so two hard
    #reverse cases are needed

    # Reverse ------------------------------------
    elif(alpha >= 260 and alpha <= 270):
        motor1 = -value
        motor2 = -value
        
    # Reverse ------------------------------------
    elif(alpha >= -90 and alpha <= -80):
        motor1 = -value
        motor2 = -value

    # hard right ---------------------------------
    elif(alpha >= -10 and alpha <= 10):
        motor1 = value
        motor2 = -value

    # hard left ----------------------------------
    elif(alpha >= 170 and alpha <= 190): 
        motor1 = -value
        motor2 = value

    # Varfible right forward ---------------------
    elif(alpha > 10 and alpha < 80): 
        motor1 = value
        motor2 = cos(2*radians(alpha))*-value

    # Varible left forward -----------------------
    elif(alpha > 100 and alpha < 170): 
        motor1 = cos(2*radians(alpha) - math.pi)*value
        motor2 = value

    # varible left reverse ----------------------
    elif(alpha > 190 and alpha < 260): 
        motor1 = -value
        motor2 = cos(2*(radians(alpha) - math.pi))*value
        
    # Varible right reverse -----------------------
    elif(alpha + 360 > 280 and alpha + 360 < 350):
        motor1 = -value*(cos(2*radians(alpha-270)))
        motor2 = -value

    # Check to make sure the values arn't bigger the the motor max 
    if(motor1 > Motormax):
        motor1 = Motormax
        
    elif(motor1 < Motormin):
        motor1 = Motormin

    if(motor2 > Motormax):
        motor2 = Motormax
        
    elif(motor2 < Motormin):
        motor2 = Motormin

    #interp for the speed cycle
    motor1 = round(interp(motor1,[Motormin, Motormax], [Motormin/speedVal, Motormax/speedVal]), 0)
    motor2 = round(interp(motor2,[Motormin, Motormax], [Motormin/speedVal, Motormax/speedVal]), 0)

    Motorval[1] = motor1
    Motorval[2] = motor2
    #print(Motorval[1])
    #print(Motorval[2])
    
    #--------------------------------------------
    # End of setMotorValLR
    #--------------------------------------------

def setMotorValFB (x, y):
    global speedVal, Motormax, Motormin, Motorval
    
    motor3 = 0
    motor4 = 0
   
    # Dead zone ---------------------------------
    if(abs(y) <= 16): 
        y = 0
        
    VecB = (0, y)
    value = mag(VecB)
    
    if(value > Motormax):
        value = Motormax

    # Asend/Pitch up ----------------------------
    if(y > 10):
        if(pitchFlag == False):
            motor3 = value
            motor4 = value
        else:
            motor3 = value
            motor4 = -value

    # Desend/Pitch down -------------------------
    elif(y < -10):
        if(pitchFlag == False):
            motor3 = -value
            motor4 = -value
        else:
            motor3 = -value
            motor4 = value

    #interp for the speed cycle
    motor3 = round(interp(motor3,[Motormin, Motormax], [Motormin/speedVal, Motormax/speedVal]), 0)
    motor4 = round(interp(motor4,[Motormin, Motormax], [Motormin/speedVal, Motormax/speedVal]), 0)
            
    Motorval[3] = motor3
    Motorval[4] = motor4
    #print(Motorval[3])
    #print(Motorval[4])

    
    #--------------------------------------------
    # End of setMotorValFB
    #--------------------------------------------

#------------------------------------------------------------------------------

def arm_disarm_Component(comp): #Changes a compent flag to it's oppisit.
    global PID_arm, CG_arm, WC_arm, CandT_arm, pitchFlag
    if(comp == 0):
        setPID_arm(not PID_arm)
        print("PID is " + str(PID_arm))
    elif (comp == 1):
        setCG_arm(True)
        setWC_arm(False)
        setCandT_arm(False)
        print("Critter Getter is " + str(CG_arm))
        print("Water Collecter is " + str(WC_arm))
        print("Cap and Trade is " + str(CandT_arm))
    elif (comp == 2):
        setCG_arm(False)
        setWC_arm(True)
        setCandT_arm(False)
        print("Critter Getter is " + str(CG_arm))
        print("Water Collecter is " + str(WC_arm))
        print("Cap and Trade is " + str(CandT_arm))
    elif (comp == 3):
        setCG_arm(False)
        setWC_arm(False)
        setCandT_arm(True)
        print("Critter Getter is " + str(CG_arm))
        print("Water Collecter is " + str(WC_arm))
        print("Cap and Trade is " + str(CandT_arm))
    elif (comp == 4):
        setPitchFlag(not pitchFlag)
        print("pitch is " + str(pitchFlag))
    elif (comp == 5):
        setCG_arm(False)
        setWC_arm(False)
        setCandT_arm(False)
        print("Critter Getter is " + str(CG_arm))
        print("Water Collecter is " + str(WC_arm))
        print("Cap and Trade is " + str(CandT_arm))


#------------------------------------------------------------------------------
def SCButton():
    global Buttonflag, Joysticks

    if(Buttonflag == False and Joysticks.get_button(4) == True):
        speedCycle()
        Buttonflag = True
        
    elif(Buttonflag == True):
        if(Joysticks.get_button(4) == False):
            Buttonflag = False
            print Buttonflag


#------------------------------------------------------------------------------
def pitchButton():
    global Joysticks, Buttonflag2, pSwitch

    if(Buttonflag2 == False and Joysticks.get_button(5) == True):
        print "step 1"
        arm_disarm_Component(4)
        pSwitch.value = not pSwitch.value
        print pSwitch.value
        Buttonflag2 = True
        
    elif(Buttonflag2 == True):
        if(Joysticks.get_button(5) == False):
            Buttonflag2 = False
            
            

            
#------------------------------------------------------------------------------
    
def GuiSetup():
    global app
    global MotorMin, MotorMax
    global LSlider, RSlider, FSlider, ASlider
    global speedLbl, depLbl, preLbl, depInput
    global pSwitch, Pbox, Ibox, Dbox
    
    app = gui.Desktop()
    app.connect(gui.QUIT, app.quit, None)

    Main = gui.Table(width = 900)
    Main.tr()

    # c.tr() makes a row
    # c.td(component) creates a cell

    # Top panel for displaying network status and emergancy options
    n = gui.Table()
    n.tr()

    n.td(gui.Label("Network: Status"), height = 40)
    n.td(gui.Label("       "))
    emergeButton = gui.Button("In Case of Emergency")
    emergeButton.connect(gui.CLICK, emergeClick)
    n.td(emergeButton)

    #Make sub tabels to be put into c that hold seperate elements.

    #tabel on the "west" side of the frame.
    w = gui.Table()
    w.tr()
    #Radio button group
    w.tr()
    w1 = gui.Table()

    w1.tr()
    w1.td(gui.Label("PID Controls"), colspan = 5, height = 50)
    w1.tr()
    pidSwitch =gui.Switch(value = False)
    pidSwitch.connect(gui.CLICK, arm_disarm_Component,0)
    w1.td(pidSwitch)
    w1.td(gui.Label("Arm "))
    w1.td(gui.Label(""), width = 95, height = 30)
    pidButton1 = gui.Button("Hover")
    pidButton1.connect(gui.CLICK, pidHover)
    w1.td(pidButton1, align = 1)

    w.td(w1, align = -1)

    w.tr()
    w2 = gui.Table()

    w2.tr()
    depInput = gui.Input(size = 6)
    w2.td(depInput, align = -1)
    w2.td(gui.Label("m "), align = -1, width = 30, height = 30)
    pidButton2 = gui.Button("Go to depth")
    pidButton2.connect(gui.CLICK, pidGoDepth)
    w2.td(pidButton2, align = 1)

    w.td(w2, align = -1)


    #Sliders to control coeficients
    w.tr()
    w3 = gui.Table()

    #P
    w3.tr()
    #w3.td(gui.Label("Stable "))
    Pbox = gui.Input(value = "0",height=16,width=120)
    w3.td(Pbox)
    w3.td(gui.Label(" Quick"), align = -1)

    #I
    w3.tr()
    #w3.td(gui.Label("Stable "))
    Ibox = gui.Input(value = "0",height=16,width=120)
    w3.td(Ibox)
    w3.td(gui.Label(" Accurate"), align = -1)

    #D
    w3.tr()
    #w3.td(gui.Label("Cautious "))
    Dbox = gui.Input(value = "0",height=16,width=120)
    w3.td(Dbox)
    w3.td(gui.Label(" Responsive"), align = -1)

    w.td(w3, align = -1)

    #Restore PID defaults button
    w.tr()
    w4 = gui.Table()

    w4.tr()
    pidButton3 = gui.Button("Restore PID Defaults")
    pidButton3.connect(gui.CLICK, pidDefault)
    w4.td(pidButton3, valign = 1)
    w4.td(gui.Label(""), height = 30)
    
##    w4.tr()
##    pidButton4 = gui.Button("Auto-Calibrate")
##    pidButton4.connect(gui.CLICK, pidCalibrate)
##    w4.td(pidButton4)
##    w4.td(gui.Label(""), height = 30)

    w.td(w4, align = -1)

    #Second panel under top panel for depth, pressure, and subsytems label
    w.tr()
    w5 = gui.Table()

    w5.tr()
    w5.td(gui.Label("Depth "), height = 30, align = -1)
    depLbl = gui.Input("0", size = 6)
    w5.td(depLbl, align = 1)
    w5.td(gui.Label(" m"))
    w5.tr()
    w5.td(gui.Label("Pressure "), align = -1)
    preLbl = gui.Input("0", size = 6)
    w5.td(preLbl, align = 1)
    w5.td(gui.Label(" kPa"))

    w.td(w5, align = -1)
    
    #Soleniod controls
    w.tr()
    w.td(gui.Label("Solenoid Controls "), height = 30, align = -1)
    w.tr()
    w6 = gui.Table()
    w6.tr()
    
    sol0 = gui.Switch(false)
    sol0.connect(gui.CLICK, fireSol, 0)
    w6.td(sol0)

    sol1 = gui.Switch(false)
    sol1.connect(gui.CLICK, fireSol, 1)
    w6.td(sol1)

    sol2 = gui.Switch(false)
    sol2.connect(gui.CLICK, fireSol, 2)
    w6.td(sol2)
    
    sol3 = gui.Switch(false)
    sol3.connect(gui.CLICK, fireSol, 3)
    w6.td(sol3)

    sol4 = gui.Switch(false)
    sol4.connect(gui.CLICK, fireSol, 4)
    w6.td(sol4)

    sol5 = gui.Switch(false)
    sol5.connect(gui.CLICK, fireSol, 5)
    w6.td(sol5)

    sol6 = gui.Switch(false)
    sol6.connect(gui.CLICK, fireSol, 6)
    w6.td(sol6)

    sol7 = gui.Switch(false)
    sol7.connect(gui.CLICK, fireSol, 7)
    w6.td(sol7)

    sol8 = gui.Switch(false)
    sol8.connect(gui.CLICK, fireSol, 8)
    w6.td(sol8)

    sol9 = gui.Switch(false)
    sol9.connect(gui.CLICK, fireSol, 9)
    w6.td(sol9)

    w.td(w6, align = 0)

    w.tr()
    w.td(gui.Label("0 1 2 3 4 5 6 7 8 9"), height = 30, align = 0)
    
    
    

    # Center tabel that holds all the navigation data.
    c = gui.Table()

    #verticle sliders for motor bars and space for surface.
    c.tr()

    c1 = gui.Table()
    c1.tr()
    LSlider = gui.VSlider(value=0,min=Motormin,max=Motormax,size=20,height=120,width=16)
    RSlider = gui.VSlider(value=0,min=Motormin,max=Motormax,size=20,height=120,width=16)
    FSlider = gui.VSlider(value=0,min=Motormin,max=Motormax,size=20,height=120,width=16)
    ASlider = gui.VSlider(value=0,min=Motormin,max=Motormax,size=20,height=120,width=16)
    c1.td(LSlider, width = 20, valign = 1)
    c1.td(RSlider, width = 20, valign = 1)
    c1.td(gui.Label("  Surface  "), height = 180, width = 240)
    c1.td(FSlider, width = 20, valign = 1)
    c1.td(ASlider, width = 20, valign = 1)
    c1.tr()
    c1.td(gui.Label("L"))
    c1.td(gui.Label("R"))
    c1.td(gui.Label(""))
    c1.td(gui.Label("F"))
    c1.td(gui.Label("A"))

    c.td(c1)

    # Motor duty cycle bar.
    c.tr()

    c2 = gui.Table()
    c2.tr()
    c2.td(gui.Label(" Motor Duty Cycle "), height = 50, colspan = 3, valign = 1)
    c2.tr()
    c2.td(gui.Label("0 "), height = 30)
    MotormaxS = gui.HSlider(value=25,min=0,max=127,size=20,height=16,width=120)
    MotormaxS.connect(gui.CHANGE, setMotorMax, MotormaxS) 
    c2.td(MotormaxS)
    c2.td(gui.Label(" 100"))

    c.td(c2)

    #motor configuration graphic
    c.tr()

    c3 = gui.Table()
    c3.tr()
    c3.td(gui.Label(""), height = 30)
    c3.tr()
    c3.td(gui.Label(" Motor Configuration "))
    c3.tr()
    c3.td(gui.Label("  Surface  "), height = 150, width = 150)
    c3.tr()
    c3.td(gui.Label(""), height = 30)

    c.td(c3)

    #Radio Buttons for controling pitch and button for speed cycle.
    c.tr()

    c4 = gui.Table()
    c4.tr()
    pSwitch =gui.Switch(value = False)
    pSwitch.connect(gui.CLICK, arm_disarm_Component,4)
    c4.td(pSwitch)
    c4.td(gui.Label("Pitch on"))
    c4.td(gui.Label("     "))

    spdCycButton = gui.Button("Speed Cycle")
    spdCycButton.connect(gui.CLICK, speedCycle)
    c4.td(spdCycButton)

    c4.tr()
    speedLbl = gui.Input("1/1", size = 4, align = 1)
    c4.td(speedLbl, colspan = 4, align = 1)

    c.td(c4)

    # East tabel for hold all the subsystems functions.
    e = gui.Table(width = 200)
    e.tr()
    e.td(gui.Label(" Subsystems "), height = 50)

    e.tr()

    sysSelectGroup = gui.Group(value = 0)

    disarmRadio = gui.Radio(sysSelectGroup, value = 0)
    disarmRadio.connect(gui.CLICK, arm_disarm_Component,5)

    e0 = gui.Table()
    e0.tr()
    e0.td(disarmRadio, width = 20)
    e0.td(gui.Label("Disarm All"))

    e.td(e0)

    # Critter Getter functions.
    e.tr()

    e1 = gui.Table()
    e1.tr()


    e1a = gui.Table()
    e1a.tr()
    e1a.td(gui.Label("Critter Getter"), height = 29, align = -1)
    e1a.td(gui.Label(), width = 30)
    cgRadio = gui.Radio(sysSelectGroup, value = 1)
    cgRadio.connect(gui.CLICK, arm_disarm_Component,1)
    e1a.td(cgRadio)
    e1a.td(gui.Label("Arm "))
    e1a.td(gui.Label(""), height = 29, width = 20)
    e1.td(e1a, align = -1)

    e1.tr()
    e1b = gui.Table()
    e1b.tr()
    e1b.td(gui.Label("Status: "), height = 29, align = -1)
    critLbl = gui.Input(size = 15)
    e1b.td(critLbl)
    e1.td(e1b, align = -1)

    e1.tr()

    e1b = gui.Table()
    e1b.tr()
    cgButton1 = gui.Button("Flush")
    cgButton2 = gui.Button("Extend")

    cgButton1.connect(gui.CLICK, operateWC, 1)
    cgButton2.connect(gui.CLICK, operateWC, 2)
    
    e1b.td(cgButton1)
    e1b.td(gui.Label(""), height = 29)
    e1b.td(cgButton2)
    e1.td(e1b, align = -1)

    e.td(e1, height = 120, align = -1)

    #Water Collecter functions.
    e.tr()

    e2 = gui.Table()
    e2.tr()
    
    e2a = gui.Table()
    e2a.tr()
    e2a.td(gui.Label("Water Collecter"), height = 29, align = -1)
    e2a.td(gui.Label(), width = 30)
    wcRadio = gui.Radio(sysSelectGroup, value = 2)
    wcRadio.connect(gui.CLICK, arm_disarm_Component,2)
    e2a.td(wcRadio)
    e2a.td(gui.Label("Arm "))
    e2a.td(gui.Label(""), height = 29, width = 20)
    e2.td(e2a, align = -1)

    e2.tr()
    e2b = gui.Table()
    e2b.tr()
    e2b.td(gui.Label("Status: "), height = 29, align = -1)
    wcLbl = gui.Input(size = 15)
    e2b.td(wcLbl)
    e2.td(e2b, align = -1)

    e2.tr()
    e2c = gui.Table()
    e2c.tr()
    wcButton = gui.Button("Operate")
    e2c.td(wcButton, height = 29)
    e2.td(e2c, align=-1)

    e.td(e2, height = 120, align = -1)

    #Cap and trade functions.
    e.tr()

    e3 = gui.Table()
    e3.tr()
    
    #CandTarm_disarm = gui.Group(value = 2)
    e3a = gui.Table()
    e3a.tr()
    e3a.td(gui.Label("Cap and Trade"), height = 29, align = -1)
    e3a.td(gui.Label(), width = 30)
    ctRadio = gui.Radio(sysSelectGroup, value = 3)
    ctRadio.connect(gui.CLICK, arm_disarm_Component,3)
    e3a.td(ctRadio)
    e3a.td(gui.Label("Arm "))
    e3a.td(gui.Label(""), height = 29, width = 20)
    e3.td(e3a, align =-1)

    e3.tr()
    e3b = gui.Table()
    e3b.tr()
    e3b.td(gui.Label("Status: "), height = 29, align = -1)
    ctLbl = gui.Input(size = 15)
    e3b.td(ctLbl)
    e3.td(e3b, align = -1)

    e3.tr()
    ctButton1 = gui.Button("Operate")
    e3.td(ctButton1, height = 29, align = -1)

    e.td(e3, height = 120, align = -1)

    #put it together.
    Main.tr()
    Main.td(n, colspan = 3)
    Main.tr()
    Main.td(gui.Label(""), height = 30)
    Main.tr()
    Main.td(w, valign = -1)
    Main.td(c, valign = -1)
    Main.td(e, valign = -1)
    Main.tr()
    Main.td(gui.Label(""), height = 30)

    app.init(Main)#Main is main tabel.

def init():
    global Joy, Joysticks
    pygame.init()

    #-----------------------------------------------------------------------------
    #Main gui window
    #-----------------------------------------------------------------------------
    Joy = True
    print(pygame.joystick.get_count())
    try:
        x = pygame.joystick.get_count()
        if (x == 0):
            print("no Joystick detected by the computer")
            Joy = False
        print(x)
    except:
        print("no Joystick detected in port")
        Joy = False

##    Motorval = ['M',0,0,0,0,0]
##    Solval = ['S',0,0,0,0,0,0,0,0,0,0,0]
##
##    Motormax = 127
##    Motormin = -128
##    pitchFlag = False
##    Buttonflag = False
##    Buttonflag2 = False
##    theta = 0

    if(Joy):
        Joysticks = pygame.joystick.Joystick(0)
        Joysticks.init()

##    XS1_val = 0
##    YS1_val = 0
##    YS2_val = 0
##    XS2_val = 0
##
##    hat_val = (0,0)
##    CG_arm = False
##    WC_arm = False
##    CandT_arm = False
##    PID_arm = False
##    PID_hover_flag = False
##    PID_godepth_flag = False
##    depth = 0
##    targetdepth = 0
##    kP = 0
##    kI = 0
##    kD = 0
##
##    PIDdata = ['P', PID_arm, depth, kP, kI, kD]
##    speedFlag = 0
##    speedVal = 1
##
##    speedLbl = None
    GuiSetup()

#------------------------------------------------------------------------------

def Refresh(arg): # Called from ROVcontrol to execute all control functions.
    global app, Motormin, Motormax, Motorval, Joy, Joysticks
    global LSlider, RSlider, FSlider, ASlider
    global depLbl, preLbl
    global PID_hover_flag, PID_godepth_flag, Pbox, Ibox, Dbox, kP, kI, kD
    global targetdepth
    app.loop()
    pygame.event.pump()

    PID_hover_flag = False
    PID_godepth_flag = False

    # Udate PID array.
    kP = int(Pbox.value)
    kI = int(Ibox.value)
    kD = int(Dbox.value)
    
    if(Joy):
        XS1_val = round(interp(Joysticks.get_axis(0),[-1,1], [Motormin, Motormax]), 0) #Rounds to 3 decimal places. will be replaced with an interp funtion later
        YS1_val = round(-interp(Joysticks.get_axis(1),[-1,1], [Motormin, Motormax]), 0)
        XS2_val = round(interp(Joysticks.get_axis(2),[-1,1], [Motormin, Motormax]), 0)
        YS2_val = round(-interp(Joysticks.get_axis(3),[-1,1], [Motormin, Motormax]), 0)
        SCButton()
        pitchButton()
    else:
        XS1_val = 0
        YS1_val = 0
        XS2_val = 0
        YS2_val = 0
        
    setMotorValLR(XS1_val, YS1_val)
    setMotorValFB(XS2_val, YS2_val)

    LSlider.value = -Motorval[1]
    RSlider.value = -Motorval[2]
    FSlider.value = -Motorval[3]
    ASlider.value = -Motorval[4]

    depLbl.value = " " + str(sensorData) ###str(Motorval[1])
    preLbl.value = " " + str(sensorData) ###str(Motorval[2])
    ###print "Updated Labels with: ", sensorData ### Test code
    
    #---------------------------------------------------------------------------
    # send the values to micro controller.
    #---------------------------------------------------------------------------

    Motorval[5] = 0
    if(Motorval[1] < 0):
        Motorval[5] += 8
        Motorval[1] = abs(Motorval[1])
    if(Motorval[2] < 0):
        Motorval[5] += 4
        Motorval[2] = abs(Motorval[2])
    if(Motorval[3] < 0):
        Motorval[5] += 2
        Motorval[3] = abs(Motorval[3])
    if(Motorval[4] < 0):
        Motorval[5] += 1
        Motorval[4] = abs(Motorval[4])

    Instruction = bytearray(11)
    Instruction[0] = 'M'

    for i in range(1, 6):
        #[opCode,left, right, front, back, DirectionFlags]
        Instruction[i] = int(round(Motorval[i], 0))
    
    PIDdata = bytearray(11)
    PIDdata[0] = 'P'
    PIDdata[1] = int(getPID_command())
    #print int(PIDdata[1])
    PIDdata[2] = int(targetdepth)
    PIDdata[3] = kP
    PIDdata[4] = kI
    PIDdata[5] = kD
    #print PIDdata
    
    Solval2 = bytearray(11)
    Solval2[0] = 'S'

    for i in range(1, 11):
        Solval2[i] = Solval[i]

    return (PIDdata, Instruction, Solval2)
    
#--------------------------------------------------------------------------------


##while(True):
##    Refresh(None)
##    pygame.time.wait(10)
