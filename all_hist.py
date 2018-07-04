import sys
import numpy
from math import sqrt

class Particle:
  def __init__(self,dataline):
    line=dataline.split(' ')
    self.pdg=line[9]
    self.E=float(line[5])
    self.px=float(line[6])
    self.py=float(line[7])
    self.pz=float(line[8])
  
  def xF(self,pzmax):
    return abs(self.pz)/pzmax

  def mT(self):
    return sqrt(self.pT2()+0.938*0.938)

  def mT2(self):
    return self.pT2() + 0.938*0.938

  def y(self):
    return 0.5*numpy.log((self.E+self.pz)/(self.E-self.pz))

  def pT2(self):
    return self.px*self.px + self.py*self.py

  def in_rap_intervall(self):
    y=self.y()
    return (-0.4<y and y<-0.2)

  def pT(self):
    return sqrt(self.px*self.px + self.py*self.py)

class Eventdata:
  def __init__(self,nbins,pz_beam,rapidity_range_factor = 1.2):
    self.pz_beam=pz_beam
    self.nbins = nbins
    self.xF_binwidth = 1.0/nbins
    E_beam = sqrt(pz_beam*pz_beam + 0.938*0.938)
    self.y_beam = 0.5 * numpy.log((E_beam + pz_beam)/(E_beam - pz_beam))
    self.ymax = self.y_beam * rapidity_range_factor
    self.y_binwidth = 2.0*self.ymax/nbins

    self.n_p = 0
    self.n_n =0
    self.n_p_bar = 0
    self.n_lambda = 0
    self.n_lambda_bar = 0
    self.n_pi_plus = 0
    self.n_pi_minus = 0
    self.n_K_plus = 0
    self.n_K_minus = 0
    self.n_other_particles= 0
    
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

    #this is not really a pt histogramm
    #it is the summed up pt^2 in every xF bin
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
    self.np_midrap=0

  def update_hists(self,xF_hist, y_hist, pT_hist,pT2, particle):
    ''' calling histogramms by reference to update them i hope
    '''
    #update dN/dxF(xF) and <pT>(xF) (actually sum pT)
    pT=particle.pT()
    xF=particle.xF(self.pz_beam)
    y=particle.y()
    if xF >= 1:
      print [xF,particle.pdg]
      #xF_hist[self.nbins-1]+=1
      #pT_hist[self.nbins-1]+=pT
      #pT2[self.nbins-1]+=pT*pT
    else: 
      xF_hist[xF/self.xF_binwidth]+=1
      pT_hist[xF/self.xF_binwidth]+= pT
      pT2[xF/self.xF_binwidth]+=pT*pT
    if abs(y) < self.ymax:
      y_hist[int((y+self.ymax)/self.y_binwidth)]+=1
    

  def add_particle(self,particle):
    if particle.pdg == '2212': #Proton
      self.update_hists(self.p_hist_xF,self.p_hist_y,self.p_hist_pT\
                                               ,self.p_pT2,particle)
      if particle.in_rap_intervall(): 
        self.p_hist_mT+=particle.mT()
        self.p_mT2+=particle.mT2()
        self.np_midrap+=1
      self.n_p+=1
    elif particle.pdg == '-2212': #Anti-Proton
      self.update_hists(self.p_bar_hist_xF, self.p_bar_hist_y,\
                        self.p_bar_hist_pT,self.p_bar_pT2, particle)
      self.n_p_bar+=1
    elif particle.pdg == '2112': #neutron
      self.update_hists(self.n_hist_xF, self.n_hist_y,\
                        self.n_hist_pT, self.n_pT2, particle)
      self.n_n+=1
    elif particle.pdg == '3212': #Lambda
      self.update_hists(self.lambda_hist_xF,self.lambda_hist_y,\
                        self.lambda_hist_pT,self.lambda_pT2,particle)
      self.n_lambda+=1
    elif particle.pdg == '-3212': #Anti-Lambda
      self.update_hists(self.lambda_bar_hist_xF,self.lambda_bar_hist_y,\
                        self.lambda_bar_hist_pT,self.lambda_bar_pT2,particle)
      self.n_lambda_bar+=1
    elif particle.pdg == '211': #Pi+
      self.update_hists(self.pi_plus_hist_xF,self.pi_plus_hist_y,\
                        self.pi_plus_hist_pT,self.pi_plus_pT2,particle)
      self.n_pi_plus+=1
    elif particle.pdg == '-211': #Pi-
      self.update_hists(self.pi_minus_hist_xF,self.pi_minus_hist_y,\
                        self.pi_minus_hist_pT,self.pi_minus_pT2,particle)
      self.n_pi_minus+=1
    elif particle.pdg == '321': #K+
      self.update_hists(self.K_plus_hist_xF,self.K_plus_hist_y,\
                        self.K_plus_hist_pT,self.K_plus_pT2,particle)
      self.n_K_plus+=1
    elif particle.pdg == '-321': #K-
      self.update_hists(self.K_minus_hist_xF,self.K_minus_hist_y,\
                        self.K_minus_hist_pT,self.K_minus_pT2,particle)
      self.n_K_minus+=1

  def is_nontrivial(self):
    n_particles = self.n_p + self.n_p_bar + self.n_lambda + self.n_lambda_bar\
                + self.n_pi_plus + self.n_pi_minus + self.n_K_plus\
                + self.n_K_minus + self.n_other_particles
    if n_particles>2:
      return True
    if n_particles == 2 and self.n_p!=2:
      return True
    return False

  def add_other_particle(self):
    self.n_other_particles += 1

