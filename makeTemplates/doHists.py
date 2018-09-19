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
step1Dir = '/user_data/ssagir/CMSSW_7_4_7/src/zprimeAnalyzer/singLep/inputFiles_18_8_17'

"""
Note: 
--Each process in step1 (or step2) directories should have the root files hadded! 
--The code will look for <step1Dir>/<process>_hadd.root for nominal trees.
The uncertainty shape shifted files will be taken from <step1Dir>/../<shape>/<process>_hadd.root,
--Each process given in the lists below must have a definition in "samples.py"
--Check the set of cuts in "analyze.py"
"""

bkgList = [
'TTinc','TTmtt1000toInf','TTmtt0to1000inc','TTmtt1000toInfinc',
'STs','STt','STbt','STtW','STbtW',
'WJetsInc',
'DyHT70to100','DyHT100to200','DyHT200to400','DyHT400to600','DyHT600to800','DyHT800to1200','DyHT1200to2500','DyHT2500toInf',
'WW',
'QCDPt15to7000',
'QCDflatPt15to7000',
'QCDmjj1000toInf',#'QCDmjj0to1000inc','QCDmjj1000toInfinc',
'QCDPt50to80','QCDPt80to120','QCDPt120to170','QCDPt170to300','QCDPt300to470','QCDPt470to600','QCDPt600to800','QCDPt800to1000','QCDPt1000toInf',
]

dataList = ['Data']

whichSignal = 'Zp' #HTB, TT, BB, or X53X53
massList = range(2000,6000+1,1000)
sigList = [whichSignal+'M'+str(mass) for mass in massList]
decays = ['']

iPlot = 'zpMass' #choose a discriminant from plotList below!
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
pfix+='_'+datestr#+'_'+timestr
		
if len(sys.argv)>5: isEMlist=[str(sys.argv[5])]
else: isEMlist = ['E','M']
if len(sys.argv)>6: nttaglist=[str(sys.argv[6])]
else: nttaglist = ['0','1']
if len(sys.argv)>7: nWtaglist=[str(sys.argv[7])]
else: nWtaglist=['0p']
if len(sys.argv)>8: nbtaglist=[str(sys.argv[8])]
else:
	nbtaglist=['0','1']#,'2']
	if not isCategorized: nbtaglist = ['0p']
if len(sys.argv)>9: njetslist=[str(sys.argv[9])]
else: njetslist=['0p']

