#!/usr/bin/python

import os,sys,time,math,datetime,pickle,itertools,fnmatch
from ROOT import gROOT,TFile,TH1F
from array import array
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from weights import *
from utils import *

gROOT.SetBatch(1)
start_time = time.time()

lumiStrOrg = str(targetlumi/1000).replace('.','p') # 1/fb

region='SR' #PS,SR,TTCR,WJCR
isCategorized=1
cutString=''#'DY1.0_1jet400_2jet400'
if region=='SR': pfix='templates_zpMass_'
if not isCategorized: pfix='kinematics_'+region+'_'
pfix+='test_2018_8_23'
outDir = os.getcwd()+'/'+pfix+'/'+cutString

scaleSignalXsecTo1pb = True # this has to be "True" if you are making templates for limit calculation!!!!!!!!
scaleLumi = True
newTargetlumi = 3000000.
doAllSys = False
doQ2sys = False
if not doAllSys: doQ2sys = False
systematicList = ['pileup','jec','jer','jms','jmr','tau21','taupt','topsf','toppt','ht','muR','muF','muRFcorrd','trigeff','btag','mistag']
normalizeRENORM_PDF = False #normalize the renormalization/pdf uncertainties to nominal templates --> normalizes signal processes only !!!!
rebinBy = 2 #performs a regular rebinning with "Rebin(rebinBy)", put -1 if rebinning is not desired

doTTinc = False
bkgGrupList = ['tt','sitop','wjets','zjets','qcd']
bkgProcList = []#'tt','qcd']
bkgProcs = {}
bkgProcs['tt'] = ['TTmtt1000toInf','TTmtt0to1000inc','TTmtt1000toInfinc']
if doTTinc: bkgProcs['tt'] = ['TTinc']
bkgProcs['sitop'] = ['STs','STt','STbt','STtW','STbtW']
bkgProcs['wjets'] = ['WJetsInc']
bkgProcs['zjets'] = ['DyHT70to100','DyHT100to200','DyHT200to400','DyHT400to600','DyHT600to800','DyHT800to1200','DyHT1200to2500','DyHT2500toInf']
bkgProcs['ww'] = ['WW']
#bkgProcs['qcd'] = ['QCDPt15to7000']
#bkgProcs['qcd'] = ['QCDflatPt15to7000']
bkgProcs['qcd'] = ['QCDPt50to80','QCDPt80to120','QCDPt120to170','QCDPt170to300','QCDPt300to470','QCDPt470to600','QCDPt600to800','QCDPt800to1000','QCDPt1000toInf']
#bkgProcs['qcd'] = ['QCDPt170to300','QCDPt300to470','QCDPt470to600','QCDPt600to800','QCDPt800to1000','QCDPt1000toInf']
dataList = ['Data']

htProcs = []#['ewk','WJets']
topptProcs = []#['top','TTJets']
bkgProcs['top_q2up'] = []#bkgProcs['T']+['TTJetsPHQ2U']#'TtWQ2U','TbtWQ2U']
bkgProcs['top_q2dn'] = []#bkgProcs['T']+['TTJetsPHQ2D']#'TtWQ2D','TbtWQ2D']

massList = range(2000,6000+1,1000)
sigList = ['ZpM'+str(mass) for mass in massList]

isEMlist = ['E','M']
nttaglist = ['0p','0','1']
nWtaglist = ['0p']
nbtaglist = ['0p','0','1']#,'2']
if not isCategorized: 
	nttaglist = ['0p']
	nbtaglist = ['0p']
njetslist=['0p']

catList = ['is'+item[0]+'_nT'+item[1]+'_nW'+item[2]+'_nB'+item[3]+'_nJ'+item[4] for item in list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist,njetslist))]
tagList = ['nT'+item[0]+'_nW'+item[1]+'_nB'+item[2]+'_nJ'+item[3] for item in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist))]
for ind in range(len(catList)): catList[ind] = catList[ind].replace('_nT0p','').replace('_nW0p','').replace('_nB0p','').replace('_nJ0p','')
for ind in range(len(tagList)): tagList[ind] = tagList[ind].replace('_nT0p','').replace('_nW0p','').replace('_nB0p','').replace('_nJ0p','')