class Smash_run:
  def __init__(self,nbins):
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

    #this is not really a pt histogramm
    #it is the summed up pt^2 in every xF bin
    self.p_pT2 = numpy.zeros(nbins)
    self.p_bar_pT2 = numpy.zeros(nbins)
    self.n_pT2 = numpy.zeros(nbins)
    self.lambda_pT2 = numpy.zeros(nbins)
    self.lambda_bar_pT2 = numpy.zeros(nbins)
    self.pi_plus_pT2 = numpy.zeros(nbins)
    self.pi_minus_pT2 = numpy.zeros(nbins)
    self.K_plus_pT2 = numpy.zeros(nbins)
    self.K_minus_pT2 = numpy.zeros(nbins)

    self.p_hist_mT = 0
    self.p_mT2 =  0
    self.np_midrap = 0


  def add_event(self,event):
    self.p_hist_xF += event.p_hist_xF
    self.p_bar_hist_xF += event.p_bar_hist_xF
    self.n_hist_xF += event.n_hist_xF
    self.lambda_hist_xF += event.lambda_hist_xF
    self.lambda_bar_hist_xF += event.lambda_bar_hist_xF
    self.pi_plus_hist_xF += event.pi_plus_hist_xF
    self.pi_minus_hist_xF += event.pi_minus_hist_xF
    self.K_plus_hist_xF += event.K_plus_hist_xF
    self.K_minus_hist_xF += event.K_minus_hist_xF

    self.p_hist_y += event.p_hist_y
    self.p_bar_hist_y += event.p_bar_hist_y
    self.n_hist_y += event.n_hist_y
    self.lambda_hist_y += event.lambda_hist_y
    self.lambda_bar_hist_y += event.lambda_bar_hist_y
    self.pi_plus_hist_y += event.pi_plus_hist_y
    self.pi_minus_hist_y += event.pi_minus_hist_y
    self.K_plus_hist_y += event.K_plus_hist_y
    self.K_minus_hist_y += event.K_minus_hist_y

    #this is not really a pt histogramm
    #it is the summed up pt in every xF bin
    self.p_hist_pT += event.p_hist_pT
    self.p_bar_hist_pT += event.p_bar_hist_pT
    self.n_hist_pT += event.n_hist_pT
    self.lambda_hist_pT += event.lambda_hist_pT
    self.lambda_bar_hist_pT += event.lambda_bar_hist_pT
    self.pi_plus_hist_pT += event.pi_plus_hist_pT
    self.pi_minus_hist_pT += event.pi_minus_hist_pT
    self.K_plus_hist_pT += event.K_plus_hist_pT
    self.K_minus_hist_pT += event.K_minus_hist_pT
    
    self.p_pT2 += event.p_pT2
    self.p_bar_pT2 += event.p_bar_pT2
    self.n_pT2 += event.n_pT2
    self.lambda_pT2 += event.lambda_pT2
    self.lambda_bar_pT2 += event.lambda_bar_pT2
    self.pi_plus_pT2 += event.pi_plus_pT2
    self.pi_minus_pT2 += event.pi_minus_pT2
    self.K_plus_pT2 += event.K_plus_pT2
    self.K_minus_pT2 += event.K_minus_pT2

    self.p_hist_mT+=event.p_hist_mT
    self.p_mT2 += event.p_mT2
    self.np_midrap+=event.np_midrap
    self.nevents+=1

  def save_results(self,foldername):
    output=open(sys.argv[1]+'/nevents.txt','w')
    print >> output, self.nevents
    mT_output=open(sys.argv[1]+'/p_mT','w')
    mT2_output=open(sys.argv[1]+'/p_mT2','w')
    print >> mT_output, self.p_hist_mT
    print >> mT2_output, self.p_mT2
    np_midrap_file=open(sys.argv[1]+'/n_protons_midrap','w')
    print >> np_midrap_file, self.np_midrap

    numpy.save(foldername+'/proton_xF',self.p_hist_xF)
    numpy.save(foldername+'/proton_bar_xF',self.p_bar_hist_xF)
    numpy.save(foldername+'/neutron_xF',self.n_hist_xF)
    numpy.save(foldername+'/lambda_xF',self.lambda_hist_xF)
    numpy.save(foldername+'/lambda_bar_xF',self.lambda_bar_hist_xF)
    numpy.save(foldername+'/pi_plus_xF', self.pi_plus_hist_xF)
    numpy.save(foldername+'/pi_minus_xF', self.pi_minus_hist_xF)
    numpy.save(foldername+'/K_plus_xF',self.K_plus_hist_xF)
    numpy.save(foldername+'/K_minus_xF',self.K_minus_hist_xF)
    
    numpy.save(foldername+'/proton_pT',self.p_hist_pT)
    numpy.save(foldername+'/proton_bar_pT',self.p_bar_hist_pT)
    numpy.save(foldername+'/neutron_pT', self.n_hist_pT)
    numpy.save(foldername+'/lambda_pT',self.lambda_hist_pT)
    numpy.save(foldername+'/lambda_bar_pT',self.lambda_bar_hist_pT)
    numpy.save(foldername+'/pi_plus_pT', self.pi_plus_hist_pT)
    numpy.save(foldername+'/pi_minus_pT', self.pi_minus_hist_pT)
    numpy.save(foldername+'/K_plus_pT',self.K_plus_hist_pT)
    numpy.save(foldername+'/K_minus_pT',self.K_minus_hist_pT)

    numpy.save(foldername+'/proton_pT2',self.p_pT2)
    numpy.save(foldername+'/proton_bar_pT2',self.p_bar_pT2)
    numpy.save(foldername+'/neutron_pT2',self.n_pT2)
    numpy.save(foldername+'/lambda_pT2',self.lambda_pT2)
    numpy.save(foldername+'/lambda_bar_pT2',self.lambda_bar_pT2)
    numpy.save(foldername+'/pi_plus_pT2',self.pi_plus_pT2)
    numpy.save(foldername+'/pi_minus_pT2',self.pi_minus_pT2)
    numpy.save(foldername+'/K_plus_pT2',self.K_plus_pT2)
    numpy.save(foldername+'/K_minus_pT2',self.K_minus_pT2)

    numpy.save(foldername+'/proton_y',self.p_hist_y)
    numpy.save(foldername+'/proton_bar_y',self.p_bar_hist_y)
    numpy.save(foldername+'/neutron_y',self.n_hist_y)
    numpy.save(foldername+'/lambda_y',self.lambda_hist_y)
    numpy.save(foldername+'/lambda_bar_y',self.lambda_bar_hist_y)
    numpy.save(foldername+'/pi_plus_y', self.pi_plus_hist_y)
    numpy.save(foldername+'/pi_minus_y', self.pi_minus_hist_y)
    numpy.save(foldername+'/K_plus_y',self.K_plus_hist_y)
    numpy.save(foldername+'/K_minus_y',self.K_minus_hist_y)
    
nbins=20
full_smash_run=Smash_run(nbins)
sqrtsnn = float(sys.argv[2])
pzmax = sqrt(sqrtsnn*sqrtsnn/4.0 -0.938*0.938)
particles_of_interest= ['2212', '-2212','3212','-3212','211','-211','321','-321']
try:
  datafile=open(sys.argv[1]+'/particle_lists.oscar')
except IOError:
  datafile=open(sys.argv[1]+'/particle_lists.oscar.unfinished')
  print 'WARNING: USING UNFINISHED SMASH OUTPUT'
current_event = Eventdata(nbins,pzmax)
for line in datafile:
  if line[0] == '#': #end of event
    if current_event.is_nontrivial():
      full_smash_run.add_event(current_event)
      current_event = Eventdata(nbins,pzmax) #override event with empty event
    continue
  
  dataline=line.split(' ')
  pdg=dataline[9]
  if pdg in particles_of_interest:
    current_particle=Particle(line)
    current_event.add_particle(current_particle)
  else:
    current_event.add_other_particle()
full_smash_run.save_results(sys.argv[1])
