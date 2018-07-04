import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['mathtext.fontset'] = 'stix'
from matplotlib import pyplot as plt
import numpy
import sys
import os
from math import sqrt
par = sys.argv[1]
values=sys.argv[2:]

sqrtsnn=17.27#GeV
pz_beam = sqrt(sqrtsnn*sqrtsnn/4.0 -0.938*0.938)
E_beam = sqrt(pz_beam*pz_beam + 0.938*0.938)
y_beam = 0.5 * numpy.log((E_beam + pz_beam)/(E_beam - pz_beam))
ymax=y_beam*1.2
beam_momentum='158AGeV'
plab='158'
par_dict = {'String_Tension': r'\kappa', 'Gluon_Beta': r'\beta_\mathrm{gluon}',\
            'Gluon_Pmin': r'p_\mathrm{min,gluon}',\
            'Quark_Alpha': r'\alpha_\mathrm{quark}',\
            'Quark_Beta': r'\beta_\mathrm{quark}',\
            'Strange_Supp': r's\bar{s}\, \mathrm{supp}',\
            'Diquark_Supp': r'\mathrm{Diquark\,supp}',\
            'Sigma_Perp': r'\sigma_T',\
            'StringZ_A': r'a_\mathrm{string}',\
            'StringZ_B': r'b_\mathrm{string}',\
            'String_Sigma_T': r'\sigma_{T,\mathrm{string}}'}
unit = {'String_Tension': r'\,\mathrm{GeV/fm}',\
        'Gluon_Beta': '',\
        'Gluon_Pmin': '\,\mathrm{GeV}',\
        'Quark_Alpha': '',\
        'Quark_Beta': '',\
        'Strange_Supp': '',\
        'Diquark_Supp': '',\
        'Sigma_Perp': r'\,\mathrm{GeV}',\
        'StringZ_A': '',\
        'StringZ_B': r'\,\mathrm{GeV^{-2}}',\
        'String_Sigma_T': r'\,\mathrm{GeV}'}

label_dict={'p':r'$\mathrm{p}$', 'p_bar':r'$\bar{p}$',\
            'lambda': r'$\Lambda$', 'lambda_bar': r'$\bar{\Lambda}$',\
            'pi_plus': r'$\pi^+$', 'pi_minus':r'$\pi^-$',\
            'K_plus': r'$K^+$', 'K_minus': r'$K^-$'}

