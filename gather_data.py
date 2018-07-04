import sys
import numpy
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

sqrtsnn = sys.argv[1]
nfolders = int(sys.argv[2])
nevents = 0
for i in range(1, nfolders+1):
  foldername='data_'+sqrtsnn+'/'+str(i)+'/'
  neventfile=open(foldername+'nevents.txt','r')
  nevents+=int(neventfile.read()[:-1])
  if i==1:
    protonhist=numpy.load(foldername+'proton_hist.npy')
    lambdahist=numpy.load(foldername+'lambda_hist.npy')
  else:
    protonhist+=numpy.load(foldername+'proton_hist.npy')
    lambdahist+=numpy.load(foldername+'lambda_hist.npy')
nbins=len(protonhist)
binwidth = 1.0/nbins
binmids=(numpy.linspace(0,1,nbins+1) + (0.5*binwidth*numpy.ones(nbins+1)))[:-1]
err_proton = numpy.sqrt(protonhist)
err_lambda = numpy.sqrt(lambdahist)

normed_protons = protonhist/(nevents*binwidth)
normed_lambdas = lambdahist/(nevents*binwidth)
normed_proton_err = err_proton/(nevents*binwidth)
normed_lambda_err = err_lambda/(nevents*binwidth)

numpy.save('data_'+sqrtsnn+'/plot_data/protons',normed_protons)
numpy.save('data_'+sqrtsnn+'/plot_data/lambdas',normed_lambdas)
numpy.save('data_'+sqrtsnn+'/plot_data/protons_err',normed_proton_err)
numpy.save('data_'+sqrtsnn+'/plot_data/lambdas_err',normed_lambda_err)


fig=plt.figure()
ax=fig.add_subplot(111)
ax.set_xlabel('$x_F$',fontsize=25)
ax.set_yscale('log')
ax.set_ylabel('$\\frac{dN}{dx_F}$',fontsize=25)
ax.errorbar(binmids,normed_protons, yerr = normed_proton_err,label='$mathrm{Protons}\\, \\sqrt{s_{NN}}='+sqrtsnn+'$')
ax.errorbar(binmids,normed_lambdas, yerr = normed_lambda_err,label=r'$mathrm{Lambdas}\, \sqrt{s_{NN}}='+sqrtsnn+r'$')
legend=plt.legend(loc='best')
#plt.tight_layout()
plt.savefig('data_'+sqrtsnn+'/dndxF.pdf')

  
