#!/usr/bin/python

#targetlumi = 35867. # 1/pb
targetlumi = 300000. # 1/pb

# Number of processed MC events (before selections)
nRun={}
nRun['ZpM2000'] = 399988. #N_gen=400k
nRun['ZpM3000'] = 399992. #N_gen=400k
nRun['ZpM4000'] = 399990. #N_gen=400k
nRun['ZpM5000'] = 399989. #N_gen=400k
nRun['ZpM6000'] = 399987. #N_gen=400k

filterEffTTbar = 0.0246 #21.27/864.4
nRun['TTinc'] = 269205951 #N_gen=270M (original~50M+ext1~220M) # there seems to be a duplication of events that is being checked!!!
nRun['TTmtt0to1000inc'] = nRun['TTinc']
nRun['TTmtt1000toInfinc'] = nRun['TTinc']*filterEffTTbar+12769661. #N_gen=12,770,210
nRun['TTmtt1000toInf'] = nRun['TTmtt1000toInfinc']#12769661.

nRun['STs'] = 7376778. #N_gen=5,877,000(v1)+1,500,000(v2)
nRun['STt'] = 66141783. #N_gen=59,759,100 #missing 5/2182 files
nRun['STbt']= 5253355. #N_gen=39,792,299 #missing 2/177 files
nRun['STtW'] = 14540191. #N_gen=11,839,000
nRun['STbtW'] = 14955459. #N_gen=12,000,000

nRun['WJetsInc'] = 149042577. #N_gen=151,958,925 #missing 35/3566 files

nRun['DyHT70to100'] = 19096772. #N_gen=19,098,098
nRun['DyHT100to200'] = 19311172. #N_gen=19,312,573
nRun['DyHT200to400'] = 10625680. #N_gen=10,653,173
nRun['DyHT400to600'] = 10161396. #N_gen=10,174,397
nRun['DyHT600to800'] = 9966447. #N_gen=9,967,183
nRun['DyHT800to1200'] = 9411932. #N_gen=9,412,655
nRun['DyHT1200to2500'] = 4588584. #N_gen=4,653,394 #missing 1/82 files
nRun['DyHT2500toInf'] = 3091458. #N_gen=3,091,754

nRun['WW'] = 99127796. #N_gen=100,000,000 #missin 15/2219 files

nRun['QCDPt50to80'] = 1999953. #N_gen=2,000,000
nRun['QCDPt80to120'] = 2999927. #N_gen=3,000,000
nRun['QCDPt120to170'] = 2910426. #N_gen=3,000,000
nRun['QCDPt170to300'] = 2999931. #N_gen=3,000,000
nRun['QCDPt300to470'] = 39642166. #N_gen=4,000,000
nRun['QCDPt470to600'] = 7999775. #N_gen=8,000,000
nRun['QCDPt600to800'] = 7999789. #N_gen=8,000,000
nRun['QCDPt800to1000'] = 7791003. #N_gen=3,000,000
nRun['QCDPt1000toInf'] = 999975. #N_gen=1,000,000

filterEffQCD = 0.0874 #from McM
nRun['QCDPt15to7000'] = 199376610. #N_gen=200,000,000 #missing 16/5406 files
nRun['QCDflatPt15to7000'] = 29951843. #N_gen=29,984,274
nRun['QCDmjj0to1000inc'] = nRun['QCDflatPt15to7000']
nRun['QCDmjj1000toInfinc'] = nRun['QCDflatPt15to7000']*filterEffQCD+19713175. #N_gen=20,391,603
nRun['QCDmjj1000toInf'] = nRun['QCDmjj1000toInfinc']#19713175.

# Cross sections for MC samples (in pb)
xsec={}
xsec['ZpM2000'] = 1.#1.153e+0
xsec['ZpM3000'] = 1.#1.556e-01
xsec['ZpM4000'] = 1.#3.585e-02
xsec['ZpM5000'] = 1.#1.174e-02
xsec['ZpM6000'] = 1.#4.939e-03

