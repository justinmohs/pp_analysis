import sys
import numpy
from math import sqrt

datafile=open(sys.argv[1]+'/particle_lists.oscar')
particlecounter=0
nproton=0
nlambda=0
next_line_relevant=False
sqrtsnn = float(sys.argv[2])
pzmax = sqrt(sqrtsnn*sqrtsnn/4.0 -0.938*0.938)
nbins=20
binwidth=1.0/nbins
nevents=0
full_lambda_hist=numpy.zeros(nbins)
full_proton_hist=numpy.zeros(nbins)
for line in datafile:
  if line[0] == '#': #end of event
    if particlecounter > 2: #see if collision happened
      nevents+=1
      if nproton != 0:
        full_proton_hist+=protonhist
      if nlambda != 0:
        full_lambda_hist+=lambdahist
    particlecounter=0
    nproton=0
    nlambda=0
    continue
  particlecounter+=1
  particle=line.split(' ')
  pdg=particle[9]

  if pdg == '2212': #Proton
    if nproton == 0:
      protonhist = numpy.zeros(nbins)
    nproton+=1
    pz = float(particle[8])
    x_F = abs(pz)/pzmax
    if x_F >= 1.0:
      protonhist[nbins-1]+=1
    else:
      protonhist[x_F/binwidth]+=1

  if pdg == '3122': #Lambda
    if nlambda == 0:
      lambdahist = numpy.zeros(nbins)
    nlambda+=1
    pz = float(particle[8])
    x_F = abs(pz)/pzmax
    if x_F>=1:
      lambdahist[nbins-1]+=1
    else:
      lambdahist[x_F/binwidth]+=1
print full_proton_hist
numpy.save(sys.argv[1]+'/proton_hist',full_proton_hist)
numpy.save(sys.argv[1]+'/lambda_hist',full_lambda_hist)
output=open(sys.argv[1]+'/nevents.txt','w')
print >> output, nevents

