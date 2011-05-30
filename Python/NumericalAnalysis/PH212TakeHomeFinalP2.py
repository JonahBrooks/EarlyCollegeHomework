import math
from visual.graph import *

display = gdisplay(xtitle="Altitude(m)",ytitle="Pressure(Pa)",
                   xmax = 10, xmin=0, ymax = 100, ymin = 0)
PvH = gcurve(gdisplay=display, color=color.cyan)

Ro = 9.*(10**5) #Radius of the planet's surface
G = 6.67*(10**-11)

Po = 1.22521    #Density of air on earth
M = 25.*Ro**2/G #Mass of planet, from GmM/R**2 = 25 m/s**2
r = Ro*1.01     #Radius to start countin for atmosphere

pressure = 0
dr = 0.01       #Delta radius
i = 0.0
while r >= (Ro):
    try:
        pressure += (math.exp(Ro-r)/(r**2))*dr
        #pressure += math.exp(Ro-r)*dr
    except:
        print Ro-r
        break
    r -= dr
    i += dr
    if i > .1 and r-Ro < 100:
        PvH.plot(pos=(r-Ro,pressure*G*M*3*Po))
        i = 0

pressure *= G*M*3*Po
#pressure *= 25*3*Po
print "Atmospheric pressure at surface:", pressure

#########################################################################
# Comment out everything above this section, and uncomment everything   #
# below this section to run the analysis on the triple integral.        #
#########################################################################

##import math
##from visual.graph import *
##
##display = gdisplay(xtitle="r(m)",ytitle="P(Pa)",xmax = 10, xmin=0,
##                   ymax = 100, ymin = 0)
##PvH = gcurve(gdisplay=display, color=color.cyan)
##
##Ro = 9.*(10**5) #Radius of the planet's surface
##Po = 1.22521    #Density of air on earth
##
##phi = 0
##dPhi = math.pi/1000
##stuffDphi = 0
##while phi < math.pi:
##    stuffDphi += sin(phi)*dPhi
##    phi += dPhi
##
##i=0
##r = Ro*1.01
##dr = 0.01
##stuffDr = 0
##while r >= Ro:
##    stuffDr += math.exp(Ro-r)*3*Po*r**2*dr
##    r -= dr
##    i += dr
##    if i > .1 and r-Ro < 100:
##        PvH.plot(pos=(r-Ro,stuffDr*stuffDphi*25./(2*Ro**2)))
##        i = 0
##
##stuff = stuffDphi*stuffDr*2*math.pi
##print "Mass in kilograms:", stuff
##stuff *= 25./(4*math.pi*Ro**2)
##print "Pressure in Pascals:", stuff
