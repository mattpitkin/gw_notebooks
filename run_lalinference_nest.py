#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run lalinference_nest on GW170817 searching over coalescence time and distance.
"""

import os
import subprocess as sp
import numpy as np

# L1 frame file (2048 seconds) - peak of waveform is at 1842.43 seconds ± 30 msec
# sample rate of 4096 Hz
framefile = 'L-L1_LOSC_CLN_4_V1-1187007040-2048.gwf'

# create cache file
cache = 'L L1_LOSC_CLN_4_V1 1187007040 2048 file://localhost{}/{}'.format(os.getcwd(), framefile)
cachefile = os.path.join(os.getcwd(), 'L1cache.lcf')
fp = open(cachefile, 'w')
fp.write(cache+'\n')
fp.close()

m1 = 1.72140419742
m2 = 1.1085929782

chirpmass = (m1*m2)**(3./5.)/(m1+m2)**(1./5.)
q = m2/m1

commands = {
  # detector
  '--ifo': 'L1',
  # PSD estimation
  '--psdstart': '1187007040',
  '--psdlength': '2048',      # use all of the frame data for PSD estimation
  '--seglen': '106.66666666666667',          # average 106.666666666666 second chunks of data
  # trigger info
  '--trigtime': '{}'.format(1187007040.0+1842.43), # time of trigger (data segment for analysing will start seglen-2 second before this time)
  '--L1-flow': '24', # start at 24 Hz
  '--L1-fhigh': '400', # go up to 400 Hz
  # frame data
  '--L1-cache': cachefile,
  '--L1-channel': 'L1:LOSC-STRAIN', # strain channel in frame
  '--srate': '4096', # sample rate
  # prior ranges
  '--dt': '0.2', # range around trigger time for tc
  '--distance-min': '10',  # minimum distance
  '--distance-max': '100', # maximum distance
  # Nested sampling parameters
  '--Nlive': '2048', # number of live points
  '--Nmcmcinitial': '1000',
  '--progress': '',
  '--outfile': 'results.hdf',
  # waveform setting
  '--approx': 'IMRPhenomPv2',
  '--fref': '100', # reference frequency
  '--modeldomain': 'frequency',
  '--amporder': '0',
  # fix parameters
  '--fix-chirpmass': '{}'.format(chirpmass), # chirp mass
  '--fix-q': '{}'.format(q), # mass ratio
  '--fix-rightascension': '3.446157844',
  '--fix-declination': '-0.4080841591',
  '--fix-phase': '2.60174675393',
  '--fix-costheta_jn': '{}'.format(np.cos(2.74719229269)), # cos(theta_jn)
  '--fix-a_spin1': '0.264813928565',
  '--fix-a_spin2': '0.702414508316',
  '--fix-tilt_spin1': '2.58869030589',
  '--fix-tilt_spin2': '0.948965945788',
  '--fix-phi_jl': '6.04852924541',
  '--fix-phi12': '4.81306908412',
  '--fix-polarisation': '0.860990548555'
}

execfile = '/home/matthew/.local/share/virtualenvs/master-aVPqGZEW/bin/lalinference_nest'

commandcall = [execfile]
for key, value in commands.items():
    commandcall.append(key)
    commandcall.append(value)

print(' '.join(commandcall))

p = sp.Popen(' '.join(commandcall), stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
err, out = p.communicate()

print(out)
print(err)
