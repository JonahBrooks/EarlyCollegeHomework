#########################################################################
# Calculates the volume of a spherical cap of a given height            #
# Steps through all heights in small chunks looking for a given volume  #
#########################################################################
import math
g = 25.     # m/s
Pw = 1000   # kg/m**3, density of water
m = 1.5*10**6 # kg, mass of the ship
r = 25.     # m, radius of the spherical ship

def Volume(h):   # Calculate the volume of a semisphere of height h
    volume = 0
    dz = 0.001
    z = r
    while z > (r-h):
        Rc = r**2 - z**2    # Radius of this dz tall disk squared
        volume += (math.pi*Rc)*dz # volume of this disk
        z -= dz
    return volume

Vb = m/Pw
print "Searching for Vb = ", Vb
v = 0
dh = 0.01
h = 0
while True:
    v = Volume(h)
    if v > Vb:
        break
    h += dh

print
print "Found nearest volume to be", v,"(m^3) at h = ", h, "(m)"
print "Where h is the height of the semisphere under the surface of the water."
print
print "So, the distance from the center to the water line is:", r-h, "(m)"
print "And the height of the sphere above the water is:", 2*r-h, "(m)"
