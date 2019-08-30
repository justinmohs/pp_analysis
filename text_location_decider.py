class Location_decider:
  def __init__(s):
    s.particle = ''
    s.observable = ''
    s.special_positions = { 'y': {'p': [0.75, 0.05]},
                            'mpt': {'p': [0.05, 0.05],
                                    'pi_plus': [0.7,0.05]}
    }
    s.default_positions = {'y': [0.95, 0.5],
                           'mpt': [0.6, 0.05],
                           'xF': [0.05, 0.05]}

  def update_position(s):
    if not s.particle or not s.observable:
      return
    try:
      s.xpos, s.ypos = s.special_positions[s.observable][s.particle]
    except KeyError:
      s.xpos, s.ypos = s.default_positions[s.observable]

  def set_particle(s, particle):
    s.particle = particle
    s.update_position()

  def set_observable(s, observable):
    s.observable = observable
    s.update_position()

  def get_xpos(s):
    return s.xpos
  def get_ypos(s):
    return s.ypos
  def get_va(s):
    if s.ypos == 0.05:
      return 'bottom'
    elif s.ypos == 0.95 or s.ypos == 0.5:
      return 'top'
    else:
      print('Warning: unexpected ypos')
      return 'top'

  def get_ha(s):
    if s.xpos == 0.05 or s.xpos == 0.7:
      return 'left'
    elif s.xpos == 0.95 or s.xpos == 0.6 or s.xpos == 0.75:
      return 'right'
    else:
      print('Warning: unexpected xpos')
      return 'right'
