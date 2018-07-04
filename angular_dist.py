import numpy as np
import sys
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.size'] = 20
from matplotlib import pyplot as plt
from math import atan2 ,sqrt
class Particle():
  def __init__(s,line):
    line=line.split(' ')
    s.pdg = int(line[9])
    px = float(line[6])
    py = float(line[7])
    pz = float(line[8])
    s.theta = atan2(sqrt(px*px + py*py), pz)
  def is_proton(s):
    return s.pdg == 2212

class Interaction():
  def __init__(s,line):
    if int(line[-3:]) == 41: # soft string
      s.reactiontype = 'soft'
    elif int(line[-3:]) == 42: # hard string
      s.reactiontype = 'hard'
    else:
      s.reactiontype = 'other'
    s.n_in = int(line[17])
    s.n_out = int(line[23:25])
    s.n_lines_left = s.n_in + s.n_out
    s.incoming = []
    s.outgoing = []
    
  def add_line(s,line):
    s.n_lines_left -= 1
    if len(s.incoming) < s.n_in:
      s.incoming.append(Particle(line))
    elif len(s.outgoing) < s.n_out:
      s.outgoing.append(Particle(line))
    else:
      raise RuntimeError('More particles added to Interaction than declared')
    
  def is_complete(s):
    return s.n_lines_left == 0

class Actionlist():
  def __init__(s):
    s.soft_thetas = []
    s.soft_n_actions = 0
    s.hard_thetas = []
    s.hard_n_actions = 0
  def add_interaction(s,action):
    if not action.is_complete():
      raise RuntimeError('Incmplete interaction added to Actionlist')
    if action.reactiontype == 'soft':
      s.soft_n_actions += 1
      for particle in action.outgoing:
        if particle.is_proton():
          s.soft_thetas.append(particle.theta)
    elif action.reactiontype == 'hard':
      s.hard_n_actions += 1
      for particle in action.outgoing:
        if particle.is_proton():
          s.hard_thetas.append(particle.theta)
  @staticmethod
  def bins_hist(thetas,n_actions):
    hist,bins = np.histogram(thetas,bins=25)
    bincenter = (bins[:-1]+bins[1:])/2.0
    binwidth = bins[1:]-bins[:-1]
    err = np.sqrt(hist)/(n_actions*binwidth)
    hist = hist/(binwidth*n_actions)
    return hist,err,bincenter

  def make_theta_plot(s):
    h_hist,h_err,h_bins = s.bins_hist(s.hard_thetas,s.hard_n_actions)
    s_hist,s_err,s_bins = s.bins_hist(s.soft_thetas,s.soft_n_actions)
    fig=plt.figure()
    ax=fig.add_subplot('111')
    ax.errorbar(s_bins,s_hist,yerr=s_err,label='soft',lw=2)
    ax.errorbar(h_bins,h_hist,yerr=h_err,label='hard',lw=2)
    ax.set_title(r'$p+p\rightarrow p+X,\, \sqrt{s}=17.23\,\mathrm{GeV}$',fontsize=25)
    legend=ax.legend(loc='best')
    ax.set_xlabel(r'$\Theta$',fontsize=30)
    ax.set_ylabel(r'$dN/d\Theta$',fontsize=30)
    fig.subplots_adjust(bottom=0.15)
    plt.savefig('angular_distribution.pdf')

def read_file(filename):
  datafile=open(filename,'r')
  for line in datafile:
    if line[:13] == '# interaction': #beginning an interaction
      action = Interaction(line)
    elif line[0] != '#':
      action.add_line(line)
      if action.is_complete():
        actions.add_interaction(action)

actions = Actionlist()
for filename in sys.argv[1:]:
  read_file(filename)
actions.make_theta_plot()
