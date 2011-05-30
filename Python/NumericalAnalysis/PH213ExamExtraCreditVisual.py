import math
from visual import *

Eo = 8.85*10**-12  # Epsilon naught

L = 1.00*10**-3     # Length of the straw, in meters
q = 1.00*10**-6     # Charge of the straw, in Coulombs

s = 5.00*10**-4     # Meters from the base of the rod to the center of the ring

R = 1.00*10**-3     # Radius of the ring, in meters
Q = 1.00*10**-5     # Charge of the ring, in Coulombs

parts = 1000.0  # Number of parts to divide each object into for processing

dl = L/parts                # Small chunk of the straw's length
dTheta = 2*math.pi/parts    # Small chunk of the ring's angle
dq = q/parts                # Small chunk of the straw's charge
dQ = Q/parts                # Small chunk of the ring's charge

Fnet = 0    # Force of the ring on the straw, in Netwons

graphics = True             # Change this to False to disable graphics
if graphics == True:        # which will greatly decrease computing time
    hoop = ring(pos=vector(0,0,0), axis=vector(0,1,0), radius = R,
                    thickness=R/100, color=color.yellow)

    straw = cylinder(pos=vector(0,s,0), axis=vector(0,1,0), length = L,
                    radius = L/100, color=color.green)

    rLine = arrow(pos=vector(0,0,0), length=0, axis=vector(0,0,0),
                    shaftwidth=L/200, fixedwidth = True, color=color.white)

    dStraw = cylinder(pos=vector(0,s,0), axis=vector(0,1,0), length = dl*30,
                    radius = straw.radius*1.1, color=color.red)             

print "Computing the force of the ring on the straw..."
h = s
while h < (L + s):      
    r = math.sqrt(h**2 + R**2)
    cosPhi = h/r    # By symmetry we only need the vertical component
    if graphics == True:
        dStraw.y = h
    theta = 0
    while theta < 2*math.pi:
        #rate(200)
        Fnet += ((dq*dQ)/(4*math.pi*Eo*r**2))*(cosPhi)
        if graphics == True:
            rLine.pos = vector(R*cos(theta),0,R*sin(theta))
            rLine.axis = (vector(0,h,0)-rLine.pos)
            rLine.length = r
        theta += dTheta
    h += dl

print "\nFnet =\t", Fnet, "Newtons"

    # Now to compute the answer using the formula I derived via integration
FIntegral = (q*Q/(4*math.pi*Eo*L))  
FIntegral *= (1/(math.sqrt(R**2+s**2)) - 1/(math.sqrt(R**2+(s+L)**2)))

print "Or:\t", FIntegral, "Newtons from my formula"
print "\nThis simulation varies from my predicted value by %.3f%%" \
      % (100*abs(Fnet-FIntegral)/FIntegral)
