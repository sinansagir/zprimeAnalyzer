#!/usr/bin/python

targetlumi = 300000. # 1/pb

# Number of processed MC events (before selections)
nRun={}
nRun['ZpM4000'] = 445500. #N_gen=450k
nRun['ZpM6000'] = 444708. #N_gen=450k
nRun['ZpM8000'] = 445500. #N_gen=450k
nRun['ZpM10000']= 445599. #N_gen=450k
nRun['ZpM12000']= 445500. #N_gen=450k

nRun['ZpW1M2000'] = 250000. #N_gen=1M
nRun['ZpW1M4000'] = 250000. #N_gen=1M
nRun['ZpW1M6000'] = 300000. #N_gen=1M
nRun['ZpW1M8000'] = 350000. #N_gen=1M
nRun['ZpW1M10000']= 450000. #N_gen=1M

nRun['ZpW30M4000'] = 450000. #N_gen=450k
nRun['ZpW30M6000'] = 400000. #N_gen=400k
nRun['ZpW30M8000'] = 400000. #N_gen=400k
nRun['ZpW30M10000']= 400000. #N_gen=400k
nRun['ZpW30M12000']= 400000. #N_gen=400k

nRun['tt'] = 5100000. #N_gen=5,100,000
nRun['ttHT500to1000'] = 6100000. #N_gen=6,100,000
nRun['ttHT1000to2000'] = 6100000. #N_gen=6,100,000
nRun['ttHT2000to5000'] = 6100000. #N_gen=6,100,000
nRun['ttHT5000to10000'] = 6100000. #N_gen=6,100,000
nRun['ttHT10000to27000'] = 6090000. #N_gen=6,090,000

nRun['t123j'] = 1012128. #N_gen=3,362,345

nRun['Vj'] = 1000000. #N_gen=1,000,000 a.k.a. W+jets sample
nRun['VjHT500to1000'] = 6200000. #N_gen=6,200,000
nRun['VjHT1000to2000'] = 6200000. #N_gen=6,200,000
nRun['VjHT2000to5000'] = 6180000. #N_gen=6,180,000
nRun['VjHT5000to10000'] = 6160000. #N_gen=6,160,000
nRun['VjHT10000to27000'] = 6200000. #N_gen=6,200,000

nRun['ee'] = 1410010. #N_gen=1,410,010
nRun['eeHT500to1000'] = 6200000. #N_gen=6,200,000
nRun['eeHT1000to2000'] = 6200000. #N_gen=6,200,000
nRun['eeHT2000to5000'] = 5910000. #N_gen=5,910,000
nRun['eeHT5000to10000'] = 6190000. #N_gen=6,190,000
nRun['eeHT10000to27000'] = 6190000. #N_gen=6,190,000
nRun['mumu'] = 1000000. #N_gen=1,000,000
nRun['mumuHT500to1000'] = 6200000. #N_gen=6,200,000
nRun['mumuHT1000to2000'] = 6200000. #N_gen=6,200,000
nRun['mumuHT2000to5000'] = 6200000. #N_gen=6,200,000
nRun['mumuHT5000to10000'] = 6200000. #N_gen=6,200,000
nRun['mumuHT10000to27000'] = 6160000. #N_gen=6,160,000

nRun['VV'] = 985392. #N_gen=985,392
nRun['VVHT500to1000'] = 6190000. #N_gen=6,190,000
nRun['VVHT1000to2000'] = 5838411. #N_gen=5,838,411
nRun['VVHT2000to5000'] = 6200000. #N_gen=6,200,000
nRun['VVHT5000to10000'] = 6200000. #N_gen=6,200,000
nRun['VVHT10000to27000'] = 6200000. #N_gen=6,200,000

nRun['jj'] = 1000000. #N_gen=1,000,000
nRun['jjHT500to1000'] = 6180000. #N_gen=6,180,000
nRun['jjHT1000to2000'] = 6200000. #N_gen=6,200,000
nRun['jjHT2000to5000'] = 6190000. #N_gen=6,190,000
nRun['jjHT5000to10000'] = 6100000. #N_gen=6,100,000
nRun['jjHT10000to27000'] = 6100000. #N_gen=6,100,000

# Cross sections for MC samples (in pb)
xsec={}
xsec['ZpM4000'] = 1.#
xsec['ZpM6000'] = 1.#
xsec['ZpM8000'] = 1.#
xsec['ZpM10000']= 1.#
xsec['ZpM12000']= 1.#

xsec['ZpW1M2000'] = 1.#0.0001026
xsec['ZpW1M4000'] = 1.#8.007e-06
xsec['ZpW1M6000'] = 1.#1.692e-06
xsec['ZpW1M8000'] = 1.#8.325e-07
xsec['ZpW1M10000']= 1.#6.766e-07

xsec['ZpW30M4000'] = 1.#
xsec['ZpW30M6000'] = 1.#
xsec['ZpW30M8000'] = 1.#
xsec['ZpW30M10000']= 1.#
xsec['ZpW30M12000']= 1.#

# All background cross sections are (unless otherwise noted) from: http://fcc-physics-events.web.cern.ch/fcc-physics-events/LHEevents_helhc.php
xsec['tt'] = 11.09 
xsec['ttHT500to1000'] = 164.4
xsec['ttHT1000to2000'] = 10.72
xsec['ttHT2000to5000'] = 0.3235
xsec['ttHT5000to10000'] = 0.0008756
xsec['ttHT10000to27000'] = 1.214e-06

xsec['t123j'] = 1134.

xsec['Vj'] = 18.54
xsec['VjHT500to1000'] = 277.3
xsec['VjHT1000to2000'] = 18.03
xsec['VjHT2000to5000'] = 0.7608
xsec['VjHT5000to10000'] = 0.003244
xsec['VjHT10000to27000'] = 4.769e-06

xsec['ee'] = 0.000621
xsec['eeHT500to1000'] = 0.1267
xsec['eeHT1000to2000'] = 0.01034
xsec['eeHT2000to5000'] = 0.0006172
xsec['eeHT5000to10000'] = 2.603e-06
xsec['eeHT10000to27000'] = 6.65e-09
xsec['mumu'] = 0.000621
xsec['mumuHT500to1000'] = 0.1267
xsec['mumuHT1000to2000'] = 0.01034
xsec['mumuHT2000to5000'] = 0.0006172
xsec['mumuHT5000to10000'] = 2.603e-06
xsec['mumuHT10000to27000'] = 6.65e-09

xsec['VV'] = 0.1562
xsec['VVHT500to1000'] = 1.74
xsec['VVHT1000to2000'] = 0.1483
xsec['VVHT2000to5000'] = 0.008341
xsec['VVHT5000to10000'] = 4.367e-05
xsec['VVHT10000to27000'] = 7.496e-08

xsec['jj'] = 3871.
xsec['jjHT500to1000'] = 9.202e+04
xsec['jjHT1000to2000'] = 3966.
xsec['jjHT2000to5000'] = 118.
xsec['jjHT5000to10000'] = 0.3968
xsec['jjHT10000to27000'] = 0.0008586

# Calculate lumi normalization weights
weight = {}
for sample in sorted(nRun.keys()): weight[sample] = (targetlumi*xsec[sample]) / (nRun[sample])
# for sample in sorted(nRun.keys()): print sample, weight[sample]
