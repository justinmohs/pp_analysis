''' make the dNdx_F plots from the gathered data 
expects an energy and an info about which particles from that energy should be
plotted like 200 pl 17 p as argv will plot only protons at sqrtsnn=17GeV 
and protons and lambdas at 200GeV
'''

import matplotlib
matplotlib.use('Agg')
import sys
import numpy
from matplotlib import pyplot as plt

config_file=open('plot_config.txt','r')
config=config_file.read()
config=config.split('\n')
config_info=[]
for i in range(len(config)):
  if config[i]: #not empty string
    line=config[i].split(' ')
    config_info.append('True'==line[0])
hannah_data=config_info[0]
lambda_205=config_info[3]
proton_205=config_info[2]
proton_175=config_info[1]
usedata=[proton_175,proton_205,lambda_205]
datafiles=['xf_dist_proton_175.exp',\
           'xf_dist_proton_205.exp', 'xf_dist_lambda_205.exp']
datalabels=['data protons Elab=175 AGeV', \
            'data protons Elab=205 AGeV', 'data lambdas Elab=205 AGeV']
sqrtsnn=[]
p_and_l=[] #p for only protons #l for only lambdas pl for both
for i in range(1,len(sys.argv)):
  if i%2 ==1:
    sqrtsnn.append(sys.argv[i])
  else:
    p_and_l. append(sys.argv[i])

binmids=[]
hist=[]
err=[]
labels=[]

for i in range(len(sqrtsnn)):
  if 'p' in p_and_l[i]:
    histogramm=numpy.load('data_'+sqrtsnn[i]+'/plot_data/protons.npy')
    hist.append(histogramm)
    nbins=len(histogramm)
    binwidth=1.0/nbins
    binmids.append(numpy.arange(binwidth/2.0,1,binwidth))
    err.append(numpy.load('data_'+sqrtsnn[i]+'/plot_data/protons_err.npy')) 
    labels.append('smash protons sqrtsNN='+str(sqrtsnn[i])+" GeV")
    
  if 'l' in p_and_l[i]:
    histogramm=numpy.load('data_'+sqrtsnn[i]+'/plot_data/lambdas.npy')
    hist.append(histogramm)
    nbins=len(histogramm)
    binwidth=1.0/nbins
    binmids.append(numpy.arange(binwidth/2.0,1,binwidth))
    err.append(numpy.load('data_'+sqrtsnn[i]+'/plot_data/lambdas_err.npy'))
    labels.append('smash lambdas sqrtsNN='+str(sqrtsnn[i])+" GeV")
plots=[]    
fig=plt.figure()
ax=fig.add_subplot(111)
plt.title('Proton+Proton')
ax.set_xlabel('$x_F$',fontsize=20)
ax.set_ylabel(r'$\frac{dN}{dx_F}$',fontsize=20)
ax.set_yscale('log')
for i in range(len(hist)):
  plots.append(ax.errorbar(binmids[i],hist[i],yerr=err[i],label=labels[i]))

if hannah_data:
  xf=[]
  protonhist=[]
  lambdahist=[]
  hannah_file=open('exp_data/dndxf.dat','r')
  for line in hannah_file:
    if line[0]=='#':
      continue
    data=line.split('\t')
    xf.append(float(data[0]))
    protonhist.append(data[1])
    lambdahist.append(data[2])
  plots.append(ax.plot(xf,protonhist,label='Hannah protons Elab=200AGeV'))
  plots.append(ax.plot(xf,lambdahist,label='Hannah lambdas Elab=200AGeV'))
for i in range(len(datafiles)):
  if usedata[i]:
    data=numpy.loadtxt('exp_data/'+datafiles[i])
    xf=data[:,0]
    hist=data[:,1]
    err=data[:,2]
    plots.append(ax.errorbar(xf,hist,yerr=err,label=datalabels[i]))
legend=plt.legend(loc='best')
plt.savefig('dndxF_sqrtsnn.pdf')
 
