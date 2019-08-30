import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['figure.max_open_warning'] = 30
from matplotlib import pyplot as plt
import numpy
import sys
import os
from math import sqrt
from text_location_decider import Location_decider
sqrtsnn = float(sys.argv[1])#GeV
par = sys.argv[2]
values=sys.argv[3:]


pz_beam = sqrt(sqrtsnn*sqrtsnn/4.0 -0.938*0.938)
E_beam = sqrt(pz_beam*pz_beam + 0.938*0.938)
y_beam = 0.5 * numpy.log((E_beam + pz_beam)/(E_beam - pz_beam))
ymax=y_beam*1.2

energy_dict = {17.27: '158', 12.32: '80', 8.765:'40', 7.73: '30.9', 6.27: '20'}
plab = energy_dict[sqrtsnn]

beam_momentum = plab+'AGeV'

par_dict = {'String_Tension': r'\kappa', 'Gluon_Beta': r'\beta_\mathrm{gluon}',\
            'Gluon_Pmin': r'p_\mathrm{min,gluon}',\
            'Quark_Alpha': r'\alpha_\mathrm{quark}',\
            'Quark_Beta': r'\beta_\mathrm{quark}',\
            'Strange_Supp': r'\lambda_s',\
            'Diquark_Supp': r'\lambda_\mathrm{diquark}',\
            'Sigma_Perp': r'\sigma_T',\
            'StringZ_A': r'a_\mathrm{string}',\
            'StringZ_B': r'b_\mathrm{string}',\
            'String_Sigma_T': r'\sigma_{T,\mathrm{string}}',\
            'Prob_proton_to_d_uu': r'\xi',\
            'Leading_Frag_Mean': r'\mu_\mathrm{leading}',\
            'Leading_Frag_Width': r'\sigma_\mathrm{leading}',\
            'StringZ_A_Leading': r'a_\mathrm{leading}',\
            'StringZ_B_Leading': r'b_\mathrm{leading}',\
            'Popcorn_Rate': r'\mathrm{Popcorn\,Rate}'}
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
        'String_Sigma_T': r'\,\mathrm{GeV}',\
        'Prob_proton_to_d_uu': '',\
        'Leading_Frag_Mean': '',\
        'Leading_Frag_Width': '',\
        'StringZ_A_Leading': '',\
        'StringZ_B_Leading': '\,\mathrm{GeV^{-2}}',
        'Popcorn_Rate': ''}

label_dict={'p':r'$\mathrm{p}$', 'p_bar':r'$\mathrm{\bar{p}}$',\
            'n':r'$\mathrm{n}$',\
            'lambda': r'$\Lambda$', 'lambda_bar': r'$\bar{\Lambda}$',\
            'pi_plus': r'$\pi^+$', 'pi_minus':r'$\pi^-$',\
            'K_plus': r'$K^+$', 'K_minus': r'$K^-$'}