def readTree(file):
	if not os.path.exists(file): 
		print "Error: File does not exist! Aborting ...",file
		os._exit(1)
	tFile = TFile(file,'READ')
	tTree = tFile.Get('Delphes')
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
	'lepPt':('lepPt',linspace(0, 1000, 51).tolist(),';p_{T}(l) [GeV]'),
	'lepEta':('lepEta',linspace(-3, 3, 51).tolist(),';Lepton #eta'),
	'lepPhi':('lepPhi',linspace(-4, 4, 51).tolist(),';Lepton #phi'),
	'lepRelIso':('lepRelIso',linspace(0, 10, 51).tolist(),';Lepton RelIso'),
	'lepAbsIso':('lepAbsIso',linspace(0, 2000, 51).tolist(),';Lepton AbsIso'),
	'metPt':('metPt',linspace(0, 1500, 51).tolist(),';p^{miss}_{T} [GeV]'),
	'leadJetPt':('leadJetPt',linspace(0, 3000, 51).tolist(),';p_{T}(j_{1}) [GeV]'),
	'leadJetEta':('leadJetEta',linspace(-3, 3, 51).tolist(),';j_{1} #eta'),
	'leadJetPhi':('leadJetPhi',linspace(-4, 4, 51).tolist(),';j_{1} #phi'),
	'subLeadJetPt':('subLeadJetPt',linspace(0, 1500, 51).tolist(),';p_{T}(j_{2}) [GeV]'),
	'subLeadJetEta':('subLeadJetEta',linspace(-3, 3, 51).tolist(),';j_{2} #eta'),
	'subLeadJetPhi':('subLeadJetPhi',linspace(-4, 4, 51).tolist(),';j_{2} #phi'),
	'tlepLeadAK4Pt':('tlepLeadAK4Pt',linspace(0, 1500, 51).tolist(),';p_{T}(j_{1} in leptonic t) [GeV]'),
	'NJetsSel':('NJetsSel',linspace(0, 15, 16).tolist(),';AK4 jet multiplicity'),
	'minDR_lepJet':('minDR_lepJet',linspace(0, 2, 51).tolist(),';min[#DeltaR(l, jets)]'),
	'ptRel_lepJet':('ptRel_lepJet',linspace(0, 300, 51).tolist(),';p^{rel}_{T}(l, jets) [GeV]'),
	'deltaR_ljets0':('deltaR_ljets[0]',linspace(0, 5, 51).tolist(),';#DeltaR(l, j_{1})'),
	'deltaR_ljets1':('deltaR_ljets[1]',linspace(0, 5, 51).tolist(),';#DeltaR(l, j_{2})'),
	'WlepPt':('WlepPt',linspace(0, 3000, 51).tolist(),';p^{rec}_{T}(W) [GeV]'),
	'WlepMass':('WlepMass',linspace(75, 90, 51).tolist(),';M^{rec}(W) [GeV]'),
	'thadPt':('thadPt',linspace(0, 3000, 51).tolist(),';p^{rec}_{T}(hadronic t) [GeV]'),
	'thadMass':('thadMass',linspace(50, 300, 51).tolist(),';M^{rec}(hadronic t) [GeV]'),
	'thadChi2':('thadChi2',linspace(0, 100, 51).tolist(),';#chi^{2}(hadronic t)'),
	'tlepPt':('tlepPt',linspace(0, 3000, 51).tolist(),';p^{rec}_{T}(leptonic t) [GeV]'),
	'tlepMass':('tlepMass',linspace(50, 300, 51).tolist(),';M^{rec}(leptonic t) [GeV]'),
	'tlepChi2':('tlepChi2',linspace(0, 100, 51).tolist(),';#chi^{2}(leptonic t)'),
	'topAK8Pt':('topAK8Pt',linspace(0, 3000, 51).tolist(),';p_{T}(tagged t) [GeV]'),
	'topAK8Eta':('topAK8Eta',linspace(-3, 3, 51).tolist(),';tagged t #eta'),
	'topAK8Phi':('topAK8Phi',linspace(-4, 4, 51).tolist(),';tagged t #phi'),
	'topAK8Mass':('topAK8Mass',linspace(0, 300, 51).tolist(),';M(tagged t) [GeV]'),
	'topAK8Tau32':('topAK8Tau32',linspace(0, 1, 51).tolist(),';#tau_{3}/#tau_{2}(tagged t)'),
	'topAK8SDMass':('topAK8SDMass',linspace(0, 300, 51).tolist(),';M_{S-D}(tagged t) [GeV]'),
	'Ntoptagged':('Ntoptagged',linspace(0, 3, 4).tolist(),';t tag multiplicity'),

	'zpDeltaR':('zpDeltaR',linspace(0, 5, 51).tolist(),';#DeltaR(t_{1}, t_{2})'),
	'zpDeltaY':('zpDeltaY',linspace(0, 5, 51).tolist(),';#DeltaY(t_{1}, t_{2})'),
	'zpPt':('zpPt',linspace(0, 2000, 51).tolist(),';p_{T}(t#bar{t}) [GeV]'),
	'zpMass':('zpMass',linspace(0, 8000, 161).tolist(),';M_{rec}(t#bar{t}) [GeV]'),
	'genzpMass':('genzpMass',linspace(0, 8000, 161).tolist(),';M_{gen}(t#bar{t}) [GeV]'),
		
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
		#outDir+='/'+cutString
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
		#outDir+='/'+cutString
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
		#outDir+='/'+cutString
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