for particle in ['p','p_bar','pi_plus','pi_minus','K_plus', 'K_minus']:
  #load experimental data
  data=numpy.loadtxt('exp_data/'+beam_momentum+'/'+particle+'_y')
  exp_y=data[:,0]
  exp_dndy=data[:,1]
  exp_err=(data[:,2]+data[:,3])
  NA49 = numpy.loadtxt('NA49_data/'+beam_momentum+'/'+particle)
  xF_exp=NA49[:,0]
  dndxF_exp=NA49[:,1]
  dndxF_exp_err=NA49[:,2]*dndxF_exp/100#since its in percentage
  mpT_exp=NA49[:,3]
  mpT_exp_err=NA49[:,4]*mpT_exp/100#since its in percentage

  #create figures
  fig1=plt.figure()
  ax1=fig1.add_subplot('111')
  ax1.set_title(label_dict[particle]+r' $\sqrt{s_{NN}}='+str(sqrtsnn)+\
                r'\,\mathrm{GeV}$',fontsize=25)
  ax1.set_xlabel('$y$',fontsize=30)
  ax1.set_ylabel(r'$dN/dy$',fontsize=30)
  label_y=r'$\mathrm{NA61} \, p_{lab}='+plab+r'\,\mathrm{GeV}$'
  ax1.errorbar(exp_y, exp_dndy, yerr=exp_err, fmt='o', mfc='m',ecolor='m',markersize=8,label=label_y)
  ax1.set_ylim(0,max(exp_dndy)*1.2)

  fig2=plt.figure()
  ax2=fig2.add_subplot('111')
  ax2.set_title(label_dict[particle]+r' $\sqrt{s_{NN}}='+str(sqrtsnn)+\
                r'\,\mathrm{GeV}$',fontsize=25)
  ax2.set_xlabel(r'$x_F$',fontsize=30)
  ax2.set_ylabel(r'$dN/dx_F$',fontsize=30)
  ax2.errorbar(xF_exp,dndxF_exp,yerr=dndxF_exp_err,marker='o',linestyle='none',lw=2,\
             label=r'$\mathrm{NA49\, data}$')

  fig3=plt.figure()
  ax3=fig3.add_subplot('111')
  ax3.set_title(label_dict[particle]+r' $\sqrt{s_{NN}}='+str(sqrtsnn)+\
                r'\,\mathrm{GeV}$', fontsize=25)
  ax3.set_xlabel(r'$x_F$',fontsize=30)
  ax3.set_ylabel(r'$\langle p_T \rangle \,\mathrm{\left[GeV\right]}$',fontsize=30)
  ax3.errorbar(xF_exp,mpT_exp,yerr=mpT_exp_err,marker='o',linestyle='none',lw=2,\
             label=r'$\mathrm{NA49\, data}$')

  for val in values:
    foldername="data_"+str(sqrtsnn)+"_"+par+"_"+val+'/plot_data/'
    #devide xF_hist by 2, because it includes forward and backward rapidity
    #while in the experiment they only include forward rapidity
    xF_hist = numpy.load(foldername+particle+'_xF.npy')/2
    xF_err = numpy.load(foldername+particle+'_xF_err.npy')/2
    nbins=len(xF_hist)
    binwidth=1.0/nbins
    xF_binmids=(numpy.linspace(0,1,nbins+1) + (0.5*binwidth*numpy.ones(nbins+1)))[:-1]
    ax2.errorbar(xF_binmids,xF_hist,yerr=xF_err,lw=2,\
                 label=r'$\mathrm{SMASH}\,'+par_dict[par]+'='+val+unit[par]+'$')
    ax2.set_ylim(0,1.2*max(xF_hist[:-1]))
    
    mean_pT = numpy.load(foldername+particle+'_pT.npy')
    mean_pT_err = numpy.load(foldername+particle+'_pT_err.npy')
    ax3.plot(xF_binmids,mean_pT,lw=2,\
                 label=r'$\mathrm{SMASH}\,'+par_dict[par]+'='+val+unit[par]+'$')

    y_hist = numpy.load(foldername+particle+'_y.npy')
    y_err = numpy.load(foldername+particle+'_y_err.npy')
    y_binwidth = 2*ymax/nbins
    y_binmids = (numpy.linspace(-ymax,ymax,nbins+1) + (0.5*y_binwidth*numpy.ones(nbins+1)))[:-1]
    ax1.errorbar(y_binmids,y_hist,yerr=y_err,lw=2,\
                 label=r'$\mathrm{SMASH}\,'+par_dict[par]+'='+val+unit[par]+'$')
  ax1.set_xlim([0,ymax])
  legend1=ax1.legend(loc='best')
  legend3=ax3.legend(loc='best')
  legend2=ax2.legend(loc='best')
  if not os.path.exists(par+'_'+str(sqrtsnn)+'/y/'):
    os.makedirs(par+'_'+str(sqrtsnn)+'/y/')
  if not os.path.exists(par+'_'+str(sqrtsnn)+'/xF/'):
    os.makedirs(par+'_'+str(sqrtsnn)+'/xF/')
  if not os.path.exists(par+'_'+str(sqrtsnn)+'/mpt/'):
    os.makedirs(par+'_'+str(sqrtsnn)+'/mpt/')

  fig1.savefig(par+'_'+str(sqrtsnn)+'/y/'+particle+'.pdf')
  fig2.savefig(par+'_'+str(sqrtsnn)+'/xF/'+particle+'.pdf')
  fig3.savefig(par+'_'+str(sqrtsnn)+'/mpt/'+particle+'.pdf')


  



    




