Code to work with the root files in the "Air Shower Array"-experiment in the "Astroparticle-Physics-Lab-Course" in the Physics Masters at RWTH Aachen 

Code example:
from openROOT import *
from matplotlib.pyplot import show
rootFile = "data/testData.root"
print(getNEvents(rootFile))
plot = getPlot(rootFile, 49, 1, 1)
show()