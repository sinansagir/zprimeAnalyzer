#!/usr/bin/python

targetlumi = 300000. # 1/pb

# Number of processed MC events (before selections)
nRun={}
nRun['ZpM2000'] = 50000. #N_gen=1M
nRun['ZpM4000'] = 50000. #N_gen=1M
nRun['ZpM6000'] = 49000. #N_gen=1M
nRun['ZpM8000'] = 49000. #N_gen=1M
nRun['ZpM10000']= 49000. #N_gen=1M

nRun['TTinc'] = 264263150 #N_gen= --->>tobeupdated

nRun['t123j'] = 1012128. #N_gen=3,362,345

nRun['VJ'] = 1000000. #N_gen=1,000,000 a.k.a. W+jets sample

nRun['ee'] = 1410010. #N_gen=1,410,010
nRun['eeHT500to1000'] = 6200000. #N_gen=6,200,000
nRun['eeHT1000to2000'] = 6200000. #N_gen=6,200,000
nRun['eeHT2000to5000'] = 5910000. #N_gen=5,910,000
nRun['eeHT5000to10000'] = 6190000. #N_gen=6,190,000
nRun['eeHT10000to27000'] = 6190000. #N_gen=6,190,000
nRun['mumu'] = 1000000. #N_gen=1,000,000

nRun['VV'] = 985392. #N_gen=985,392

nRun['jj'] = 1000000. #N_gen=1,000,000

# Cross sections for MC samples (in pb)
xsec={}
xsec['ZpM2000'] = 1.#0.0001026
xsec['ZpM4000'] = 1.#8.007e-06
xsec['ZpM6000'] = 1.#1.692e-06
xsec['ZpM8000'] = 1.#8.325e-07
xsec['ZpM10000']= 1.#6.766e-07

xsec['TTinc'] = 864.6 # --->>tobeupdated

xsec['t123j'] = 11.14 # --->>tobeupdated

xsec['VJ'] = 18.54 #http://fcc-physics-events.web.cern.ch/fcc-physics-events/LHEevents_helhc.php

xsec['ee'] = 0.000621 #http://fcc-physics-events.web.cern.ch/fcc-physics-events/LHEevents_helhc.php
xsec['eeHT500to1000'] = 0.1267 #http://fcc-physics-events.web.cern.ch/fcc-physics-events/LHEevents_helhc.php
xsec['eeHT1000to2000'] = 0.01034 #http://fcc-physics-events.web.cern.ch/fcc-physics-events/LHEevents_helhc.php
xsec['eeHT2000to5000'] = 0.0006172 #http://fcc-physics-events.web.cern.ch/fcc-physics-events/LHEevents_helhc.php
xsec['eeHT5000to10000'] = 2.603e-06 #http://fcc-physics-events.web.cern.ch/fcc-physics-events/LHEevents_helhc.php
xsec['eeHT10000to27000'] = 6.65e-09 #http://fcc-physics-events.web.cern.ch/fcc-physics-events/LHEevents_helhc.php
xsec['mumu'] = 0.000621 #http://fcc-physics-events.web.cern.ch/fcc-physics-events/LHEevents_helhc.php

xsec['VV'] = 0.1562 #http://fcc-physics-events.web.cern.ch/fcc-physics-events/LHEevents_helhc.php
 
xsec['jj'] = 3871. #http://fcc-physics-events.web.cern.ch/fcc-physics-events/LHEevents_helhc.php

# Calculate lumi normalization weights
weight = {}
for sample in sorted(nRun.keys()): weight[sample] = (targetlumi*xsec[sample]) / (nRun[sample])
# for sample in sorted(nRun.keys()): print sample, weight[sample]