loc = Location_decider()
for particle in ['p','p_bar','pi_plus','pi_minus','K_plus', 'K_minus','n','lambda']:
  loc.set_particle(particle)
  #load experimental data
  try:
    data=numpy.loadtxt('exp_data/'+beam_momentum+'/'+particle+'_y')
    exp_y=data[:,0]
    exp_dndy=data[:,1]
    exp_err=(data[:,2]+data[:,3])
    y_exists=True
  except IOError:
    y_exists=False
  try:
    NA49 = numpy.loadtxt('NA49_data/'+beam_momentum+'/'+particle)
    xF_exp=NA49[:,0]
    dndxF_exp=NA49[:,1]
    dndxF_exp_err=NA49[:,2]*dndxF_exp/100.0#since its in percentage
    xF_exists=True
  except IOError:
    xF_exists=False
  if xF_exists:
    try:
      mpT_exp=NA49[:,3]
      mpT_exp_err=NA49[:,4]*mpT_exp/100.0#since its in percentage
      mpT_exists=True
    except IndexError:
      mpT_exists=False
  else:
    mpT_exists = False # Assuming xF and mpt only exist together

  #create figures
  fig1=plt.figure()
  ax1=fig1.add_subplot('111')
  loc.set_observable('y')
  ax1.text(loc.get_xpos(), loc.get_ypos(), label_dict[particle]+'\n'+\
           '$\sqrt{s}='+str(sqrtsnn)+ '\,\mathrm{GeV}$'+'\n'+ \
           '$\mathrm{SMASH\ 1.6}$',fontsize=15,\
           va=loc.get_va(), ha=loc.get_ha(), transform = ax1.transAxes)
  ax1.set_xlabel('$y$',fontsize=20)
  ax1.set_ylabel(r'$dN/dy$',fontsize=20)
  if y_exists:
    label_y=r'$\mathrm{NA61} \, p_{\rm lab}='+plab+r'\,\mathrm{GeV}$'
    ax1.errorbar(exp_y, exp_dndy, yerr=exp_err, fmt='o',\
                 markersize=8,label=label_y)

  fig2=plt.figure()
  ax2=fig2.add_subplot('111')
  #ax2.set_title(label_dict[particle]+r'$,\ \sqrt{s}='+str(sqrtsnn)+\
  #              r'\,\mathrm{GeV}$',fontsize=25)
  loc.set_observable('xF')
  ax2.text(loc.get_xpos(), loc.get_ypos(), label_dict[particle]+'\n'+\
           r'$\sqrt{s}='+str(sqrtsnn)+ r'\,\mathrm{GeV}$'+'\n'+ \
           '$\mathrm{SMASH\ 1.6}$',fontsize=15,\
           va=loc.get_va(), ha=loc.get_ha(), transform = ax2.transAxes)
  ax2.set_xlabel(r'$x_F$',fontsize=20)
  ax2.set_ylabel(r'$dN/dx_F$',fontsize=20)
  if xF_exists:
    ax2.errorbar(xF_exp,dndxF_exp,yerr=dndxF_exp_err,marker='o',\
                 linestyle='none',lw=2, label=r'$\mathrm{NA49\ data}$')

  fig3=plt.figure()
  ax3=fig3.add_subplot('111')
  #ax3.set_title(label_dict[particle]+r'$,\ \sqrt{s}='+str(sqrtsnn)+\
  #              r'\,\mathrm{GeV}$', fontsize=25)
  loc.set_observable('mpt')
  ax3.text(loc.get_xpos(), loc.get_ypos(), label_dict[particle]+'\n'+\
           r'$\sqrt{s}='+str(sqrtsnn)+ r'\,\mathrm{GeV}$' + '\n'+ \
           '$\mathrm{SMASH\ 1.6}$',fontsize=15,\
           va=loc.get_va(), ha=loc.get_ha(), transform = ax3.transAxes)
  ax3.set_xlabel(r'$x_F$',fontsize=20)
  ax3.set_ylabel(r'$\langle p_T \rangle \,\mathrm{\left[GeV\right]}$',fontsize=20)
  if mpT_exists:
    ax3.errorbar(xF_exp,mpT_exp,yerr=mpT_exp_err,marker='o',linestyle='none',lw=2,\
                 label=r'$\mathrm{NA49\ data}$')

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
                 label=r'$'+par_dict[par]+'='+val+unit[par]+'$')
    if particle=='p':
      ax2.set_ylim(bottom=0.0)
    else:
      ax2.set_yscale('log')
    mean_pT = numpy.load(foldername+particle+'_pT.npy')
    mean_pT_err = numpy.load(foldername+particle+'_pT_err.npy')
    # find first entry with bad statistics
    k=0
    while k < len(mean_pT) and mean_pT_err[k] / mean_pT[k] < 0.04: #relative error is 4%
      k += 1
    ax3.errorbar(xF_binmids[:k],mean_pT[:k], mean_pT_err[:k], lw=2,\
                 label=r'$'+par_dict[par]+'='+val+unit[par]+'$')

    y_hist = numpy.load(foldername+particle+'_y.npy')
    y_err = numpy.load(foldername+particle+'_y_err.npy')
    y_binwidth = 2*ymax/nbins
    y_binmids = (numpy.linspace(-ymax,ymax,nbins+1) + (0.5*y_binwidth*numpy.ones(nbins+1)))[:-1]
    ax1.errorbar(y_binmids,y_hist,yerr=y_err,lw=2,\
                 label=r'$'+par_dict[par]+'='+val+unit[par]+'$')
  ax1.set_xlim([0,ymax])
  ax1.set_ylim(bottom=0.0)
  legend1=ax1.legend(loc='best')
  legend3=ax3.legend(loc='best')
  legend2=ax2.legend(loc='best')

  if not os.path.exists(par+'_'+str(sqrtsnn)+'/y/'):
    os.makedirs(par+'_'+str(sqrtsnn)+'/y/')
  if not os.path.exists(par+'_'+str(sqrtsnn)+'/xF/'):
    os.makedirs(par+'_'+str(sqrtsnn)+'/xF/')
  if not os.path.exists(par+'_'+str(sqrtsnn)+'/mpt/'):
    os.makedirs(par+'_'+str(sqrtsnn)+'/mpt/')
  fig1.tight_layout()
  fig1.savefig(par+'_'+str(sqrtsnn)+'/y/'+particle+'.pdf')
  fig2.tight_layout()
  fig2.savefig(par+'_'+str(sqrtsnn)+'/xF/'+particle+'.pdf')
  fig3.tight_layout()
  fig3.savefig(par+'_'+str(sqrtsnn)+'/mpt/'+particle+'.pdf')


  



    




