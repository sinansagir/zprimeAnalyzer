#!/usr/bin/python

import os,sys,time,math,datetime,pickle,itertools,getopt
from ROOT import TH1D,gROOT,TFile,TTree
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from numpy import linspace
from weights import *
from analyze import *
from samples import *
from utils import *

gROOT.SetBatch(1)
start_time = time.time()

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb
step1Dir = '/user_data/ssagir/HGCALLHCCTuples_v1_step0hadds/nominal'

"""
Note: 
--Each process in step1 (or step2) directories should have the root files hadded! 
--The code will look for <step1Dir>/<process>_hadd.root for nominal trees.
The uncertainty shape shifted files will be taken from <step1Dir>/../<shape>/<process>_hadd.root,
--Each process given in the lists below must have a definition in "samples.py"
--Check the set of cuts in "analyze.py"
"""

bkgList = ['TTmtt1000toInf','QCDmjj1000toInf']

dataList = ['Data']

whichSignal = 'RSG' #HTB, TT, BB, or X53X53
massList = range(3000,5000+1,1000)
sigList = [whichSignal+'M'+str(mass) for mass in massList]
decays = ['']

iPlot = 'RSGMass' #choose a discriminant from plotList below!
if len(sys.argv)>2: iPlot=sys.argv[2]
region = 'SR'
if len(sys.argv)>3: region=sys.argv[3]
isCategorized = 1
if len(sys.argv)>4: isCategorized=int(sys.argv[4])
doAllSys= False
doQ2sys = False
q2List  = [#energy scale sample to be processed
	       'TTJetsPHQ2U','TTJetsPHQ2D']
runData = True
runBkgs = True
runSigs = True

cutList = {'delYCut':1.0,'jet1PtCut':400,'jet2PtCut':400}

cutString  = 'DY'+str(cutList['delYCut'])+'_1jet'+str(int(cutList['jet1PtCut']))
cutString += '_2jet'+str(int(cutList['jet2PtCut']))

cTime=datetime.datetime.now()
datestr='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
timestr='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
pfix='templates_'
if not isCategorized: pfix='kinematics_'+region+'_'
pfix+=iPlot
pfix+='_TEST_'+datestr#+'_'+timestr
		
if len(sys.argv)>5: isEMlist=[str(sys.argv[5])]
else: isEMlist = ['LT','GT']
if len(sys.argv)>6: nttaglist=[str(sys.argv[6])]
else: nttaglist = ['0p']
if len(sys.argv)>7: nWtaglist=[str(sys.argv[7])]
else: nWtaglist=['0p']
if len(sys.argv)>8: nbtaglist=[str(sys.argv[8])]
else:
	nbtaglist=['0','1','2']
	if not isCategorized: nbtaglist = ['0p']
if len(sys.argv)>9: njetslist=[str(sys.argv[9])]
else: njetslist=['0p']

def readTree(file):
	if not os.path.exists(file): 
		print "Error: File does not exist! Aborting ...",file
		os._exit(1)
	tFile = TFile(file,'READ')
	tTree = tFile.Get('rsgluon')
	return tFile, tTree 

print "READING TREES"
shapesFiles = ['jec','jer']
tTreeData = {}
tFileData = {}
for data in dataList:
	if not runData: break
	print "READING:", data
	tFileData[data],tTreeData[data]=readTree(step1Dir+'/'+samples[data]+'_hadd.root')

tTreeSig = {}
tFileSig = {}
for sig in sigList:
	if not runSigs: break
	for decay in decays:
		print "READING:", sig+decay
		print "        nominal"
		tFileSig[sig+decay],tTreeSig[sig+decay]=readTree(step1Dir+'/'+samples[sig+decay]+'_hadd.root')
		if doAllSys:
			for syst in shapesFiles:
				for ud in ['Up','Down']:
					print "        "+syst+ud
					tFileSig[sig+decay+syst+ud],tTreeSig[sig+decay+syst+ud]=readTree(step1Dir.replace('nominal',syst.upper()+ud.lower())+'/'+samples[sig+decay]+'_hadd.root')