xsec['TTinc'] = 864.6 #from https://docs.google.com/spreadsheets/d/1Oz8rWBoPJInKoy4_QyT0BArO9VnMe7AeyikUE09h2O0/edit#gid=0
xsec['TTmtt0to1000inc'] = xsec['TTinc']
xsec['TTmtt1000toInfinc'] = xsec['TTinc']*filterEffTTbar#21.27 #(xsec*filtering coeff.) from McM
xsec['TTmtt1000toInf'] = xsec['TTinc']*filterEffTTbar#21.27 #(xsec*filtering coeff.) from McM

xsec['STs'] = 11.14
xsec['STt'] = 48.03
xsec['STbt']= 29.2
xsec['STtW'] = 45.06
xsec['STbtW'] = 45.02

xsec['WJetsInc'] = 60520. #from https://docs.google.com/spreadsheets/d/1Oz8rWBoPJInKoy4_QyT0BArO9VnMe7AeyikUE09h2O0/edit#gid=0

xsec['DyHT70to100'] = 161.6*1.23
xsec['DyHT100to200'] = 150*1.23
xsec['DyHT200to400'] = 32.95*1.23
xsec['DyHT400to600'] = 3.911*1.23
xsec['DyHT600to800'] = 0.8301*1.23
xsec['DyHT800to1200'] = 0.3852*1.23
xsec['DyHT1200to2500'] = 0.08874*1.23
xsec['DyHT2500toInf'] = 0.001755*1.23

xsec['WW'] = 3.423
    
xsec['QCDPt50to80'] = 21870000. #from https://docs.google.com/spreadsheets/d/1Oz8rWBoPJInKoy4_QyT0BArO9VnMe7AeyikUE09h2O0/edit#gid=0
xsec['QCDPt80to120'] = 3063000. #from https://docs.google.com/spreadsheets/d/1Oz8rWBoPJInKoy4_QyT0BArO9VnMe7AeyikUE09h2O0/edit#gid=0
xsec['QCDPt120to170'] = 541100. #from https://docs.google.com/spreadsheets/d/1Oz8rWBoPJInKoy4_QyT0BArO9VnMe7AeyikUE09h2O0/edit#gid=0
xsec['QCDPt170to300'] = 137100. #from https://docs.google.com/spreadsheets/d/1Oz8rWBoPJInKoy4_QyT0BArO9VnMe7AeyikUE09h2O0/edit#gid=0
xsec['QCDPt300to470'] = 9325. #from https://docs.google.com/spreadsheets/d/1Oz8rWBoPJInKoy4_QyT0BArO9VnMe7AeyikUE09h2O0/edit#gid=0
xsec['QCDPt470to600'] = 809.7 #from https://docs.google.com/spreadsheets/d/1Oz8rWBoPJInKoy4_QyT0BArO9VnMe7AeyikUE09h2O0/edit#gid=0
xsec['QCDPt600to800'] = 231.8 #from https://docs.google.com/spreadsheets/d/1Oz8rWBoPJInKoy4_QyT0BArO9VnMe7AeyikUE09h2O0/edit#gid=0
xsec['QCDPt800to1000'] = 42.51 #from https://docs.google.com/spreadsheets/d/1Oz8rWBoPJInKoy4_QyT0BArO9VnMe7AeyikUE09h2O0/edit#gid=0
xsec['QCDPt1000toInf'] = 14.08 #from https://docs.google.com/spreadsheets/d/1Oz8rWBoPJInKoy4_QyT0BArO9VnMe7AeyikUE09h2O0/edit#gid=0

xsec['QCDPt15to7000'] = 2190000000.
xsec['QCDflatPt15to7000'] = 2207000000.
xsec['QCDmjj0to1000inc'] = xsec['QCDflatPt15to7000']
xsec['QCDmjj1000toInfinc'] = 1174. #(xsec*filtering coeff.) from McM
xsec['QCDmjj1000toInf'] = 1174. #(xsec*filtering coeff.) from McM

# Calculate lumi normalization weights
weight = {}
for sample in sorted(nRun.keys()): weight[sample] = (targetlumi*xsec[sample]) / (nRun[sample])
# for sample in sorted(nRun.keys()): print sample, weight[sample]
