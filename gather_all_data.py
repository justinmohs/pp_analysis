import sys
import numpy
from math import sqrt

class PlotData:
  def __init__(self,nbins,sqrtsnn,rapidity_range_factor=1.2):
    self.sqrtsnn=sqrtsnn
    pzbeam = sqrt(float(sqrtsnn)*float(sqrtsnn)/4.0 -0.938*0.938)
    E_beam = sqrt(pzbeam*pzbeam+0.938*0.938)
    ybeam=0.5*numpy.log((E_beam+pzbeam)/(E_beam-pzbeam))
    self.ymax=ybeam*rapidity_range_factor
    self.nbins=nbins
    self.nevents=0
    self.p_hist_xF = numpy.zeros(nbins)
    self.p_bar_hist_xF = numpy.zeros(nbins)
    self.n_hist_xF = numpy.zeros(nbins)
    self.lambda_hist_xF = numpy.zeros(nbins)
    self.lambda_bar_hist_xF = numpy.zeros(nbins)
    self.pi_plus_hist_xF = numpy.zeros(nbins)
    self.pi_minus_hist_xF = numpy.zeros(nbins)
    self.K_plus_hist_xF = numpy.zeros(nbins)
    self.K_minus_hist_xF = numpy.zeros(nbins)

    self.p_hist_y = numpy.zeros(nbins)
    self.p_bar_hist_y = numpy.zeros(nbins)
    self.n_hist_y = numpy.zeros(nbins)
    self.lambda_hist_y = numpy.zeros(nbins)
    self.lambda_bar_hist_y = numpy.zeros(nbins)
    self.pi_plus_hist_y = numpy.zeros(nbins)
    self.pi_minus_hist_y = numpy.zeros(nbins)
    self.K_plus_hist_y = numpy.zeros(nbins)
    self.K_minus_hist_y = numpy.zeros(nbins)

    #this is not really a pt histogramm
    #it is the summed up pt in every xF bin
    self.p_hist_pT = numpy.zeros(nbins)
    self.p_bar_hist_pT = numpy.zeros(nbins)
    self.n_hist_pT = numpy.zeros(nbins)
    self.lambda_hist_pT = numpy.zeros(nbins)
    self.lambda_bar_hist_pT = numpy.zeros(nbins)
    self.pi_plus_hist_pT = numpy.zeros(nbins)
    self.pi_minus_hist_pT = numpy.zeros(nbins)
    self.K_plus_hist_pT = numpy.zeros(nbins)
    self.K_minus_hist_pT = numpy.zeros(nbins)

    self.p_pT2 = numpy.zeros(nbins)
    self.p_bar_pT2 = numpy.zeros(nbins)
    self.n_pT2 = numpy.zeros(nbins)
    self.lambda_pT2 = numpy.zeros(nbins)
    self.lambda_bar_pT2 = numpy.zeros(nbins)
    self.pi_plus_pT2 = numpy.zeros(nbins)
    self.pi_minus_pT2 = numpy.zeros(nbins)
    self.K_plus_pT2 = numpy.zeros(nbins)
    self.K_minus_pT2 = numpy.zeros(nbins)

    self.p_hist_mT=0
    self.p_mT2=0
    self.n_p_midrap=0

  def read_folder(self,foldername):
    self.p_hist_xF += numpy.load(foldername+'proton_xF.npy')
    self.p_bar_hist_xF += numpy.load(foldername+'proton_bar_xF.npy')
    self.n_hist_xF += numpy.load(foldername+'neutron_xF.npy')
    self.lambda_hist_xF += numpy.load(foldername+'lambda_xF.npy')
    self.lambda_bar_hist_xF += numpy.load(foldername+'lambda_bar_xF.npy')
    self.pi_plus_hist_xF += numpy.load(foldername+'pi_plus_xF.npy')
    self.pi_minus_hist_xF += numpy.load(foldername+'pi_minus_xF.npy')
    self.K_plus_hist_xF += numpy.load(foldername+'K_plus_xF.npy')
    self.K_minus_hist_xF += numpy.load(foldername+'K_minus_xF.npy')

    self.p_hist_y += numpy.load(foldername+'proton_y.npy')
    self.p_bar_hist_y += numpy.load(foldername+'proton_bar_y.npy')
    self.n_hist_y +=numpy.load(foldername+'neutron_y.npy')
    self.lambda_hist_y += numpy.load(foldername+'lambda_y.npy')
    self.lambda_bar_hist_y += numpy.load(foldername+'lambda_bar_y.npy')
    self.pi_plus_hist_y += numpy.load(foldername+'pi_plus_y.npy')
    self.pi_minus_hist_y += numpy.load(foldername+'pi_minus_y.npy')
    self.K_plus_hist_y += numpy.load(foldername+'K_plus_y.npy')
    self.K_minus_hist_y += numpy.load(foldername+'K_minus_y.npy')

    #this is not really a pt histogramm
    #it is the summed up pt in every xF bin
    self.p_hist_pT += numpy.load(foldername+'proton_pT.npy')
    self.p_bar_hist_pT +=numpy.load(foldername+'proton_bar_pT.npy')
    self.n_hist_pT += numpy.load(foldername+'neutron_pT.npy')
    self.lambda_hist_pT += numpy.load(foldername+'lambda_pT.npy')
    self.lambda_bar_hist_pT += numpy.load(foldername+'lambda_bar_pT.npy')
    self.pi_plus_hist_pT += numpy.load(foldername+'pi_plus_pT.npy')
    self.pi_minus_hist_pT += numpy.load(foldername+'pi_minus_pT.npy')
    self.K_plus_hist_pT += numpy.load(foldername+'K_plus_pT.npy')
    self.K_minus_hist_pT += numpy.load(foldername+'K_minus_pT.npy')

    self.p_pT2 += numpy.load(foldername+'proton_pT2.npy')
    self.p_bar_pT2 +=numpy.load(foldername+'proton_bar_pT2.npy')
    self.n_pT2 += numpy.load(foldername+'neutron_pT2.npy')
    self.lambda_pT2 += numpy.load(foldername+'lambda_pT2.npy')
    self.lambda_bar_pT2 += numpy.load(foldername+'lambda_bar_pT2.npy')
    self.pi_plus_pT2 += numpy.load(foldername+'pi_plus_pT2.npy')
    self.pi_minus_pT2 += numpy.load(foldername+'pi_minus_pT2.npy')
    self.K_plus_pT2 += numpy.load(foldername+'K_plus_pT2.npy')
    self.K_minus_pT2 += numpy.load(foldername+'K_minus_pT2.npy')
    neventfile=open(foldername+'nevents.txt','r')
    self.nevents+=int(neventfile.read()[:-1])
    n_p_midrap_file=open(foldername+'n_protons_midrap','r')
    p_mT_file=open(foldername+'p_mT','r')
    p_mT2_file = open(foldername+'p_mT2','r')
    self.p_hist_mT+=float(p_mT_file.read()[:-1])
    self.p_mT2+=float(p_mT2_file.read()[:-1])
    self.n_p_midrap+=int(n_p_midrap_file.read()[:-1])
  def save_xF(self,filename,hist):
    binwidth=1.0/self.nbins
    err = numpy.sqrt(hist)
    normed_hist=hist/(binwidth*self.nevents)
    normed_err=err/(binwidth*self.nevents)
    numpy.save(filename+'_xF.npy',normed_hist)
    numpy.save(filename+'_xF_err.npy',normed_err)

  def save_y(self,filename,hist):
    binwidth=2*self.ymax/self.nbins #from -ymax to ymax
    err = numpy.sqrt(hist)
    normed_hist=hist/(binwidth*self.nevents)
    normed_err=err/(binwidth*self.nevents)
    numpy.save(filename+'_y.npy',normed_hist)
    numpy.save(filename+'_y_err.npy',normed_err)

  def save_pT(self,filename,pT_hist,pT2,xF_hist):
    mean_pT = pT_hist/xF_hist
    mean_pT2 = pT2/xF_hist
    mean_pT_err = numpy.sqrt((mean_pT2-mean_pT**2)/(xF_hist-1))
    numpy.save(filename+'_pT.npy',mean_pT)
    numpy.save(filename+'_pT_err.npy',mean_pT_err)

  def save_results(self,fname):
    foldername=fname+'plot_data/'
    self.save_xF(foldername+'p',self.p_hist_xF)
    self.save_xF(foldername+'p_bar',self.p_bar_hist_xF)
    self.save_xF(foldername+'n',self.n_hist_xF)
    self.save_xF(foldername+'lambda',self.lambda_hist_xF)
    self.save_xF(foldername+'lambda_bar',self.lambda_bar_hist_xF)
    self.save_xF(foldername+'pi_plus',self.pi_plus_hist_xF)
    self.save_xF(foldername+'pi_minus',self.pi_minus_hist_xF)
    self.save_xF(foldername+'K_plus',self.K_plus_hist_xF)
    self.save_xF(foldername+'K_minus',self.K_minus_hist_xF)

    self.save_y(foldername+'p',self.p_hist_y)
    self.save_y(foldername+'p_bar',self.p_bar_hist_y)
    self.save_y(foldername+'n',self.n_hist_y)
    self.save_y(foldername+'lambda',self.lambda_hist_y)
    self.save_y(foldername+'lambda_bar',self.lambda_bar_hist_y)
    self.save_y(foldername+'pi_plus',self.pi_plus_hist_y)
    self.save_y(foldername+'pi_minus',self.pi_minus_hist_y)
    self.save_y(foldername+'K_plus',self.K_plus_hist_y)
    self.save_y(foldername+'K_minus',self.K_minus_hist_y)

    self.save_pT(foldername+'p',self.p_hist_pT,self.p_pT2,self.p_hist_xF)
    self.save_pT(foldername+'p_bar',self.p_bar_hist_pT,self.p_bar_pT2,\
                                                       self.p_bar_hist_xF)
    self.save_pT(foldername+'n', self.n_hist_pT, self.n_pT2,self.n_hist_xF)
    self.save_pT(foldername+'lambda',self.lambda_hist_pT,self.lambda_pT2,\
                                                       self.lambda_hist_xF)
    self.save_pT(foldername+'lambda_bar',self.lambda_bar_hist_pT,\
                             self.lambda_bar_pT2,self.lambda_bar_hist_xF)
    self.save_pT(foldername+'pi_plus',self.pi_plus_hist_pT,\
                                  self.pi_plus_pT2, self.pi_plus_hist_xF)
    self.save_pT(foldername+'pi_minus',self.pi_minus_hist_pT,\
                            self.pi_minus_pT2,self.pi_minus_hist_xF)
    self.save_pT(foldername+'K_plus',self.K_plus_hist_pT,\
                                 self.K_plus_pT2,self.K_plus_hist_xF)
    self.save_pT(foldername+'K_minus',self.K_minus_hist_pT,
                      self.K_minus_pT2,self.K_minus_hist_xF)
    
    
    mean_mT = self.p_hist_mT/self.n_p_midrap
    mean_mT2 = self.p_mT2/self.n_p_midrap
    mT_err = (mean_mT2-mean_mT*mean_mT)/(self.n_p_midrap-1)
    output=open(foldername+'p_mean_mT','w')
    print >> output , mean_mT
    output2=open(foldername+'p_mean_mT_err','w')
    print >> output2, mT_err
nbins=20
sqrtsnn = sys.argv[1]
nfolders = int(sys.argv[2])
all_data=PlotData(nbins,sqrtsnn)
for i in range(1,nfolders+1):
  foldername=sys.argv[3]+str(i)+'/'
  all_data.read_folder(foldername)
all_data.save_results(sys.argv[3])