tTreeBkg = {}
tFileBkg = {}
for bkg in bkgList+q2List:
	if not runBkgs: break
	if bkg in q2List and not doQ2sys: continue
	print "READING:",bkg
	print "        nominal"
	tFileBkg[bkg],tTreeBkg[bkg]=readTree(step1Dir+'/'+samples[bkg]+'_hadd.root')
	if doAllSys:
		for syst in shapesFiles:
			for ud in ['Up','Down']:
				if bkg in q2List:
					tFileBkg[bkg+syst+ud],tTreeBkg[bkg+syst+ud]=None,None
				else:
					print "        "+syst+ud
					tFileBkg[bkg+syst+ud],tTreeBkg[bkg+syst+ud]=readTree(step1Dir.replace('nominal',syst.upper()+ud.lower())+'/'+samples[bkg]+'_hadd.root')
print "FINISHED READING"

#bigbins = [0,50,100,150,200,250,300,350,400,450,500,600,700,800,1000,1200,1500]
bigbins = [0,50,100,125,150,175,200,225,250,275,300,325,350,375,400,450,500,600,700,800,900,1000,1200,1400,1600,1800,2000,2500,3000,3500,4000,5000]

plotList = {#discriminantName:(discriminantNtupleName, binning, xAxisLabel)
	'nTrueInt':('nTrueInteractions_singleLepCalc',linspace(0, 75, 76).tolist(),';# true interactions'),
	'NPV'   :('npu',linspace(100, 300, 201).tolist(),';PV multiplicity'),
	'AK8NJets':('NumAK8Jets',linspace(0, 5, 6).tolist(),';AK8 jet multiplicity'),
	'AK8Jet1Eta':('Jet0Eta',linspace(-2.4, 2.4, 21).tolist(),';Lead AK8 Jet #eta'),
	'AK8Jet2Eta':('Jet1Eta',linspace(-2.4, 2.4, 21).tolist(),';Sublead AK8 Jet #eta'),
	'AK8Jet1Phi':('Jet0Phi',linspace(-4, 4, 21).tolist(),';Lead AK8 Jet #phi'),
	'AK8Jet2Phi':('Jet1Phi',linspace(-4, 4, 21).tolist(),';Sublead AK8 Jet #phi'),
	'AK8Jet1Pt':('Jet0Pt',linspace(0, 3000, 31).tolist(),';Lead AK8 Jet p_{T} [GeV]'),
	'AK8Jet2Pt':('Jet1Pt',linspace(0, 3000, 31).tolist(),';Sublead AK8 Jet p_{T} [GeV]'),
	'AK8Jet1M':('Jet0M',linspace(0, 500, 51).tolist(),';Lead AK8 Jet Mass [GeV]'),
	'AK8Jet2M':('Jet1M',linspace(0, 500, 51).tolist(),';Sublead AK8 Jet Mass [GeV]'),
	'AK8Jet1SDM':('Jet0SDmass',linspace(0, 500, 51).tolist(),';Lead AK8 Jet SD Mass [GeV]'),
	'AK8Jet2SDM':('Jet1SDmass',linspace(0, 500, 51).tolist(),';Sublead AK8 Jet SD Mass [GeV]'),
	'AK8Jet1SDMcorr':('Jet0SDmass*Jet0L2RelativeCorr',linspace(0, 500, 51).tolist(),';Lead AK8 Jet SD Mass [GeV]'),
	'AK8Jet2SDMcorr':('Jet1SDmass*Jet0L2RelativeCorr',linspace(0, 500, 51).tolist(),';Sublead AK8 Jet SD Mass [GeV]'),
	'AK8Jet1Tau32':('Jet0Tau3/Jet0Tau2',linspace(0, 1, 51).tolist(),';Lead AK8 Jet #tau_{3}/#tau_{2}'),
	'AK8Jet2Tau32':('Jet1Tau3/Jet1Tau2',linspace(0, 1, 51).tolist(),';Sublead AK8 Jet #tau_{3}/#tau_{2}'),
	'AK8Jet1Tau21':('Jet0Tau2/Jet0Tau1',linspace(0, 1, 51).tolist(),';Lead AK8 Jet #tau_{2}/#tau_{1}'),
	'AK8Jet2Tau21':('Jet1Tau2/Jet1Tau1',linspace(0, 1, 51).tolist(),';Sublead AK8 Jet #tau_{2}/#tau_{1}'),
	'AK8Jet1MaxSubbDisc':('Jet0SDmaxbdisc',linspace(0, 1, 51).tolist(),';Lead AK8 Jet Max Subjet b Disc.'),
	'AK8Jet2MaxSubbDisc':('Jet1SDmaxbdisc',linspace(0, 1, 51).tolist(),';Sublead AK8 Jet Max Subjet b Disc.'),
	'AK8Jet1Sub1bDisc':('Jet0SDsubjet0bdisc',linspace(0, 1, 51).tolist(),';Lead AK8 Jet Lead Subjet b Disc.'),
	'AK8Jet1Sub2bDisc':('Jet0SDsubjet1bdisc',linspace(0, 1, 51).tolist(),';Lead AK8 Jet Sublead Subjet b Disc.'),
	'AK8Jet2Sub1bDisc':('Jet1SDsubjet0bdisc',linspace(0, 1, 51).tolist(),';Sublead AK8 Jet Lead Subjet b Disc.'),
	'AK8Jet2Sub2bDisc':('Jet1SDsubjet1bdisc',linspace(0, 1, 51).tolist(),';Sublead AK8 Jet Sublead Subjet b Disc.'),
	'AK8Jet1Mult':('Jet0Mult',linspace(0, 1000, 201).tolist(),';Lead AK8 Jet Mult'),
	'AK8Jet2Mult':('Jet1Mult',linspace(0, 1000, 201).tolist(),';Sublead AK8 Jet Mult'),
	'AK8Jet1CHF':('Jet0CHF',linspace(0, 1, 51).tolist(),';Lead AK8 Jet CHF'),
	'AK8Jet2CHF':('Jet1CHF',linspace(0, 1, 51).tolist(),';Sublead AK8 Jet CHF'),

	'DRJ1J2':('deltaR',linspace(0, 5, 51).tolist(),';#DeltaR(j_{1}, j_{2})'),
	'DEtaJ1J2':('deltaEta',linspace(-5, 5, 101).tolist(),';#Delta#eta(j_{1}, j_{2})'),
	'DPhiJ1J2':('deltaPhi',linspace(-3.2, 3.2, 51).tolist(),';#Delta#phi(j_{1}, j_{2})'),
	'DYJ1J2':('deltaY',linspace(0, 2, 51).tolist(),';#DeltaY(j_{1}, j_{2})'),
	'RSGPt':('RSGPt',linspace(0, 1500, 31).tolist(),';p_{T}(t#bar{t}) [GeV]'),
	'RSGMass':('RSGMass',linspace(0, 6000, 121).tolist(),';M(t#bar{t}) [GeV]'),
	
	'MET'   :('corr_met_singleLepCalc',linspace(0, 1500, 51).tolist(),';#slash{E}_{T} [GeV]'),
	'PrunedSmeared' :('theJetAK8PrunedMass_JetSubCalc_PtOrdered',linspace(0, 500, 51).tolist(),';AK8 jet pruned mass [GeV]'),
	'PrunedSmearedNm1' :('theJetAK8PrunedMassWtagUncerts_JetSubCalc_PtOrdered',linspace(0, 500, 51).tolist(),';AK8 jet pruned mass [GeV]'),
	'SoftDropMass' :('theJetAK8SoftDropMass_JetSubCalc_PtOrdered',linspace(0, 500, 51).tolist(),';AK8 jet soft-drop mass [GeV]'),
	'SoftDropMassNm1' :('theJetAK8SoftDropMass_JetSubCalc_PtOrdered',linspace(0, 500, 51).tolist(),';AK8 jet soft-drop mass [GeV]'),
	'Tau1':('theJetAK8NjettinessTau1_JetSubCalc_PtOrdered',linspace(0,1,51).tolist(),';AK8 Jet #tau_{1}'),
	'Tau2':('theJetAK8NjettinessTau2_JetSubCalc_PtOrdered',linspace(0,1,51).tolist(),';AK8 Jet #tau_{2}'),
	'JetPhi':('theJetPhi_JetSubCalc_PtOrdered',linspace(-3.2,3.2,65).tolist(),';AK4 Jet #phi'),
	'JetPhiAK8':('theJetAK8Phi_JetSubCalc_PtOrdered',linspace(-3.2,3.2,65).tolist(),';AK8 Jet #phi'),
	
	'NJets_vs_NBJets':('NJets_JetSubCalc:NJetsCSV_JetSubCalc',linspace(0, 15, 16).tolist(),';AK4 jet multiplicity',linspace(0, 10, 11).tolist(),';b-tagged jet multiplicity'),

	}

