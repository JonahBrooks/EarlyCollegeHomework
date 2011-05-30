###########################################################################
# This program simulates the Earth revolving around the Sun, and the      #
# Moon and a Geostationary Satellite revolving around the Earth.          #
# The "Sun" only exists as a source of gravity and a source of light.     #
# This program simulates one day of motion every second, meaning that the #
# Earth goes around once a second, the moon orbits once every ~27 seconds,#
# and the light source shifts once around the earth every ~6 minutes.     #
#                                                                         #
# Either your computer needs to support Pixel Shader 3.0, or have         #
# PIL (http://www.pythonware.com/products/pil/#pil117   ) installed to    #
# display the Earth texture                                               #
#                                                                         #
# Created by Jonah Brooks on January 8th, 2011                            #
###########################################################################

from visual import *

PIL_Installed = False
try:
    import Image # Must install PIL
    name = "earth"
    width = 512 # must be power of 2
    height = 512 # must be power of 2
    im = Image.open(name+".jpg")
    im = im.resize((width,height), Image.ANTIALIAS)
    materials.saveTGA(name,im)
except:
    print "Python Image Library is not installed"
else:
    PIL_Installed = True
    
scene = display(title="Orbit",width=800,height=800,
                range=vector(4*10**8,4*10**8,4*10**8),center=vector(0,0,0),
                autoscale=0)
scene.lights = []
dt = 72     #Change in time, seconds = twentieth of an hour

G = 6.67 * 10**(-11)   #Gravitational constant

M = 5.9742*10**24     #Mass of the Earth, Kg
m = 7.36*10**22       #Mass of the Moon, Kg
Ms= 1.98892*10**30    #Mass of the Sub, Kg

mDist = 3.844*10**8   #Initial distance from the Earth to the Moon, in meters
sDist = 1.49598*10**11#Distance from the Sun to the Earth, one AU in meters
oDist = 4.2*10**7     #Distance from the Earth to the satellite



Se = vector(0.,0.,0.)           #Earth's position vector, meters
Sm = Se + vector(mDist,0.,0.)   #Moon's position vector, meters
Ss = Se - vector(sDist,0.,0.)   #Sun's position vector, meters
So = Se + vector(oDist,0.,0.)   #Satellite's position vector, meters


R = mag(Se-Sm)            #Distance between the Earth and the Moon
Rs= mag(Se-Ss)            #Distance between the Earth and the Sun
Ro= mag(Se-So)            #Distance between the Earth and the Sun
r = (M + m*mDist)/(M+m)   #Distance from Earth to Earth-Moon center of mass
rs= (M + Ms*sDist)/(M+Ms) #Distance from Earth to Earth-Sun center of mass

    # Initial velocity vectors derived by solving Centripital Force and
    # Universial Gravitational Force for velocity
        # Initial velocities for orbiting the Sun
Ve = vector(0.,sqrt(G*Ms*rs/Rs**2),0.)  #Velocity vector of the Earth, meters/sec
Vm = Ve                                 #Velocity vector of the Moon, meters/sec
Vs = vector(0.,0.,0.)                   #Velocity vector of the Sun, meters/sec

        # Updated velocities for Earth-Moon orbit 
Ve = Ve + vector(0.,-sqrt(G*m*r/R**2),0.)   
Vm = Vm + vector(0.,sqrt(G*M*(mDist-r)/R**2),0.) 
        #Velocity vector of the Satellite, meters/sec, from lecture
Vo = Ve + vector(0.,oDist*3.14159*2/(24*3600),0.) 


Ae = vector(G*m/(R**2),0.,0.)   #Acceleration vector of the Earth, meters/sec**2
Am = vector(-G*M/(R**2),0.,0.)  #Acceleration vector of the Moon, meters/sec**2
As = vector(0.,0.,0.)
Ao = vector(-G*M/(Ro**2),0.,0.)

Fe = vector(G*M*m/(R**2),0.,0.)     #Forces acting on the Earth, Newtons
Fm = vector(-G*M*m/(R**2),0.,0.)    #Forces acting on the Moon, Newtons
Fs = vector(0.,0.,0.)

if PIL_Installed == True:
    Earth = sphere(pos=Se, radius=6.38*10**6,
                   material=materials.texture(data=im, mapping="spherical"),
                   up=vector(0,0,1))
else:
    Earth = sphere(pos=Se, radius=6.38*10**6, material=materials.earth,
                   up=vector(0,0,1))
    
Moon = sphere(pos=Sm, radius=1.74*10**6, color=color.white)
Satellite = sphere(pos=So, radius = 10**6, color=color.white)
SunLight = local_light(pos=Ss, color=color.white)
dT = 2*3.14159*dt/(24*3600)  #Delta Theta of the earth's rotation

satelliteArrow = arrow(pos=Se, axis=(So-Se), shaftwidth=Satellite.radius/10)
satelliteArrow.visible = False    # Comment this out to see an arrow pointing
                                  # from the earth to the satellite
while True:
    rate(600) # Attempts to simulate one day per second
    R = mag(Se-Sm)
    Rs= mag(Se-Ss)
        # Update the various vectors of the Moon
    Fm = norm(Se-Sm)*G*M*m/R**2 + norm(Ss-Sm)*G*m*Ms/mag(Sm-Ss)**2  
    Am = Fm/m
    Vm = (Vm) + (Am*dt)
    Sm = (Sm) + (Vm*dt)

        # Update the various vectors of the Earth
    Fe = norm(Sm-Se)*G*M*m/R**2 + norm(Ss-Se)*G*M*Ms/Rs**2  
    Ae = Fe/M
    Ve = (Ve) + (Ae*dt)
    Se = (Se) + (Ve*dt)

        # Updates the various vectors of the Sun
    Fs = norm(Se-Ss)*G*M*Ms/Rs**2 + norm(Sm-Ss)*G*m*Ms/mag(Ss-Sm)**2
    As = Fs/Ms
    Vs = Vs + As*dt
    Ss = Ss + Vs*dt

        # Updates the various vectors of the Satellite
    Ao = norm(Se-So)*G*M/Ro**2 + norm(Sm-So)*G*m/mag(Sm-So)**2\
         + norm(Ss-So)*G*Ms/mag(Ss-So)**2
    Vo = Vo + Ao*dt
    So = So + Vo*dt
    
    Earth.pos = Se
    Moon.pos = Sm
    Satellite.pos = So
    SunLight.pos = Ss   
    Earth.rotate(angle=dT, axis=Earth.up, origin=Earth.pos)

    GCenter = Se + norm(Sm-Se)*r #Center of gravity in the Earth-Moon system
    scene.center = GCenter       #Center the camera on the center of gravity
    #scene.center = Earth.pos    # Uncomment this to fully center the Earth

    satelliteArrow.pos = Se
    satelliteArrow.axis=(So-Se)
    
