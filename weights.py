#!/usr/bin/python

#targetlumi = 35867. # 1/pb
targetlumi = 36000. # 1/pb

# Number of processed MC events (before selections)
nRun={}
nRun['RSGM3000'] = 151093.
nRun['RSGM4000'] = 151076.
nRun['RSGM5000'] = 149820.

nRun['TTinc'] = 2873776.
nRun['TTinc0to1000'] = nRun['TTinc']
nRun['TTinc1000toInf'] = nRun['TTinc']*0.02474 + 24561633.
nRun['TTmtt1000toInf'] = 2334071.

nRun['QCDFlat'] = 7358392.
nRun['QCDmjj1000toInf']  = 3802314.

# Cross sections for MC samples (in pb)
xsec={}
xsec['RSGM3000'] = 0.1507
xsec['RSGM4000'] = 0.03617
xsec['RSGM5000'] = 0.01158

xsec['TTinc'] = 864.4
xsec['TTinc0to1000'] = xsec['TTinc']
xsec['TTinc1000toInf'] = xsec['TTinc']*0.02474 #(xsec*filtering coeff.)
xsec['TTmtt1000toInf'] = 21.27*0.0246 #(xsec*filtering coeff.) from McM

xsec['QCDFlat'] = 2207000000.
xsec['QCDmjj1000toInf'] = 1135.*0.0874 #(xsec*filtering coeff.) from McM

# Calculate lumi normalization weights
weight = {}
for sample in sorted(nRun.keys()): weight[sample] = (targetlumi*xsec[sample]) / (nRun[sample])
# for sample in sorted(nRun.keys()): print sample, weight[sample]
# weight['RSGM3000'] = 0.297252*0.12 # from Bibhu
# weight['RSGM4000'] = 0.0718248*0.12 # from Bibhu
# weight['RSGM5000'] = 0.0231878*0.12 # from Bibhu
# weight['TTinc'] = 90.2367*0.12 #from Bibhu
# weight['TTmtt1000toInf'] = 0.0672527*0.12 #from Bibhu
# weight['QCDFlat'] = 8.99789e+07*0.12 # from Bibhu
# weight['QCDmjj1000toInf'] = 7.82602*0.12 # from Bibhu 
# for sample in sorted(nRun.keys()): print sample, weight[sample]