print "PLOTTING:",iPlot
print "         Input Variable:",plotList[iPlot][0]
print "         X-AXIS TITLE  :",plotList[iPlot][2]
print "         BINNING USED  :",plotList[iPlot][1]

catList = list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist,njetslist))
nCats  = len(catList)

catInd = 1
for cat in catList:
 	if not runData: break
 	catDir = cat[0]+'_nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]+'_nJ'+cat[4]
 	catDir = catDir.replace('_nT0p','').replace('_nW0p','').replace('_nB0p','').replace('_nJ0p','')
 	datahists = {}
 	if len(sys.argv)>1: outDir=sys.argv[1]
 	else: 
		outDir = os.getcwd()
		outDir+='/'+pfix
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
		outDir+='/'+cutString
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
		outDir+='/'+catDir
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
 	category = {'isEM':cat[0],'nttag':cat[1],'nWtag':cat[2],'nbtag':cat[3],'njets':cat[4]}
 	for data in dataList: 
 		datahists.update(analyze(tTreeData,data,cutList,False,iPlot,plotList[iPlot],category))
 		if catInd==nCats: del tFileData[data]
 	pickle.dump(datahists,open(outDir+'/datahists_'+iPlot+'.p','wb'))
 	catInd+=1

catInd = 1
for cat in catList:
 	if not runBkgs: break
 	catDir = cat[0]+'_nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]+'_nJ'+cat[4]
 	catDir = catDir.replace('_nT0p','').replace('_nW0p','').replace('_nB0p','').replace('_nJ0p','')
 	bkghists  = {}
 	if len(sys.argv)>1: outDir=sys.argv[1]
 	else: 
		outDir = os.getcwd()
		outDir+='/'+pfix
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
		outDir+='/'+cutString
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
		outDir+='/'+catDir
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
 	category = {'isEM':cat[0],'nttag':cat[1],'nWtag':cat[2],'nbtag':cat[3],'njets':cat[4]}
 	for bkg in bkgList: 
 		bkghists.update(analyze(tTreeBkg,bkg,cutList,doAllSys,iPlot,plotList[iPlot],category))
 		if catInd==nCats: del tFileBkg[bkg]
 		if doAllSys and catInd==nCats:
 			for syst in shapesFiles:
 				for ud in ['Up','Down']: del tFileBkg[bkg+syst+ud]
 	if doQ2sys: 
 		for q2 in q2List: 
 			bkghists.update(analyze(tTreeBkg,q2,cutList,False,iPlot,plotList[iPlot],category))
 			if catInd==nCats: del tFileBkg[q2]
	pickle.dump(bkghists,open(outDir+'/bkghists_'+iPlot+'.p','wb'))
 	catInd+=1

catInd = 1
for cat in catList:
 	if not runSigs: break
 	catDir = cat[0]+'_nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]+'_nJ'+cat[4]
 	catDir = catDir.replace('_nT0p','').replace('_nW0p','').replace('_nB0p','').replace('_nJ0p','')
 	sighists  = {}
 	if len(sys.argv)>1: outDir=sys.argv[1]
 	else: 
		outDir = os.getcwd()
		outDir+='/'+pfix
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
		outDir+='/'+cutString
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
		outDir+='/'+catDir
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
 	category = {'isEM':cat[0],'nttag':cat[1],'nWtag':cat[2],'nbtag':cat[3],'njets':cat[4]}
 	for sig in sigList: 
 		for decay in decays: 
 			sighists.update(analyze(tTreeSig,sig+decay,cutList,doAllSys,iPlot,plotList[iPlot],category))
 			if catInd==nCats: del tFileSig[sig+decay]
 			if doAllSys and catInd==nCats:
 				for syst in shapesFiles:
 					for ud in ['Up','Down']: del tFileSig[sig+decay+syst+ud]
	pickle.dump(sighists,open(outDir+'/sighists_'+iPlot+'.p','wb'))
 	catInd+=1

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))