lumiSys = 0.0#25 #lumi uncertainty
eltrigSys = 0.0 #electron trigger uncertainty
mutrigSys = 0.0 #muon trigger uncertainty
elIdSys = 0.0 #electron id uncertainty
muIdSys = 0.0 #muon id uncertainty
elIsoSys = 0.0 #electron isolation uncertainty
muIsoSys = 0.0 #muon isolation uncertainty

elcorrdSys = 0.0#math.sqrt(lumiSys**2+eltrigSys**2+elIdSys**2+elIsoSys**2)
mucorrdSys = 0.0#math.sqrt(lumiSys**2+mutrigSys**2+muIdSys**2+muIsoSys**2)

lumiScaleCoeff = newTargetlumi/targetlumi
lumiStr = lumiStrOrg
if scaleLumi: lumiStr=str(newTargetlumi/1000).replace('.','p') # 1/fb
	
if 'CR' in region: postTag = 'isCR_'
else: postTag = 'isSR_'
###########################################################
#################### CATEGORIZATION #######################
###########################################################
def makeThetaCats(datahists,sighists,bkghists,discriminant):
	yieldTable = {}
	yieldStatErrTable = {}
	for cat in catList:
		histoPrefix=discriminant+'_'+lumiStr+'fbinv_'+cat
		yieldTable[histoPrefix]={}
		yieldStatErrTable[histoPrefix]={}
		if doAllSys:
			for syst in systematicList:
				for ud in ['Up','Down']:
					yieldTable[histoPrefix+syst+ud]={}
			
		if doQ2sys:
			yieldTable[histoPrefix+'q2Up']={}
			yieldTable[histoPrefix+'q2Down']={}

	#Initialize dictionaries for histograms
	hists={}
	for cat in catList:
		print "              processing cat: "+cat
		histoPrefix=discriminant+'_'+lumiStr+'fbinv_'+cat
		histoPrefixOrg=histoPrefix.replace(lumiStr,lumiStrOrg)

		#Group data processes
		hists['data'+cat] = datahists[histoPrefixOrg+'_'+dataList[0]].Clone(histoPrefix+'__DATA')
		for dat in dataList:
			if dat!=dataList[0]: hists['data'+cat].Add(datahists[histoPrefixOrg+'_'+dat])
		
		#Group processes
		for proc in bkgProcList+bkgGrupList:
			hists[proc+cat] = bkghists[histoPrefixOrg+'_'+bkgProcs[proc][0]].Clone(histoPrefix+'__'+proc)
			for bkg in bkgProcs[proc]:
				if bkg!=bkgProcs[proc][0]: hists[proc+cat].Add(bkghists[histoPrefixOrg+'_'+bkg])

		#get signal
		for signal in sigList: hists[signal+cat] = sighists[histoPrefixOrg+'_'+signal].Clone(histoPrefix+'__sig')

		#systematics
		if doAllSys:
			for syst in systematicList:
				for ud in ['Up','Down']:
					for proc in bkgProcList+bkgGrupList:
						if syst=='toppt' and proc not in topptProcs: continue
						if syst=='ht' and proc not in htProcs: continue
						hists[proc+cat+syst+ud] = bkghists[histoPrefixOrg.replace(discriminant,discriminant+syst+ud)+'_'+bkgProcs[proc][0]].Clone(histoPrefix+'__'+proc+'__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
						for bkg in bkgProcs[proc]:
							if bkg!=bkgProcs[proc][0]: hists[proc+cat+syst+ud].Add(bkghists[histoPrefixOrg.replace(discriminant,discriminant+syst+ud)+'_'+bkg])
					if syst=='toppt' or syst=='ht': continue
					for signal in sigList: hists[signal+cat+syst+ud] = sighists[histoPrefixOrg.replace(discriminant,discriminant+syst+ud)+'_'+signal].Clone(histoPrefix+'__sig__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
			for pdfInd in range(100):
				for proc in bkgProcList+bkgGrupList:
					hists[proc+cat+'pdf'+str(pdfInd)] = bkghists[histoPrefixOrg.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkgProcs[proc][0]].Clone(histoPrefix+'__'+proc+'__pdf'+str(pdfInd))
					for bkg in bkgProcs[proc]:
						if bkg!=bkgProcs[proc][0]: hists[proc+cat+'pdf'+str(pdfInd)].Add(bkghists[histoPrefixOrg.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
				for signal in sigList: hists[signal+cat+'pdf'+str(pdfInd)] = sighists[histoPrefixOrg.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal].Clone(histoPrefix+'__sig__pdf'+str(pdfInd))
										
		if doQ2sys:
			for proc in bkgProcList+bkgGrupList:
				if proc+'_q2up' not in bkgProcs.keys(): continue
				hists[proc+cat+'q2Up'] = bkghists[histoPrefixOrg+'_'+bkgProcs[proc+'_q2up'][0]].Clone(histoPrefix+'__'+proc+'__q2__plus')
				hists[proc+cat+'q2Down'] = bkghists[histoPrefixOrg+'_'+bkgProcs[proc+'_q2dn'][0]].Clone(histoPrefix+'__'+proc+'__q2__minus')
				for bkg in bkgProcs[proc+'_q2up']:
					if bkg!=bkgProcs[proc+'_q2up'][0]: hists[proc+cat+'q2Up'].Add(bkghists[histoPrefixOrg+'_'+bkg])
				for bkg in bkgProcs[proc+'_q2dn']:
					if bkg!=bkgProcs[proc+'_q2dn'][0]: hists[proc+cat+'q2Down'].Add(bkghists[histoPrefixOrg+'_'+bkg])
	
		#+/- 1sigma variations of shape systematics
		if doAllSys:
			for syst in systematicList:
				for ud in ['Up','Down']:
					for proc in bkgGrupList+bkgProcList+sigList:
						if syst=='toppt' and proc not in topptProcs: continue
						if syst=='ht' and proc not in htProcs: continue
						yieldTable[histoPrefix+syst+ud][proc] = hists[proc+cat+syst+ud].Integral()
		if doQ2sys:
			for proc in bkgProcList+bkgGrupList:
				if proc+'_q2up' not in bkgProcs.keys(): continue
				yieldTable[histoPrefix+'q2Up'][proc] = hists[proc+cat+'q2Up'].Integral()
				yieldTable[histoPrefix+'q2Down'][proc] = hists[proc+cat+'q2Down'].Integral()

		#prepare yield table
		for proc in bkgGrupList+bkgProcList+sigList+['data']: yieldTable[histoPrefix][proc] = hists[proc+cat].Integral()
		yieldTable[histoPrefix]['totBkg'] = sum([hists[proc+cat].Integral() for proc in bkgGrupList])
		yieldTable[histoPrefix]['dataOverBkg']= yieldTable[histoPrefix]['data']/(yieldTable[histoPrefix]['totBkg']+1e-20)

		#prepare MC yield error table
		for proc in bkgGrupList+bkgProcList+sigList+['data']: yieldStatErrTable[histoPrefix][proc] = 0.
		yieldStatErrTable[histoPrefix]['totBkg'] = 0.
		yieldStatErrTable[histoPrefix]['dataOverBkg']= 0.

		for ibin in range(1,hists[bkgGrupList[0]+cat].GetXaxis().GetNbins()+1):
			for proc in bkgGrupList+bkgProcList+sigList+['data']: yieldStatErrTable[histoPrefix][proc] += hists[proc+cat].GetBinError(ibin)**2
			yieldStatErrTable[histoPrefix]['totBkg'] += sum([hists[proc+cat].GetBinError(ibin)**2 for proc in bkgGrupList])
		for key in yieldStatErrTable[histoPrefix].keys(): yieldStatErrTable[histoPrefix][key] = math.sqrt(yieldStatErrTable[histoPrefix][key])

	#scale signal cross section to 1pb
	if scaleSignalXsecTo1pb:
		print "       SCALING SIGNAL TEMPLATES TO 1pb ..."
		for signal in sigList:
			for cat in catList:
				hists[signal+cat].Scale(1./xsec[signal])
				if doAllSys:
					for syst in systematicList:
						if syst=='toppt' or syst=='ht': continue
						hists[signal+cat+syst+'Up'].Scale(1./xsec[signal])
						hists[signal+cat+syst+'Down'].Scale(1./xsec[signal])
						if normalizeRENORM_PDF and (syst.startswith('mu') or syst=='pdf'):
							hists[signal+cat+syst+'Up'].Scale(hists[signal+cat].Integral()/hists[signal+cat+syst+'Up'].Integral())
							hists[signal+cat+syst+'Down'].Scale(hsihistsg[signal+cat].Integral()/hists[signal+cat+syst+'Down'].Integral())
					for pdfInd in range(100): 
						hists[signal+cat+'pdf'+str(pdfInd)].Scale(1./xsec[signal])

	nbins = str(int(hists['data'+cat].GetXaxis().GetNbins()))
	#Theta templates:
	print "       WRITING THETA TEMPLATES: "
	for signal in sigList:
		print "              ... "+signal
		thetaRfileName = outDir+'/templates_'+discriminant+'_'+signal+'_'+lumiStr+'fbinv'+'.root'
		thetaRfile = TFile(thetaRfileName,'RECREATE')
		for cat in catList:
			for proc in bkgGrupList+[signal]:
				if hists[proc+cat].Integral() > 0:
					hists[proc+cat].Write()
					if doAllSys:
						for syst in systematicList:
							if syst=='toppt' and proc not in topptProcs: continue
							if syst=='ht' and proc not in htProcs: continue
							hists[proc+cat+syst+'Up'].Write()
							hists[proc+cat+syst+'Down'].Write()
						for pdfInd in range(100): hists[proc+cat+'pdf'+str(pdfInd)].Write()
					if doQ2sys:
						if proc+'_q2up' not in bkgProcs.keys(): continue
						hists[proc+cat+'q2Up'].Write()
						hists[proc+cat+'q2Down'].Write()
				else: print proc+cat,"IS EMPTY! SKIPPING ..."
			hists['data'+cat].Write()
		thetaRfile.Close()

	#Combine templates:
	print "       WRITING COMBINE TEMPLATES: "
	combineRfileName = outDir+'/templates_'+discriminant+'_'+lumiStr+'fbinv'+'.root'
	combineRfile = TFile(combineRfileName,'RECREATE')
	for cat in catList:
		print "              ... "+cat
		for signal in sigList:
			mass = [str(mass) for mass in massList if str(mass) in signal][0]
			hists[signal+cat].SetName(hists[signal+cat].GetName().replace('fbinv_','fbinv_'+postTag).replace('__sig','__'+signal.replace('M'+mass,'')+'M'+mass))
			hists[signal+cat].Write()
			if doAllSys:
				for syst in systematicList:
					if syst=='toppt' or syst=='ht': continue
					hists[signal+cat+syst+'Up'].SetName(hists[signal+cat+syst+'Up'].GetName().replace('fbinv_','fbinv_'+postTag).replace('__sig','__'+signal.replace('M'+mass,'')+'M'+mass).replace('__plus','Up'))
					hists[signal+cat+syst+'Down'].SetName(hists[signal+cat+syst+'Down'].GetName().replace('fbinv_','fbinv_'+postTag).replace('__sig','__'+signal.replace('M'+mass,'')+'M'+mass).replace('__minus','Down'))
					hists[signal+cat+syst+'Up'].Write()
					hists[signal+cat+syst+'Down'].Write()
				for pdfInd in range(100): 
					hists[signal+cat+'pdf'+str(pdfInd)].SetName(hists[signal+cat+'pdf'+str(pdfInd)].GetName().replace('fbinv_','fbinv_'+postTag).replace('__sig','__'+signal.replace('M'+mass,'')+'M'+mass))
					hists[signal+cat+'pdf'+str(pdfInd)].Write()
		for proc in bkgGrupList:
			hists[proc+cat].SetName(hists[proc+cat].GetName().replace('fbinv_','fbinv_'+postTag))
			hists[proc+cat].Write()
			if doAllSys:
				for syst in systematicList:
					if syst=='toppt' and proc not in topptProcs: continue
					if syst=='ht' and proc not in htProcs: continue
					hists[proc+cat+syst+'Up'].SetName(hists[proc+cat+syst+'Up'].GetName().replace('fbinv_','fbinv_'+postTag).replace('__plus','Up'))
					hists[proc+cat+syst+'Down'].SetName(hists[proc+cat+syst+'Down'].GetName().replace('fbinv_','fbinv_'+postTag).replace('__minus','Down'))
					hists[proc+cat+syst+'Up'].Write()
					hists[proc+cat+syst+'Down'].Write()
				for pdfInd in range(100): 
					hists[proc+cat+'pdf'+str(pdfInd)].SetName(hists[proc+cat+'pdf'+str(pdfInd)].GetName().replace('fbinv_','fbinv_'+postTag))
					hists[proc+cat+'pdf'+str(pdfInd)].Write()
			if doQ2sys:
				if proc+'_q2up' not in bkgProcs.keys(): continue
				hists[proc+cat+'q2Up'].SetName(hists[proc+cat+'q2Up'].GetName().replace('fbinv_','fbinv_'+postTag).replace('__plus','Up'))
				hists[proc+cat+'q2Down'].SetName(hists[proc+cat+'q2Down'].GetName().replace('fbinv_','fbinv_'+postTag).replace('__minus','Down'))
				hists[proc+cat+'q2Up'].Write()
				hists[proc+cat+'q2Down'].Write()
		hists['data'+cat].SetName(hists['data'+cat].GetName().replace('fbinv_','fbinv_'+postTag).replace('DATA','data_obs'))
		hists['data'+cat].Write()
	combineRfile.Close()

	print "       WRITING SUMMARY TEMPLATES: "
	for signal in sigList:
		print "              ... "+signal
		yldRfileName = outDir+'/templates_YLD_'+signal+'_'+lumiStr+'fbinv.root'
		yldRfile = TFile(yldRfileName,'RECREATE')
		for isEM in isEMlist:	
			for proc in bkgGrupList+['data',signal]:
				yldHists = {}
				yldHists[isEM+proc]=TH1F('YLD_'+lumiStr+'fbinv_is'+isEM+'_nT0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data','DATA'),'',len(tagList),0,len(tagList))
				if doAllSys and proc!='data':
					for syst in systematicList:
						for ud in ['Up','Down']:
							if syst=='toppt' and proc not in topptProcs: continue
							if syst=='ht' and proc not in htProcs: continue
							yldHists[isEM+proc+syst+ud]=TH1F('YLD_'+lumiStr+'fbinv_is'+isEM+'_nT0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data','DATA')+'__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'),'',len(tagList),0,len(tagList))
				if doQ2sys and proc+'_q2up' in bkgProcs.keys(): 
					yldHists[isEM+proc+'q2Up']  =TH1F('YLD_'+lumiStr+'fbinv_is'+isEM+'_nT0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data','DATA')+'__q2__plus','',len(tagList),0,len(tagList))
					yldHists[isEM+proc+'q2Down']=TH1F('YLD_'+lumiStr+'fbinv_is'+isEM+'_nT0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data','DATA')+'__q2__minus','',len(tagList),0,len(tagList))
				ibin = 1
				for cat in catList:
					if 'is'+isEM not in cat: continue
					binStr = ''
					if nttaglist[0]!='0p':
						nttag = cat[cat.find('_nT')+3:].split('_')[0]
						if 'p' in nttag: binStr+='#geq'+nttag[:-1]+'t/'
						else: binStr+=nttag+'t/'
					if nWtaglist[0]!='0p':
						nWtag = cat[cat.find('_nW')+3:].split('_')[0]
						if 'p' in nWtag: binStr+='#geq'+nWtag[:-1]+'W/'
						else: binStr+=nWtag+'W/'
					if nbtaglist[0]!='0p':
						nbtag = cat[cat.find('_nB')+3:].split('_')[0]
						if 'p' in nbtag: binStr+='#geq'+nbtag[:-1]+'b/'
						else: binStr+=nbtag+'b/'
					if njetslist[0]!='0p' and len(njetslist)>1:
						njets = cat[cat.find('_nJ')+3:].split('_')[0]
						if 'p' in njets: binStr+='#geq'+njets[:-1]+'j'
						else: binStr+=njets+'j'
					if binStr.endswith('/'): binStr=binStr[:-1]
					histoPrefix=discriminant+'_'+lumiStr+'fbinv_'+cat
					yldHists[isEM+proc].SetBinContent(ibin,yieldTable[histoPrefix][proc])
					yldHists[isEM+proc].SetBinError(ibin,yieldStatErrTable[histoPrefix][proc])
					yldHists[isEM+proc].GetXaxis().SetBinLabel(ibin,binStr)
					if doAllSys and proc!='data':
						for syst in systematicList:
							for ud in ['Up','Down']:
								if syst=='toppt' and proc not in topptProcs: continue
								if syst=='ht' and proc not in htProcs: continue
								yldHists[isEM+proc+syst+ud].SetBinContent(ibin,yieldTable[histoPrefix+syst+ud][proc])
								yldHists[isEM+proc+syst+ud].GetXaxis().SetBinLabel(ibin,binStr)
					if doQ2sys and proc+'_q2up' in bkgProcs.keys(): 
						yldHists[isEM+proc+'q2Up'].SetBinContent(ibin,yieldTable[histoPrefix+'q2Up'][proc])
						yldHists[isEM+proc+'q2Up'].GetXaxis().SetBinLabel(ibin,binStr)
						yldHists[isEM+proc+'q2Down'].SetBinContent(ibin,yieldTable[histoPrefix+'q2Down'][proc])
						yldHists[isEM+proc+'q2Down'].GetXaxis().SetBinLabel(ibin,binStr)
					ibin+=1
				yldHists[isEM+proc].Write()
				if doAllSys and proc!='data':
					for syst in systematicList:
						for ud in ['Up','Down']:
							if syst=='toppt' and proc not in topptProcs: continue
							if syst=='ht' and proc not in htProcs: continue
							yldHists[isEM+proc+syst+ud].Write()
				if doQ2sys and proc+'_q2up' in bkgProcs.keys(): 
					yldHists[isEM+proc+'q2Up'].Write()
					yldHists[isEM+proc+'q2Down'].Write()
		yldRfile.Close()
			
	table = []
	table.append(['CUTS:',cutString])
	table.append(['break'])
	table.append(['break'])
	
	#yields without background grouping
	table.append(['YIELDS']+[proc for proc in bkgProcList+['data']])
	for cat in catList:
		row = [cat]
		histoPrefix=discriminant+'_'+lumiStr+'fbinv_'+cat
		for proc in bkgProcList+['data']:
			row.append(str(yieldTable[histoPrefix][proc])+' $\pm$ '+str(yieldStatErrTable[histoPrefix][proc]))
		table.append(row)			
	table.append(['break'])
	table.append(['break'])
	
	#yields with top,ewk,qcd grouping
	table.append(['YIELDS']+[proc for proc in bkgGrupList+['data']])
	for cat in catList:
		row = [cat]
		histoPrefix=discriminant+'_'+lumiStr+'fbinv_'+cat
		for proc in bkgGrupList+['data']:
			row.append(str(yieldTable[histoPrefix][proc])+' $\pm$ '+str(yieldStatErrTable[histoPrefix][proc]))
		table.append(row)
	table.append(['break'])
	table.append(['break'])
	
	#yields for signals
	table.append(['YIELDS']+[proc for proc in sigList])
	for cat in catList:
		row = [cat]
		histoPrefix=discriminant+'_'+lumiStr+'fbinv_'+cat
		for proc in sigList:
			row.append(str(yieldTable[histoPrefix][proc])+' $\pm$ '+str(yieldStatErrTable[histoPrefix][proc]))
		table.append(row)

	#yields for AN tables (yields in e/m channels)
	for isEM in isEMlist:
		if isEM==isEMlist[0]: corrdSys = elcorrdSys
		if isEM==isEMlist[1]: corrdSys = mucorrdSys
		for nttag in nttaglist:
			table.append(['break'])
			table.append(['','is'+isEM+'_nT'+nttag+'_yields'])
			table.append(['break'])
			table.append(['YIELDS']+[cat for cat in catList if 'is'+isEM in cat and 'nT'+nttag in cat]+['\\\\'])
			for proc in bkgGrupList+['totBkg','data','dataOverBkg']+sigList:
				row = [proc]
				for cat in catList:
					if not ('is'+isEM in cat and 'nT'+nttag in cat): continue
					modTag = cat[cat.find('nT'):cat.find('nJ')-3]
					histoPrefix=discriminant+'_'+lumiStr+'fbinv_'+cat
					yieldtemp = 0.
					yielderrtemp = 0.
					if proc=='totBkg' or proc=='dataOverBkg':
						for bkg in bkgGrupList:
							try:
								yieldtemp += yieldTable[histoPrefix][bkg]
								yielderrtemp += yieldStatErrTable[histoPrefix][bkg]**2
							except:
								print "Missing",bkg,"for channel:",cat
								pass
						yielderrtemp += (corrdSys*yieldtemp)**2
						if proc=='dataOverBkg':
							dataTemp = yieldTable[histoPrefix]['data']+1e-20
							dataTempErr = yieldStatErrTable[histoPrefix]['data']**2
							yielderrtemp = ((dataTemp/yieldtemp)**2)*(dataTempErr/dataTemp**2+yielderrtemp/yieldtemp**2)
							yieldtemp = dataTemp/yieldtemp
					else:
						try:
							yieldtemp += yieldTable[histoPrefix][proc]
							yielderrtemp += yieldStatErrTable[histoPrefix][proc]**2
						except:
							print "Missing",proc,"for channel:",cat
							pass
						yielderrtemp += (corrdSys*yieldtemp)**2
					yielderrtemp = math.sqrt(yielderrtemp)
					if proc=='data': row.append(' & '+str(int(yieldTable[histoPrefix][proc])))
					else: row.append(' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(yielderrtemp,2)))
				row.append('\\\\')
				table.append(row)
	
	#yields for PAS tables (yields in e/m channels combined)
	for nttag in nttaglist:
		table.append(['break'])
		table.append(['','isL_nT'+nttag+'_yields'])
		table.append(['break'])
		table.append(['YIELDS']+[cat.replace('isE','isL') for cat in catList if 'isE' in cat and 'nT'+nttag in cat]+['\\\\'])
		for proc in bkgGrupList+['totBkg','data','dataOverBkg']+sigList:
			row = [proc]
			for cat in catList:
				if not ('isE' in cat and 'nT'+nttag in cat): continue
				modTag = cat[cat.find('nT'):cat.find('nJ')-3]
				histoPrefixE = discriminant+'_'+lumiStr+'fbinv_'+cat
				histoPrefixM = histoPrefixE.replace('isE','isM')
				yieldtemp = 0.
				yieldtempE = 0.
				yieldtempM = 0.
				yielderrtemp = 0. 
				if proc=='totBkg' or proc=='dataOverBkg':
					for bkg in bkgGrupList:
						try:
							yieldtempE += yieldTable[histoPrefixE][bkg]
							yieldtempM += yieldTable[histoPrefixM][bkg]
							yieldtemp  += yieldTable[histoPrefixE][bkg]+yieldTable[histoPrefixM][bkg]
							yielderrtemp += yieldStatErrTable[histoPrefixE][bkg]**2+yieldStatErrTable[histoPrefixM][bkg]**2
						except:
							print "Missing",bkg,"for channel:",cat
							pass
					yielderrtemp += (elcorrdSys*yieldtempE)**2+(mucorrdSys*yieldtempM)**2
					if proc=='dataOverBkg':
						dataTemp = yieldTable[histoPrefixE]['data']+yieldTable[histoPrefixM]['data']+1e-20
						dataTempErr = yieldStatErrTable[histoPrefixE]['data']**2+yieldStatErrTable[histoPrefixM]['data']**2
						yielderrtemp = ((dataTemp/yieldtemp)**2)*(dataTempErr/dataTemp**2+yielderrtemp/yieldtemp**2)
						yieldtemp = dataTemp/yieldtemp
				else:
					try:
						yieldtempE += yieldTable[histoPrefixE][proc]
						yieldtempM += yieldTable[histoPrefixM][proc]
						yieldtemp  += yieldTable[histoPrefixE][proc]+yieldTable[histoPrefixM][proc]
						yielderrtemp += yieldStatErrTable[histoPrefixE][proc]**2+yieldStatErrTable[histoPrefixM][proc]**2
					except:
						print "Missing",proc,"for channel:",cat
						pass
					yielderrtemp += (elcorrdSys*yieldtempE)**2+(mucorrdSys*yieldtempM)**2
				yielderrtemp = math.sqrt(yielderrtemp)
				if proc=='data': row.append(' & '+str(int(yieldTable[histoPrefixE][proc]+yieldTable[histoPrefixM][proc])))
				else: row.append(' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(yielderrtemp,2)))
			row.append('\\\\')
			table.append(row)

	#systematics
	if doAllSys:
		table.append(['break'])
		table.append(['','Systematics'])
		table.append(['break'])
		for proc in bkgGrupList+sigList:
			table.append([proc]+[cat for cat in catList]+['\\\\'])
			for syst in sorted(systematicList+['q2']):
				for ud in ['Up','Down']:
					row = [syst+ud]
					for cat in catList:
						histoPrefix = discriminant+'_'+lumiStr+'fbinv_'+cat
						nomHist = histoPrefix
						shpHist = histoPrefix+syst+ud
						try: row.append(' & '+str(round(yieldTable[shpHist][proc]/(yieldTable[nomHist][proc]+1e-20),2)))
						except:
							if not ((syst=='toppt' and proc not in topptProcs) or (syst=='ht' and proc not in htProcs) or (syst=='q2' and (proc+'_q2up' not in bkgProcs.keys() or not doQ2sys))):
								print "Missing",proc,"for channel:",cat,"and systematic:",syst
							pass
					row.append('\\\\')
					table.append(row)
			table.append(['break'])
		
	out=open(outDir+'/yields_'+discriminant+'_'+lumiStr+'fbinv'+'.txt','w')
	printTable(table,out)

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)

iPlotList = []
for file in findfiles(outDir+'/'+catList[0][2:]+'/', '*.p'):
    if 'bkghists' not in file: continue
    if not os.path.exists(file.replace('bkghists','datahists')): continue
    if not os.path.exists(file.replace('bkghists','sighists')): continue
    iPlotList.append(file.split('/')[-1].replace('bkghists_','')[:-2])

print "WORKING DIR:",outDir
print "Templates:",iPlotList
for iPlot in iPlotList:
	datahists = {}
	bkghists  = {}
	sighists  = {}
	if len(sys.argv)>1 and iPlot!=sys.argv[1]: continue
	print "LOADING DISTRIBUTION: "+iPlot
	for cat in catList:
		print "         ",cat[2:]
		datahists.update(pickle.load(open(outDir+'/'+cat[2:]+'/datahists_'+iPlot+'.p','rb')))
		bkghists.update(pickle.load(open(outDir+'/'+cat[2:]+'/bkghists_'+iPlot+'.p','rb')))
		sighists.update(pickle.load(open(outDir+'/'+cat[2:]+'/sighists_'+iPlot+'.p','rb')))
	
	#Re-scale lumi
	if scaleLumi:
		for key in bkghists.keys(): 
			bkghists[key].Scale(lumiScaleCoeff)
			#if 'QCDPt170to300' in key: bkghists[key].Scale(1./10.)
		for key in sighists.keys(): sighists[key].Scale(lumiScaleCoeff)
	
	#Rebin
	if rebinBy>0:
		print "       REBINNING HISTOGRAMS: MERGING",rebinBy,"BINS ..."
		for data in datahists.keys(): datahists[data] = datahists[data].Rebin(rebinBy)
		for bkg in bkghists.keys():   bkghists[bkg] = bkghists[bkg].Rebin(rebinBy)
		for sig in sighists.keys():   sighists[sig] = sighists[sig].Rebin(rebinBy)

 	#Negative Bin Correction
 	print "       CORRECTING NEGATIVE BINS ..."
 	for bkg in bkghists.keys(): negBinCorrection(bkghists[bkg])
 	for sig in sighists.keys(): negBinCorrection(sighists[sig])

 	#OverFlow Correction
 	print "       CORRECTING OVER(UNDER)FLOW BINS ..."
 	for data in datahists.keys(): 
 		overflow(datahists[data])
 		underflow(datahists[data])
 	for bkg in bkghists.keys():
 		overflow(bkghists[bkg])
 		underflow(bkghists[bkg])
 	for sig in sighists.keys():
 		overflow(sighists[sig])
 		underflow(sighists[sig])

	print "       MAKING CATEGORIES FOR TOTAL SIGNALS ..."
	makeThetaCats(datahists,sighists,bkghists,iPlot)

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))


