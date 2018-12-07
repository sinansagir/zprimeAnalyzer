#!/usr/bin/python

import os,sys,time,math,pickle,itertools
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
import ROOT as rt
from weights import *
from utils import *
import CMS_lumi, tdrstyle

rt.gROOT.SetBatch(1)
start_time = time.time()

lumi="3 ab^{-1}" #for plots
lumiInTemplates='3000p0'#str(targetlumi/1000).replace('.','p') # 1/fb
plotForPAS = True

region='SR' #PS,SR,TTCR,WJCR
isCategorized=1
iPlot='zpMass'
if len(sys.argv)>1: iPlot=str(sys.argv[1])
cutString=''#'DY1.0_1jet400_2jet400'
if region=='SR': pfix='templates_alljets_'
elif region=='WJCR': pfix='wjets_'
elif region=='TTCR': pfix='ttbar_'
if not isCategorized: pfix='kinematics_'+region+'_'
templateDir=os.getcwd()+'/'+pfix+'halveStatUnc_2018_10_31/'+cutString+'/'

isRebinned='_rebinned_stat0p1'#'_rebinned_stat0p1'#'_rebinned_stat0p5' #post for ROOT file names
saveKey = '_v2'# tag for plot names
signal = 'Zp'

if 'W' in signal:
	saveKey = '_W30'
	massList = range(3000,6000+1,3000)+range(8000,12000+1,2000)
	sigs = ['ZpW30M'+str(mass) for mass in massList]
	siglegs = {sigs[0]:'Z\' 30% width (3 TeV)', sigs[1]:'Z\' 30% width (6 TeV)',sigs[2]:'Z\' 30% width (8 TeV)',sigs[3]:'Z\' 30% width (10 TeV)',sigs[4]:'Z\' 30% width (12 TeV)'}
	sigColors = {sigs[0]:rt.kBlack, sigs[1]:rt.kRed,sigs[2]:rt.kOrange,sigs[3]:rt.kBlue,sigs[4]:rt.kGreen+3}
	sigLines = {sigs[0]:1, sigs[1]:3,sigs[2]:5,sigs[3]:7,sigs[4]:7}
else:
# 	massList = range(3000,6000+1,3000)+range(8000,12000+1,2000)	
# 	sigs = ['ZpM'+str(mass) for mass in massList]
# 	siglegs = {sigs[0]:'RSG (3 TeV)', sigs[1]:'RSG (6 TeV)',sigs[2]:'RSG (8 TeV)',sigs[3]:'RSG (10 TeV)',sigs[4]:'RSG (12 TeV)'}
# 	sigColors = {sigs[0]:rt.kBlack, sigs[1]:rt.kRed,sigs[2]:rt.kOrange,sigs[3]:rt.kBlue,sigs[4]:rt.kGreen+3}
# 	sigLines = {sigs[0]:1, sigs[1]:3,sigs[2]:5,sigs[3]:7,sigs[4]:7}
	massList = [3000,6000,12000]
	sigs = ['ZpM'+str(mass) for mass in massList]
	siglegs = {'ZpM3000':'RSG (3 TeV)', 'ZpM6000':'RSG (6 TeV)','ZpM8000':'RSG (8 TeV)','ZpM10000':'RSG (10 TeV)','ZpM12000':'RSG (12 TeV)'}
	sigColors = {'ZpM3000':rt.kOrange, 'ZpM6000':rt.kRed,'ZpM8000':rt.kBlack,'ZpM10000':rt.kBlue,'ZpM12000':rt.kGreen+3}
	sigLines = {'ZpM3000':1, 'ZpM6000':1,'ZpM8000':1,'ZpM10000':1,'ZpM12000':1}

scaleSignals = False
sigScaleFact = -1 #put -1 if auto-scaling wanted
tempsig='templates_'+iPlot+'_'+sigs[-1]+'_'+lumiInTemplates+'fbinv'+isRebinned+'.root'

bkgProcList = ['ttbar','qcd']#'sitop','wjets','zjets','dibos','qcd']
bkgHistColors = {'ttbar':rt.kRed-9,'sitop':rt.kRed-5,'wjets':rt.kBlue-7,'zjets':rt.kBlue-3,'dibos':rt.kBlue,'qcd':rt.kOrange-5,'ewk':rt.kBlue-7,'other':rt.kOrange-5}
proclegs = {'ttbar':'t#bar{t}','sitop':'Single top','wjets':'W+jets','zjets':'Z+jets','dibos':'WW','qcd':'QCD','data':'Data','ewk':'EW','other':'Other'}

systematicList = ['jec']#,'jer']
doAllSys = True
doQ2sys  = False
if not doAllSys: doQ2sys = False
doNormByBinWidth=True
doOneBand = False
if not doAllSys: doOneBand = True # Don't change this!
blind = True
yLog  = True
doRealPull = False
if doRealPull: doOneBand=False
compareShapes = False
if compareShapes: blind,yLog,scaleSignals,sigScaleFact=True,False,False,-1
drawYields = False
doChi2KStests = False

isEMlist = ['E','M']
nttaglist = ['0p']
nWtaglist = ['0p']
nbtaglist = ['0','1','2']
if not isCategorized: 
	nttaglist = ['0p']
	nbtaglist = ['0p']
njetslist = ['0p']
if 'YLD' in iPlot:
	doNormByBinWidth = False
	nttaglist = ['0p']
	nWtaglist = ['0p']
	nbtaglist = ['0p']
	njetslist = ['0p']

tagList = list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist))

lumiSys = 0.01 #lumi uncertainty
lepIdIsoSys = 0.01 #lepton id/iso uncertainty
jesSys = 0.0#35 #JES uncertainty
jerSys = 0.03 #JER uncertainty
btagSys = 0.01 #b-tagging uncertainty
mistagSys = 0.10 #b-tagging uncertainty
ttagSys = 0.05 #t-tagging uncertainty
puSys = 0.0#3 #Pileup uncertainty
pdfSys = 0.024 #PDF uncertainty
murfSys = 0.0 #Renorm/Fact. scale uncertainty

corrdSys = math.sqrt(lumiSys**2+lepIdIsoSys**2+jesSys**2+jerSys**2+btagSys**2+mistagSys**2+ttagSys**2+puSys**2+pdfSys**2+murfSys**2) #cheating while total e/m values are close

modelingSys = {}
modelingSys['ttbar'] = math.sqrt(0.03**2+0.04**2) #ttbar x-sec and muRF uncertainty
modelingSys['sitop'] = 0.06 #Single top x-sec uncertainty
modelingSys['wjets'] = math.sqrt(0.03**2+0.03**2) #W+jets x-sec and muRF uncertainty
modelingSys['zjets'] = 0.06 #Z+jets x-sec uncertainty
modelingSys['dibos'] = 0.06 #Diboson x-sec uncertainty
modelingSys['qcd']   = math.sqrt(0.02**2+0.05**2) #QCD DDBkg uncertainty
modelingSys['other'] = math.sqrt(modelingSys['sitop']**2+modelingSys['wjets']**2+modelingSys['zjets']**2+modelingSys['dibos']**2+modelingSys['qcd']**2)

def getNormUnc(hist,ibin,modelingUnc):
	contentsquared = hist.GetBinContent(ibin)**2
	error = corrdSys*corrdSys*contentsquared  #correlated uncertainties
	error += modelingUnc*modelingUnc*contentsquared #background modeling uncertainty from CRs
	return error

def formatUpperHist(histogram,themax):
	histogram.GetXaxis().SetLabelSize(0)
	if 'NTJets' in histogram.GetName(): histogram.GetXaxis().SetNdivisions(5)
	elif 'NWJets' in histogram.GetName(): histogram.GetXaxis().SetNdivisions(5)
	elif 'NBJets' in histogram.GetName(): histogram.GetXaxis().SetNdivisions(6,rt.kFALSE)
	else: histogram.GetXaxis().SetNdivisions(506)

	if blind == True:
		histogram.GetXaxis().SetLabelSize(0.045)
		histogram.GetXaxis().SetTitleSize(0.055)
		histogram.GetYaxis().SetLabelSize(0.045)
		histogram.GetYaxis().SetTitleSize(0.055)
		histogram.GetYaxis().SetTitleOffset(1.15)
		histogram.GetXaxis().SetNdivisions(506)
	else:
		histogram.GetYaxis().SetLabelSize(0.07)
		histogram.GetYaxis().SetTitleSize(0.08)
		histogram.GetYaxis().SetTitleOffset(.71)
	if 'YLD' in iPlot: histogram.GetXaxis().LabelsOption("u")

	if 'nB0' in histogram.GetName() and 'minMlb' in histogram.GetName() and 'YLD' not in iPlot: histogram.GetXaxis().SetTitle("min[M(l,j)], j#neqb [GeV]")
	#if 'JetPt' in histogram.GetName() or 'JetEta' in histogram.GetName(): histogram.GetYaxis().SetTitle(histogram.GetYaxis().GetTitle().replace("Events","Jets"))
	#histogram.GetYaxis().CenterTitle()
	histogram.SetMinimum(0.001)
	if region=='PS': histogram.SetMinimum(0.0101)
	if not yLog: 
		histogram.SetMinimum(0.015)
	if yLog:
		uPad.SetLogy()
		histogram.SetMaximum(1e3*themax)
	else: 
		if 'YLD' in iPlot: histogram.SetMaximum(1.3*histogram.GetMaximum())
		else: histogram.SetMaximum(1.3*histogram.GetMaximum())
		
def formatLowerHist(histogram,disc):
	histogram.GetXaxis().SetLabelSize(.12)
	histogram.GetXaxis().SetTitleSize(0.15)
	histogram.GetXaxis().SetTitleOffset(0.95)
	histogram.GetXaxis().SetNdivisions(506)

	if 'NTJets' in disc: histogram.GetXaxis().SetNdivisions(5)
	elif 'NWJets' in disc: histogram.GetXaxis().SetNdivisions(5)
	elif 'NBJets' in disc: histogram.GetXaxis().SetNdivisions(6,rt.kFALSE)
	else: histogram.GetXaxis().SetNdivisions(506)
	if 'NTJets' in disc or 'NWJets' in disc or 'NBJets' in disc or 'NJets' in disc: histogram.GetXaxis().SetLabelSize(0.15)

	histogram.GetYaxis().SetLabelSize(0.12)
	histogram.GetYaxis().SetTitleSize(0.14)
	histogram.GetYaxis().SetTitleOffset(.37)
	histogram.GetYaxis().SetTitle('Data/Bkg')
	histogram.GetYaxis().SetNdivisions(506)
	if doRealPull: histogram.GetYaxis().SetRangeUser(min(-2.99,0.8*histogram.GetBinContent(histogram.GetMaximumBin())),max(2.99,1.2*histogram.GetBinContent(histogram.GetMaximumBin())))
	#else: histogram.GetYaxis().SetRangeUser(0.45,1.55)#0,2.99)
	else: histogram.GetYaxis().SetRangeUser(0.01,1.99)#0,2.99)
	histogram.GetYaxis().CenterTitle()

if not os.path.exists(templateDir+tempsig):
	print "ERROR: File does not exits: "+templateDir+tempsig
	os._exit(1)
print "READING: "+templateDir+tempsig
RFiles = {}
for sig in sigs: RFiles[sig] = rt.TFile(templateDir+tempsig.replace(sigs[-1],sig))

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.lumi_13TeV= "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.extra2Text = "Preliminary"
CMS_lumi.lumi_sqrtS = str(lumi)+" (14 TeV)" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 600; 
W_ref = 800; 
W = W_ref
H = H_ref

iPeriod = 0 #see CMS_lumi.py module for usage!

# references for T, B, L, R
T = 0.10*H_ref
B = 0.35*H_ref 
if blind == True: B = 0.12*H_ref
L = 0.12*W_ref
R = 0.05*W_ref

tagPosX = 0.40#0.76
tagPosY = 0.68#0.50
if not blind: tagPosY-=0.1

table = []
table.append(['break'])
table.append(['Categories','prob_KS','prob_KS_X','prob_chi2','chi2','ndof'])
table.append(['break'])
bkghists = {}
bkghistsmerged = {}
sighists = {}
sighistsmerged = {}
systHists = {}
totBkgTemp1 = {}
totBkgTemp2 = {}
totBkgTemp3 = {}
for tag in tagList:
	tagStr='nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]
	modTag = tagStr[tagStr.find('nT'):tagStr.find('nJ')-3]
	for isEM in isEMlist:
		histPrefix=iPlot+'_'+lumiInTemplates+'fbinv_'
		catStr='is'+isEM+'_'+tagStr
		catStr = catStr.replace('nT0p_','').replace('nW0p_','').replace('nB0p_','').replace('_nJ0p','')
		histPrefix+=catStr
		print histPrefix
		totBkg = 0.
		for proc in bkgProcList: 
			try:
				bkghists[proc+catStr] = RFiles[sigs[-1]].Get(histPrefix+'__'+proc).Clone()
				totBkg += bkghists[proc+catStr].Integral()
			except:
				print "There is no "+proc+"!!! Skipping it....."
				pass
		hData = RFiles[sigs[-1]].Get(histPrefix+'__DATA').Clone()
		if doChi2KStests:
			hData_test = RFiles[sigs[-1]].Get(histPrefix+'__DATA').Clone()
			bkgHT_test = bkghists[bkgProcList[0]+catStr].Clone()
			for proc in bkgProcList:
				if proc==bkgProcList[0]: continue
				try: bkgHT_test.Add(bkghists[proc+catStr])
				except: pass
			print hData_test.Integral(),bkgHT_test.Integral()
		for sig in sigs: 
			sighists[sig+catStr] = RFiles[sig].Get(histPrefix+'__sig').Clone(histPrefix+'__'+sig)
			sighists[sig+catStr].Scale(xsec[sig])
		if doNormByBinWidth:
			for proc in bkgProcList:
				try: normByBinWidth(bkghists[proc+catStr])
				except: pass
			for sig in sigs: normByBinWidth(sighists[sig+catStr])
			normByBinWidth(hData)

		if doAllSys:
			q2list = []
			if doQ2sys: q2list=['q2']
			print systematicList
			for syst in systematicList+q2list:
				print syst
				for ud in ['minus','plus']:
					for proc in bkgProcList:
						try: 
							systHists[proc+catStr+syst+ud] = RFiles[sigs[-1]].Get(histPrefix+'__'+proc+'__'+syst+'__'+ud).Clone()
							if doNormByBinWidth: normByBinWidth(systHists[proc+catStr+syst+ud])
						except: pass

		bkgHT = bkghists[bkgProcList[0]+catStr].Clone()
		for proc in bkgProcList:
			if proc==bkgProcList[0]: continue
			try: bkgHT.Add(bkghists[proc+catStr])
			except: pass

		totBkgTemp1[catStr] = rt.TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapeOnly'))
		totBkgTemp2[catStr] = rt.TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapePlusNorm'))
		totBkgTemp3[catStr] = rt.TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'All'))
		
		for ibin in range(1,bkghists[bkgProcList[0]+catStr].GetNbinsX()+1):
			errorUp = 0.
			errorDn = 0.
			errorStatOnly = bkgHT.GetBinError(ibin)**2
			errorNorm = 0.
			for proc in bkgProcList:
				try: errorNorm += getNormUnc(bkghists[proc+catStr],ibin,modelingSys[proc])
				except Exception as e: 
					print '===>>> WARNING! Exception occurred on line '+str(sys.exc_info()[-1].tb_lineno)+'. Passing ...'
					pass

			if doAllSys:
				q2list=[]
				if doQ2sys: q2list=['q2']
				for syst in systematicList+q2list:
					for proc in bkgProcList:
						try:
							errorPlus = systHists[proc+catStr+syst+'plus'].GetBinContent(ibin)-bkghists[proc+catStr].GetBinContent(ibin)
							errorMinus = bkghists[proc+catStr].GetBinContent(ibin)-systHists[proc+catStr+syst+'minus'].GetBinContent(ibin)
							if errorPlus > 0: errorUp += errorPlus**2
							else: errorDn += errorPlus**2
							if errorMinus > 0: errorDn += errorMinus**2
							else: errorUp += errorMinus**2
						except: pass

			totBkgTemp1[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorStatOnly))
			totBkgTemp1[catStr].SetPointEYlow(ibin-1, math.sqrt(errorStatOnly))
			totBkgTemp2[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorStatOnly+errorNorm))
			totBkgTemp2[catStr].SetPointEYlow(ibin-1, math.sqrt(errorStatOnly+errorNorm))
			totBkgTemp3[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatOnly))
			totBkgTemp3[catStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm+errorStatOnly))
			
		if doChi2KStests:
			for ibin in range(1, bkgHT_test.GetNbinsX()+1):
				bkgHT_test.SetBinError(ibin,(totBkgTemp3[catStr].GetErrorYlow(ibin-1) + totBkgTemp3[catStr].GetErrorYhigh(ibin-1))/2 )
			prob_KS = bkgHT_test.KolmogorovTest(hData_test)
			prob_KS_X = bkgHT_test.KolmogorovTest(hData_test,"X")
			prob_chi2 = hData_test.Chi2Test(bkgHT_test,"UW")
			chi2 = hData_test.Chi2Test(bkgHT_test,"UW CHI2")
			if hData_test.Chi2Test(bkgHT_test,"UW CHI2/NDF")!=0: ndof = int(hData_test.Chi2Test(bkgHT_test,"UW CHI2")/hData_test.Chi2Test(bkgHT_test,"UW CHI2/NDF"))
			else: ndof = 0
			print '/'*80,'\n','*'*80
			print histPrefix+'_KS =',prob_KS
			print 'WARNING: KS test works on unbinned distributions. For binned histograms, see NOTE3 at https://root.cern.ch/doc/master/classTH1.html#a2747cabe9ebe61c2fdfd74ff307cef3a'
			print '*'*80,'\n','/'*80,'\n','*'*80
			print histPrefix+'_Chi2Test:'
			print "p-value =",prob_chi2,"CHI2/NDF",chi2,"/",ndof
			print '*'*80,'\n','/'*80
			table.append([catStr,prob_KS,prob_KS_X,prob_chi2,chi2,ndof])
		
		bkgHTgerr = totBkgTemp3[catStr].Clone()

		scaleFacts = {}
		for sig in sigs: 
			scaleFacts[sig] = int(bkgHT.GetMaximum()/sighists[sig+catStr].GetMaximum()) - int(bkgHT.GetMaximum()/sighists[sig+catStr].GetMaximum()) % 10
			if scaleFacts[sig]==0: scaleFacts[sig]=int(bkgHT.GetMaximum()/sighists[sig+catStr].GetMaximum())
			if scaleFacts[sig]==0: scaleFacts[sig]=1
			if sigScaleFact>0: scaleFacts[sig]=sigScaleFact
			if not scaleSignals: scaleFacts[sig]=1
			sighists[sig+catStr].Scale(scaleFacts[sig])
			
                ############################################################
		############## Making Plots of e+jets, mu+jets and e/mu+jets 
                ############################################################
		
		drawQCD = False
		try: drawQCD = bkghists['qcd'+catStr].Integral()/bkgHT.Integral()>.005 #don't plot QCD if it is less than 0.5%
		except: pass

		stackbkgHT = rt.THStack("stackbkgHT","")
		bkgProcListNew = bkgProcList[:]
		if region=='WJCR':
			bkgProcListNew[bkgProcList.index("top")],bkgProcListNew[bkgProcList.index("ewk")]=bkgProcList[bkgProcList.index("ewk")],bkgProcList[bkgProcList.index("top")]
		for proc in bkgProcListNew:
			try: 
				if drawQCD or proc!='qcd': stackbkgHT.Add(bkghists[proc+catStr])
			except: pass
			
		for proc in bkgProcList:
			try: 
				bkghists[proc+catStr].SetLineColor(bkgHistColors[proc])
				bkghists[proc+catStr].SetFillColor(bkgHistColors[proc])
				bkghists[proc+catStr].SetLineWidth(2)
			except: pass
		if drawYields: 
			bkgHT.SetMarkerSize(4)
			bkgHT.SetMarkerColor(rt.kRed)

		for sig in sigs:
			sighists[sig+catStr].SetLineColor(sigColors[sig])
			sighists[sig+catStr].SetLineStyle(sigLines[sig])#5)
			sighists[sig+catStr].SetFillStyle(0)
			sighists[sig+catStr].SetLineWidth(3)
		
		if not drawYields: hData.SetMarkerStyle(20)
		hData.SetMarkerSize(1.2)
		hData.SetMarkerColor(rt.kBlack)
		hData.SetLineWidth(2)
		hData.SetLineColor(rt.kBlack)
		if drawYields: hData.SetMarkerSize(4)

		bkgHTgerr.SetFillStyle(3004)
		bkgHTgerr.SetFillColor(rt.kBlack)
		bkgHTgerr.SetLineColor(rt.kBlack)

		c1 = rt.TCanvas("c1","c1",50,50,W,H)
		c1.SetFillColor(0)
		c1.SetBorderMode(0)
		c1.SetFrameFillStyle(0)
		c1.SetFrameBorderMode(0)
		#c1.SetTickx(0)
		#c1.SetTicky(0)
	
		yDiv=0.35
		if blind == True: yDiv=0.0
		uPad=rt.TPad("uPad","",0,yDiv,1,1) #for actual plots
	
		uPad.SetLeftMargin( L/W )
		uPad.SetRightMargin( R/W )
		uPad.SetTopMargin( T/H )
		uPad.SetBottomMargin( 0.01 )
		if blind == True: uPad.SetBottomMargin( B/H )
	
		uPad.SetFillColor(0)
		uPad.SetBorderMode(0)
		uPad.SetFrameFillStyle(0)
		uPad.SetFrameBorderMode(0)
		#uPad.SetTickx(0)
		#uPad.SetTicky(0)
		uPad.Draw()
		if blind == False:
			lPad=rt.TPad("lPad","",0,0,1,yDiv) #for sigma runner

			lPad.SetLeftMargin( L/W )
			lPad.SetRightMargin( R/W )
			lPad.SetTopMargin( 0.01 )
			lPad.SetBottomMargin( B/H )

			lPad.SetGridy()
			lPad.SetFillColor(0)
			lPad.SetBorderMode(0)
			lPad.SetFrameFillStyle(0)
			lPad.SetFrameBorderMode(0)
			#lPad.SetTickx(0)
			#lPad.SetTicky(0)
			lPad.Draw()
		if not doNormByBinWidth: hData.SetMaximum(1.2*max(hData.GetMaximum(),bkgHT.GetMaximum()))
		#hData.SetMinimum(0.015)
		hData.SetTitle("")
		if doNormByBinWidth: hData.GetYaxis().SetTitle("< Events / GeV >")
		elif len(isRebinned)==0 or '1p1' in isRebinned: 
			binWidth = int(hData.GetBinLowEdge(2)-hData.GetBinLowEdge(1))
			hData.GetYaxis().SetTitle("Events / "+str(binWidth)+ " GeV")
		elif len(isRebinned)>0: hData.GetYaxis().SetTitle("Events / bin")
		else: hData.GetYaxis().SetTitle("Events / bin")
		uPad.cd()
		hData.SetTitle("")
		if compareShapes: 
			for sig in sigs: sighists[sig+catStr].Scale(totBkg/sighists[sig+catStr].Integral())
		if blind: 
			if doNormByBinWidth: sighists[sigs[-1]+catStr].GetYaxis().SetTitle("< Events / GeV >")
			elif len(isRebinned)==0 or '1p1' in isRebinned: 
				binWidth = int(sighists[sigs[-1]+catStr].GetBinLowEdge(2)-sighists[sigs[-1]+catStr].GetBinLowEdge(1))
				sighists[sigs[-1]+catStr].GetYaxis().SetTitle("Events / "+str(binWidth)+ " GeV")
			elif isRebinned!='': sighists[sigs[-1]+catStr].GetYaxis().SetTitle("Events / bin")
			else: sighists[sigs[-1]+catStr].GetYaxis().SetTitle("Events / bin")
			formatUpperHist(sighists[sigs[-1]+catStr],stackbkgHT.GetMaximum())
			#sighists[sigs[-1]+catStr].SetMaximum(hData.GetMaximum())
			sighists[sigs[-1]+catStr].Draw("HIST")
		else: 
			formatUpperHist(hData,hData.GetMaximum())
			if 'rebinned_stat0p' in isRebinned: hData.Draw("esamex1")
			else: hData.Draw("esamex0")
		stackbkgHT.Draw("SAME HIST")
		if drawYields: 
			rt.gStyle.SetPaintTextFormat("1.0f")
			bkgHT.Draw("SAME TEXT90")
		sighists[sigs[-1]+catStr].Draw("SAME HIST")
		for sig in sigs: 
			if sig!=sigs[-1]: sighists[sig+catStr].Draw("SAME HIST")
		if not blind: 
			if 'rebinned_stat0p' in isRebinned: hData.Draw("esamex1")
			else: hData.Draw("esamex0") #redraw data so its not hidden
			if drawYields: hData.Draw("SAME TEXT00") 
		uPad.RedrawAxis()
		bkgHTgerr.Draw("SAME E2")
		
		chLatex = rt.TLatex()
		chLatex.SetNDC()
		chLatex.SetTextSize(0.05)
		chLatex.SetTextAlign(21) # align center
		flvString = ''
		tagString = ''
# 		if isEM=='LT': flvString+='|#DeltaY(j_{1},j_{2})| #leq 1'#'e+jets'
# 		if isEM=='GT': flvString+='|#DeltaY(j_{1},j_{2})| > 1'#'#mu+jets'
		chnString = 'Fully hadronic'
		if isEM=='E': flvString+='#Deltay < 1'
		if isEM=='M': flvString+='#Deltay > 1'
		if tag[0]!='0p': 
			if 'p' in tag[0]: tagString+='#geq'+tag[0][:-1]+' t, '
			else: tagString+=tag[0]+' t, '
		if tag[1]!='0p': 
			if 'p' in tag[1]: tagString+='#geq'+tag[1][:-1]+' W, '
			else: tagString+=tag[1]+' W, '
		if tag[2]!='0p': 
			if 'p' in tag[2]: tagString+='#geq'+tag[2][:-1]+' b, '
			else: tagString+=tag[2]+' b, '
		if tag[3]!='0p': 
			if 'p' in tag[3]: tagString+='#geq'+tag[3][:-1]+' j'
			else: tagString+=tag[3]+' j'
		if tagString.endswith(', '): tagString = tagString[:-2]
		if tagString!='': tagString+=' tag'
		chLatex.DrawLatex(tagPosX, tagPosY, chnString)
		chLatex.DrawLatex(tagPosX, tagPosY-0.05, flvString)
		chLatex.DrawLatex(tagPosX, tagPosY-0.10, tagString)

		if plotForPAS: leg = rt.TLegend(0.55,0.54,0.9,0.87)
		else: leg = rt.TLegend(0.45,0.54,0.9,0.87)
		rt.SetOwnership( leg, 0 )   # 0 = release (not keep), 1 = keep
		leg.SetShadowColor(0)
		leg.SetFillColor(0)
		leg.SetFillStyle(0)
		leg.SetLineColor(0)
		leg.SetLineStyle(0)
		leg.SetBorderSize(0) 
		if plotForPAS: leg.SetNColumns(1)
		else: leg.SetNColumns(2)
		leg.SetTextFont(62)#42)
		leg.SetColumnSeparation(0.05)
		scaleFactStrs = {}
		for sig in sigs: scaleFactStrs[sig] = ' x'+str(scaleFacts[sig])
		if not scaleSignals:
			for sig in sigs: scaleFactStrs[sig] = ''
		ind=0
		countlegs=0
		if plotForPAS:
			for proc in reversed(bkgProcList):
				try: leg.AddEntry(bkghists[proc+catStr],proclegs[proc],"f")
				except: continue
			while ind<len(sigs):
				try: leg.AddEntry(sighists[sigs[ind]+catStr],siglegs[sigs[ind]]+scaleFactStrs[sigs[ind]],"l")
				except: continue
				ind+=1
		else:
			if not blind:
				leg.AddEntry(hData,proclegs['data'],"ep")
				countlegs+=1
				try: leg.AddEntry(sighists[sigs[ind]+catStr],siglegs[sigs[ind]]+scaleFactStrs[sigs[ind]],"l")
				except: continue
				countlegs+=1
				ind+=1
			for proc in reversed(bkgProcList):
				try: leg.AddEntry(bkghists[proc+catStr],proclegs[proc],"f")
				except: continue
				countlegs+=1
				try: leg.AddEntry(sighists[sigs[ind]+catStr],siglegs[sigs[ind]]+scaleFactStrs[sigs[ind]],"l")
				except: continue
				countlegs+=1
				ind+=1
			while ind<len(sigs):
				leg.AddEntry(0, "", "")
				countlegs+=1
				try: leg.AddEntry(sighists[sigs[ind]+catStr],siglegs[sigs[ind]]+scaleFactStrs[sigs[ind]],"l")
				except: continue
				countlegs+=1
				ind+=1
			if countlegs%2==0: leg.AddEntry(0, "", "")
		leg.AddEntry(bkgHTgerr,"Bkg uncertainty","f")
		leg.Draw("same")

		#draw the lumi text on the canvas
		CMS_lumi.CMS_lumi(uPad, iPeriod, iPos)
	
		uPad.Update()
		uPad.RedrawAxis()
		frame = uPad.GetFrame()
		uPad.Draw()

		if blind == False and not doRealPull:
			lPad.cd()
			pull=hData.Clone("pull")
			pull.Divide(hData, bkgHT)
			for binNo in range(1,hData.GetNbinsX()+1):
				binLbl = binNo-1
				if 'NJets' in iPlot: 
					#if binNo == 1 or binNo == 5 or binNo == 10 or binNo == 15: pull.GetXaxis().SetBinLabel(binNo,str(binNo))
					if binLbl%2 == 0: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
					else: pull.GetXaxis().SetBinLabel(binNo,'')
				if 'NTJets' in iPlot: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
				if 'NWJets' in iPlot: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
				if 'NBJets' in iPlot: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
				if bkgHT.GetBinContent(binNo)!=0:
					pull.SetBinError(binNo,hData.GetBinError(binNo)/bkgHT.GetBinContent(binNo))
			pull.SetMaximum(3)
			pull.SetMinimum(0)
			pull.SetFillColor(1)
			pull.SetLineColor(1)
			formatLowerHist(pull,iPlot)
			pull.Draw("E0")#"E1")
			
			BkgOverBkg = pull.Clone("bkgOverbkg")
			BkgOverBkg.Divide(bkgHT, bkgHT)
			pullUncBandTot=rt.TGraphAsymmErrors(BkgOverBkg.Clone("pulluncTot"))
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pullUncBandTot.SetPointEYhigh(binNo-1,totBkgTemp3[catStr].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandTot.SetPointEYlow(binNo-1,totBkgTemp3[catStr].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
			pullUncBandTot.SetFillStyle(3001)
			pullUncBandTot.SetFillColor(1)
			pullUncBandTot.SetLineColor(1)
			pullUncBandTot.SetMarkerSize(0)
			rt.gStyle.SetHatchesLineWidth(1)
			pullUncBandTot.Draw("SAME E2")
			
			pullUncBandNorm=rt.TGraphAsymmErrors(BkgOverBkg.Clone("pulluncNorm"))
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pullUncBandNorm.SetPointEYhigh(binNo-1,totBkgTemp2[catStr].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandNorm.SetPointEYlow(binNo-1,totBkgTemp2[catStr].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
			pullUncBandNorm.SetFillStyle(3001)
			pullUncBandNorm.SetFillColor(2)
			pullUncBandNorm.SetLineColor(2)
			pullUncBandNorm.SetMarkerSize(0)
			rt.gStyle.SetHatchesLineWidth(1)
			if not doOneBand: pullUncBandNorm.Draw("SAME E2")
			
			pullUncBandStat=rt.TGraphAsymmErrors(BkgOverBkg.Clone("pulluncStat"))
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pullUncBandStat.SetPointEYhigh(binNo-1,totBkgTemp1[catStr].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandStat.SetPointEYlow(binNo-1,totBkgTemp1[catStr].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
			pullUncBandStat.SetFillStyle(3001)
			pullUncBandStat.SetFillColor(3)
			pullUncBandStat.SetLineColor(3)
			pullUncBandStat.SetMarkerSize(0)
			rt.gStyle.SetHatchesLineWidth(1)
			if not doOneBand: pullUncBandStat.Draw("SAME E2")

			pullLegend=rt.TLegend(0.14,0.87,0.85,0.96)
			rt.SetOwnership( pullLegend, 0 )   # 0 = release (not keep), 1 = keep
			pullLegend.SetShadowColor(0)
			pullLegend.SetNColumns(3)
			pullLegend.SetFillColor(0)
			pullLegend.SetFillStyle(0)
			pullLegend.SetLineColor(0)
			pullLegend.SetLineStyle(0)
			pullLegend.SetBorderSize(0)
			pullLegend.SetTextFont(42)
			if not doOneBand: 
				pullLegend.AddEntry(pullUncBandStat , "Bkg uncert (stat)" , "f")
				pullLegend.AddEntry(pullUncBandNorm , "Bkg uncert (stat #oplus norm syst)" , "f")
				pullLegend.AddEntry(pullUncBandTot , "Bkg uncert (stat #oplus all syst)" , "f")
			else: 
				if doAllSys: pullLegend.AddEntry(pullUncBandTot , "Bkg uncert (stat #oplus syst)" , "f")
				else: pullLegend.AddEntry(pullUncBandTot , "Bkg uncert (stat)" , "f")
			#pullLegend.AddEntry(pullQ2up , "Q^{2} Up" , "l")
			#pullLegend.AddEntry(pullQ2dn , "Q^{2} Down" , "l")
			pullLegend.Draw("SAME")
			pull.Draw("SAME")
			lPad.RedrawAxis()

		if blind == False and doRealPull:
			lPad.cd()
			pull=hData.Clone("pull")
			for binNo in range(1,hData.GetNbinsX()+1):
				binLbl = binNo-1
				if 'NJets' in iPlot: 
					#if binNo == 1 or binNo == 5 or binNo == 10 or binNo == 15: pull.GetXaxis().SetBinLabel(binNo,str(binNo))
					if binLbl%2 == 0: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
					else: pull.GetXaxis().SetBinLabel(binNo,'')
				if 'NTJets' in iPlot: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
				if 'NWJets' in iPlot: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
				if 'NBJets' in iPlot: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
				if hData.GetBinContent(binNo)!=0:
					MCerror = 0.5*(totBkgTemp3[catStr].GetErrorYhigh(binNo-1)+totBkgTemp3[catStr].GetErrorYlow(binNo-1))
					pull.SetBinContent(binNo,(hData.GetBinContent(binNo)-bkgHT.GetBinContent(binNo))/math.sqrt(MCerror**2+hData.GetBinError(binNo)**2))
				else: pull.SetBinContent(binNo,0.)
			pull.SetMaximum(3)
			pull.SetMinimum(-3)
			if '53' in sigs[-1]:
				pull.SetFillColor(2)
				pull.SetLineColor(2)
			else:
				pull.SetFillColor(kGray+2)
				pull.SetLineColor(kGray+2)
			formatLowerHist(pull,iPlot)
			pull.GetYaxis().SetTitle('#frac{(obs-bkg)}{uncertainty}')
			pull.Draw("HIST")

		#c1.Write()
		savePrefix = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plots/'
		if not os.path.exists(savePrefix): os.system('mkdir '+savePrefix)
		savePrefix+=histPrefix.replace('isE','isLT').replace('isM','isGT')+isRebinned.replace('_rebinned_stat1p1','')+saveKey
		if '000p0fbinv' in savePrefix: savePrefix=savePrefix.replace('000p0fbinv','abinv')
		if nttaglist[0]=='0p': savePrefix=savePrefix.replace('nT0p_','')
		if nWtaglist[0]=='0p': savePrefix=savePrefix.replace('nW0p_','')
		if nbtaglist[0]=='0p': savePrefix=savePrefix.replace('nB0p_','')
		if njetslist[0]=='0p': savePrefix=savePrefix.replace('nJ0p_','')
		if doNormByBinWidth: savePrefix+='_NBBW'
		if yLog: savePrefix+='_logy'
# 		if blind: savePrefix+='_blind'
# 		else:
# 			if doRealPull: savePrefix+='_pull'
# 			if doOneBand: savePrefix+='_totBand'
		if compareShapes: savePrefix+='_shp'

		c1.SaveAs(savePrefix+".pdf")
		c1.SaveAs(savePrefix+".png")
		c1.SaveAs(savePrefix+".eps")
		#c1.SaveAs(savePrefix+".root")
		#c1.SaveAs(savePrefix+".C")
		for proc in bkgProcList:
			try: del bkghists[proc+catStr]
			except: pass
					
	# Making plots for e+jets/mu+jets combined #
	histPrefixE = iPlot+'_'+lumiInTemplates+'fbinv_is'+isEMlist[0]+'_'+tagStr
	histPrefixM = iPlot+'_'+lumiInTemplates+'fbinv_is'+isEMlist[1]+'_'+tagStr
	histPrefixE = histPrefixE.replace('nT0p_','').replace('nW0p_','').replace('nB0p_','').replace('_nJ0p','')
	histPrefixM = histPrefixM.replace('nT0p_','').replace('nW0p_','').replace('nB0p_','').replace('_nJ0p','')
	print histPrefixE, histPrefixM
	totBkgMerged = 0.
	for proc in bkgProcList:
		try: 
			bkghistsmerged[proc+'isL'+tagStr] = RFiles[sigs[-1]].Get(histPrefixE+'__'+proc).Clone()
			bkghistsmerged[proc+'isL'+tagStr].Add(RFiles[sigs[-1]].Get(histPrefixM+'__'+proc))
			totBkgMerged += bkghistsmerged[proc+'isL'+tagStr].Integral()
		except:pass
	hDatamerged = RFiles[sigs[-1]].Get(histPrefixE+'__DATA').Clone()
	hDatamerged.Add(RFiles[sigs[-1]].Get(histPrefixM+'__DATA').Clone())
	if doChi2KStests:
		hDatamerged_test = RFiles[sigs[-1]].Get(histPrefixE+'__DATA').Clone()
		hDatamerged_test.Add(RFiles[sigs[-1]].Get(histPrefixM+'__DATA').Clone())
		bkgHTmerged_test = bkghistsmerged[bkgProcList[0]+'isL'+tagStr].Clone()
		for proc in bkgProcList:
			if proc==bkgProcList[0]: continue
			try: bkgHTmerged_test.Add(bkghistsmerged[proc+'isL'+tagStr])
			except: pass
	for sig in sigs: 
		sighistsmerged[sig+'isL'+tagStr] = RFiles[sig].Get(histPrefixE+'__sig').Clone(histPrefixE+'__'+sig+'merged')
		sighistsmerged[sig+'isL'+tagStr].Add(RFiles[sig].Get(histPrefixM+'__sig').Clone())
		sighistsmerged[sig+'isL'+tagStr].Scale(xsec[sig])
	if doNormByBinWidth:
		for proc in bkgProcList:
			try: normByBinWidth(bkghistsmerged[proc+'isL'+tagStr])
			except: pass
		for sig in sigs: normByBinWidth(sighistsmerged[sig+'isL'+tagStr])
		normByBinWidth(hDatamerged)

	if doAllSys:
		q2list=[]
		if doQ2sys: q2list=['q2']
		for syst in systematicList+q2list:
			for ud in ['minus','plus']:
				for proc in bkgProcList:
					try: 
						systHists[proc+'isL'+tagStr+syst+ud] = systHists[proc+'isE_'+tagStr+syst+ud].Clone()
						systHists[proc+'isL'+tagStr+syst+ud].Add(systHists[proc+'isM_'+tagStr+syst+ud])
					except: pass

	bkgHTmerged = bkghistsmerged[bkgProcList[0]+'isL'+tagStr].Clone()
	for proc in bkgProcList:
		if proc==bkgProcList[0]: continue
		try: bkgHTmerged.Add(bkghistsmerged[proc+'isL'+tagStr])
		except: pass

	totBkgTemp1['isL'+tagStr] = rt.TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'shapeOnly'))
	totBkgTemp2['isL'+tagStr] = rt.TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'shapePlusNorm'))
	totBkgTemp3['isL'+tagStr] = rt.TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'All'))
	
	for ibin in range(1,bkghistsmerged[bkgProcList[0]+'isL'+tagStr].GetNbinsX()+1):
		errorUp = 0.
		errorDn = 0.
		errorStatOnly = bkgHTmerged.GetBinError(ibin)**2
		errorNorm = 0.
		for proc in bkgProcList:
			try: errorNorm += getNormUnc(bkghistsmerged[proc+'isL'+tagStr],ibin,modelingSys[proc])
			except Exception as e: 
				print '===>>> WARNING! Exception occurred on line '+str(sys.exc_info()[-1].tb_lineno)+'. Passing ...'
				pass

		if doAllSys:
			q2list=[]
			if doQ2sys: q2list=['q2']
			for syst in systematicList+q2list:
				for proc in bkgProcList:
					try:
						errorPlus = systHists[proc+'isL'+tagStr+syst+'plus'].GetBinContent(ibin)-bkghistsmerged[proc+'isL'+tagStr].GetBinContent(ibin)
						errorMinus = bkghistsmerged[proc+'isL'+tagStr].GetBinContent(ibin)-systHists[proc+'isL'+tagStr+syst+'minus'].GetBinContent(ibin)
						if errorPlus > 0: errorUp += errorPlus**2
						else: errorDn += errorPlus**2
						if errorMinus > 0: errorDn += errorMinus**2
						else: errorUp += errorMinus**2
					except: pass

		totBkgTemp1['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorStatOnly))
		totBkgTemp1['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorStatOnly))
		totBkgTemp2['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorStatOnly+errorNorm))
		totBkgTemp2['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorStatOnly+errorNorm))
		totBkgTemp3['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatOnly))
		totBkgTemp3['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm+errorStatOnly))
	
	if doChi2KStests:
		for ibin in range(1, bkgHTmerged_test.GetNbinsX()+1):
			bkgHTmerged_test.SetBinError(ibin,(totBkgTemp3['isL'+tagStr].GetErrorYlow(ibin-1) + totBkgTemp3['isL'+tagStr].GetErrorYhigh(ibin-1))/2 )

		prob_KS = bkgHTmerged_test.KolmogorovTest(hDatamerged_test)
		prob_KS_X = bkgHTmerged_test.KolmogorovTest(hDatamerged_test,"X")
		prob_chi2 = hDatamerged_test.Chi2Test(bkgHTmerged_test,"UW")
		chi2 = hDatamerged_test.Chi2Test(bkgHTmerged_test,"UW CHI2")
		if hDatamerged_test.Chi2Test(bkgHTmerged_test,"UW CHI2/NDF")!=0: ndof = int(hDatamerged_test.Chi2Test(bkgHTmerged_test,"UW CHI2")/hDatamerged_test.Chi2Test(bkgHTmerged_test,"UW CHI2/NDF"))
		else: ndof = 0
		print '/'*80,'\n','*'*80
		print histPrefixE.replace('isE','isL')+'_KS =',prob_KS
		print 'WARNING: KS test works on unbinned distributions. For binned histograms, see NOTE3 at https://root.cern.ch/doc/master/classTH1.html#a2747cabe9ebe61c2fdfd74ff307cef3a'
		print '*'*80,'\n','/'*80,'\n','*'*80
		print histPrefixE.replace('isE','isL')+'_Chi2Test:'
		print "p-value =",prob_chi2,"CHI2/NDF",chi2,"/",ndof
		print '*'*80,'\n','/'*80
		table.append(['isL_'+tagStr,prob_KS,prob_KS_X,prob_chi2,chi2,ndof])

	bkgHTgerrmerged = totBkgTemp3['isL'+tagStr].Clone()

	scaleFactsmerged = {}
	for sig in sigs: 
		scaleFactsmerged[sig] = int(bkgHTmerged.GetMaximum()/sighistsmerged[sig+'isL'+tagStr].GetMaximum()) - int(bkgHTmerged.GetMaximum()/sighistsmerged[sig+'isL'+tagStr].GetMaximum()) % 10
		if scaleFactsmerged[sig]==0: scaleFactsmerged[sig]=int(bkgHTmerged.GetMaximum()/sighistsmerged[sig+'isL'+tagStr].GetMaximum())
		if scaleFactsmerged[sig]==0: scaleFactsmerged[sig]=1
		if sigScaleFact>0: scaleFactsmerged[sig]=sigScaleFact
		if not scaleSignals: scaleFactsmerged[sig]=1
		sighistsmerged[sig+'isL'+tagStr].Scale(scaleFactsmerged[sig])
	
	drawQCDmerged = False
	try: drawQCDmerged = bkghistsmerged['qcdisL'+tagStr].Integral()/bkgHTmerged.Integral()>.005
	except: pass

	stackbkgHTmerged = rt.THStack("stackbkgHTmerged","")
	bkgProcListNew = bkgProcList[:]
	if region=='WJCR':
		bkgProcListNew[bkgProcList.index("top")],bkgProcListNew[bkgProcList.index("ewk")]=bkgProcList[bkgProcList.index("ewk")],bkgProcList[bkgProcList.index("top")]
	for proc in bkgProcListNew:
		try: 
			if drawQCDmerged or proc!='qcd': stackbkgHTmerged.Add(bkghistsmerged[proc+'isL'+tagStr])
		except: pass

	for proc in bkgProcList:
		try: 
			bkghistsmerged[proc+'isL'+tagStr].SetLineColor(bkgHistColors[proc])
			bkghistsmerged[proc+'isL'+tagStr].SetFillColor(bkgHistColors[proc])
			bkghistsmerged[proc+'isL'+tagStr].SetLineWidth(2)
		except: pass
	if drawYields: 
		bkgHTmerged.SetMarkerSize(4)
		bkgHTmerged.SetMarkerColor(rt.kRed)
	
	for sig in sigs:
		sighistsmerged[sig+'isL'+tagStr].SetLineColor(sigColors[sig])
		sighistsmerged[sig+'isL'+tagStr].SetLineStyle(sigLines[sig])#5)
		sighistsmerged[sig+'isL'+tagStr].SetFillStyle(0)
		sighistsmerged[sig+'isL'+tagStr].SetLineWidth(3)
	
	if not drawYields: hDatamerged.SetMarkerStyle(20)
	hDatamerged.SetMarkerSize(1.2)
	hDatamerged.SetMarkerColor(rt.kBlack)
	hDatamerged.SetLineWidth(2)
	hDatamerged.SetLineColor(rt.kBlack)
	if drawYields: hDatamerged.SetMarkerSize(4)

	bkgHTgerrmerged.SetFillStyle(3004)
	bkgHTgerrmerged.SetFillColor(rt.kBlack)
	bkgHTgerrmerged.SetLineColor(rt.kBlack)

	#bkghistsmerged['ttbarisL'+tagStr].Fit("gaus","","",150.,200.)
	#bkghistsmerged['ttbarisL'+tagStr+'Fit'] = bkghistsmerged['ttbarisL'+tagStr].GetFunction("gaus").Clone('ttbarisL'+tagStr+'Fit')

	c1merged = rt.TCanvas("c1merged","c1merged",50,50,W,H)
	c1merged.SetFillColor(0)
	c1merged.SetBorderMode(0)
	c1merged.SetFrameFillStyle(0)
	c1merged.SetFrameBorderMode(0)
	#c1merged.SetTickx(0)
	#c1merged.SetTicky(0)
	
	yDiv=0.35
	if blind == True: yDiv=0.0
	uPad=rt.TPad("uPad","",0,yDiv,1,1) #for actual plots
	
	uPad.SetLeftMargin( L/W )
	uPad.SetRightMargin( R/W )
	uPad.SetTopMargin( T/H )
	uPad.SetBottomMargin( 0.01 )
	if blind == True: uPad.SetBottomMargin( B/H )
	
	uPad.SetFillColor(0)
	uPad.SetBorderMode(0)
	uPad.SetFrameFillStyle(0)
	uPad.SetFrameBorderMode(0)
	#uPad.SetTickx(0)
	#uPad.SetTicky(0)
	uPad.Draw()
	if blind == False:
		lPad=rt.TPad("lPad","",0,0,1,yDiv) #for sigma runner

		lPad.SetLeftMargin( L/W )
		lPad.SetRightMargin( R/W )
		lPad.SetTopMargin( 0.01 )
		lPad.SetBottomMargin( B/H )

		lPad.SetGridy()
		lPad.SetFillColor(0)
		lPad.SetBorderMode(0)
		lPad.SetFrameFillStyle(0)
		lPad.SetFrameBorderMode(0)
		#lPad.SetTickx(0)
		#lPad.SetTicky(0)
		lPad.Draw()
	if not doNormByBinWidth: hDatamerged.SetMaximum(1.2*max(hDatamerged.GetMaximum(),bkgHTmerged.GetMaximum()))
	#hDatamerged.SetMinimum(0.015)
	if doNormByBinWidth: hDatamerged.GetYaxis().SetTitle("< Events / GeV >")
	elif len(isRebinned)==0 or '1p1' in isRebinned: 
		binWidth = int(hDatamerged.GetBinLowEdge(2)-hDatamerged.GetBinLowEdge(1))
		hDatamerged.GetYaxis().SetTitle("Events / "+str(binWidth)+ " GeV")
	elif len(isRebinned)>0: hDatamerged.GetYaxis().SetTitle("Events / bin")
	else: hDatamerged.GetYaxis().SetTitle("Events / bin")
	uPad.cd()
	hDatamerged.SetTitle("")
	stackbkgHTmerged.SetTitle("")
	if compareShapes: 
		for sig in sigs: sighistsmerged[sig+'isL'+tagStr].Scale(totBkg/sighistsmerged[sig+'isL'+tagStr].Integral())
	if blind: 
		if doNormByBinWidth: sighistsmerged[sigs[-1]+'isL'+tagStr].GetYaxis().SetTitle("< Events / GeV >")
		elif len(isRebinned)==0 or '1p1' in isRebinned: 
			binWidth = int(sighistsmerged[sigs[-1]+'isL'+tagStr].GetBinLowEdge(2)-sighistsmerged[sigs[-1]+'isL'+tagStr].GetBinLowEdge(1))
			sighistsmerged[sigs[-1]+'isL'+tagStr].GetYaxis().SetTitle("Events / "+str(binWidth)+ " GeV")
		elif isRebinned!='': sighistsmerged[sigs[-1]+'isL'+tagStr].GetYaxis().SetTitle("Events / bin")
		else: sighistsmerged[sigs[-1]+'isL'+tagStr].GetYaxis().SetTitle("Events / bin")
		formatUpperHist(sighistsmerged[sigs[-1]+'isL'+tagStr],bkgHTmerged.GetMaximum())
		#sighistsmerged[sigs[-1]+'isL'+tagStr].SetMaximum(hDatamerged.GetMaximum())
		sighistsmerged[sigs[-1]+'isL'+tagStr].Draw("HIST")
	else: 
		formatUpperHist(hDatamerged,hDatamerged.GetMaximum())
		if 'rebinned_stat0p' in isRebinned: hDatamerged.Draw("esamex1")
		else: hDatamerged.Draw("esamex0")
	stackbkgHTmerged.Draw("SAME HIST")
	if drawYields: 
		rt.gStyle.SetPaintTextFormat("1.0f")
		bkgHTmerged.Draw("SAME TEXT90")
	sighistsmerged[sigs[-1]+'isL'+tagStr].Draw("SAME HIST")
	for sig in sigs: 
		if sig!=sigs[-1]: sighistsmerged[sig+'isL'+tagStr].Draw("SAME HIST")
	if not blind: 
		if 'rebinned_stat0p' in isRebinned: hDatamerged.Draw("esamex1")
		else: hDatamerged.Draw("esamex0") #redraw data so its not hidden
		if drawYields: hDatamerged.Draw("SAME TEXT00") 
	uPad.RedrawAxis()
	bkgHTgerrmerged.Draw("SAME E2")
	#bkghistsmerged['ttbarisL'+tagStr+'Fit'].Draw("SAME HIST")
	
	chLatexmerged = rt.TLatex()
	chLatexmerged.SetNDC()
	chLatexmerged.SetTextSize(0.05)
	chLatexmerged.SetTextAlign(21) # align center
	flvString = 'Fully hadronic'#'e/#mu+jets'
	tagString = ''
	if tag[0]!='0p':
		if 'p' in tag[0]: tagString+='#geq'+tag[0][:-1]+' t, '
		else: tagString+=tag[0]+' t, '
	if tag[1]!='0p':
		if 'p' in tag[1]: tagString+='#geq'+tag[1][:-1]+' W, '
		else: tagString+=tag[1]+' W, '
	if tag[2]!='0p':
		if 'p' in tag[2]: tagString+='#geq'+tag[2][:-1]+' b, '
		else: tagString+=tag[2]+' b, '
	if tag[3]!='0p':
		if 'p' in tag[3]: tagString+='#geq'+tag[3][:-1]+' j'
		else: tagString+=tag[3]+' j'
	if tagString.endswith(', '): tagString = tagString[:-2]
	if tagString!='': tagString+=' tag'
	chLatexmerged.DrawLatex(tagPosX, tagPosY, flvString)
	chLatexmerged.DrawLatex(tagPosX, tagPosY-0.05, tagString)

	legmerged = rt.TLegend(0.45,0.54,0.9,0.87)
	rt.SetOwnership( legmerged, 0 )   # 0 = release (not keep), 1 = keep
	legmerged.SetShadowColor(0)
	legmerged.SetFillColor(0)
	legmerged.SetFillStyle(0)
	legmerged.SetLineColor(0)
	legmerged.SetLineStyle(0)
	legmerged.SetBorderSize(0) 
	legmerged.SetNColumns(2)
	legmerged.SetTextFont(62)#42)
	legmerged.SetColumnSeparation(0.05)
	scaleFactStrs = {}
	for sig in sigs: scaleFactStrs[sig] = ' x'+str(scaleFactsmerged[sig])
	if not scaleSignals:
		for sig in sigs: scaleFactStrs[sig] = ''
	ind=0
	countlegs=0
	if not blind:
		legmerged.AddEntry(hDatamerged,proclegs['data'],"ep")
		countlegs+=1
		try: legmerged.AddEntry(sighistsmerged[sigs[ind]+'isL'+tagStr],siglegs[sigs[ind]]+scaleFactStrs[sigs[ind]],"l")
		except: continue
		countlegs+=1
		ind+=1
	for proc in reversed(bkgProcList):
		try: legmerged.AddEntry(bkghistsmerged[proc+'isL'+tagStr],proclegs[proc],"f")
		except: continue
		countlegs+=1
		try: legmerged.AddEntry(sighistsmerged[sigs[ind]+'isL'+tagStr],siglegs[sigs[ind]]+scaleFactStrs[sigs[ind]],"l")
		except: continue
		countlegs+=1
		ind+=1
	while ind<len(sigs):
		legmerged.AddEntry(0, "", "")
		countlegs+=1
		try: legmerged.AddEntry(sighistsmerged[sigs[ind]+'isL'+tagStr],siglegs[sigs[ind]]+scaleFactStrs[sigs[ind]],"l")
		except: continue
		countlegs+=1
		ind+=1
	if countlegs%2==0: legmerged.AddEntry(0, "", "")
	legmerged.AddEntry(bkgHTgerrmerged,"Bkg uncertainty","f")
	legmerged.Draw("same")

	#draw the lumi text on the canvas
	CMS_lumi.CMS_lumi(uPad, iPeriod, iPos)
	
	uPad.Update()
	uPad.RedrawAxis()
	frame = uPad.GetFrame()
	uPad.Draw()
	
	if blind == False and not doRealPull:
		lPad.cd()
		pullmerged=hDatamerged.Clone("pullmerged")
		pullmerged.Divide(hDatamerged, bkgHTmerged)
		for binNo in range(1,hDatamerged.GetNbinsX()+1):
			binLbl = binNo-1
			if 'NJets' in iPlot: 
				#if binNo == 1 or binNo == 5 or binNo == 10 or binNo == 15: pullmerged.GetXaxis().SetBinLabel(binNo,str(binNo))
				if binLbl%2 == 0: pullmerged.GetXaxis().SetBinLabel(binNo,str(binLbl))
				else: pullmerged.GetXaxis().SetBinLabel(binNo,'')
			if 'NTJets' in iPlot: pullmerged.GetXaxis().SetBinLabel(binNo,str(binLbl))
			if 'NWJets' in iPlot: pullmerged.GetXaxis().SetBinLabel(binNo,str(binLbl))
			if 'NBJets' in iPlot: pullmerged.GetXaxis().SetBinLabel(binNo,str(binLbl))
			if bkgHTmerged.GetBinContent(binNo)!=0:
				pull.SetBinError(binNo,hDatamerged.GetBinError(binNo)/bkgHTmerged.GetBinContent(binNo))
		pullmerged.SetMaximum(3)
		pullmerged.SetMinimum(0)
		pullmerged.SetFillColor(1)
		pullmerged.SetLineColor(1)
		formatLowerHist(pullmerged,iPlot)
		pullmerged.Draw("E0")#"E1")
		
		BkgOverBkgmerged = pullmerged.Clone("bkgOverbkgmerged")
		BkgOverBkgmerged.Divide(bkgHTmerged, bkgHTmerged)
		pullUncBandTotmerged=rt.TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncTotmerged"))
		for binNo in range(0,hDatamerged.GetNbinsX()+2):
			if bkgHTmerged.GetBinContent(binNo)!=0:
				pullUncBandTotmerged.SetPointEYhigh(binNo-1,totBkgTemp3['isL'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
				pullUncBandTotmerged.SetPointEYlow(binNo-1, totBkgTemp3['isL'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
		pullUncBandTotmerged.SetFillStyle(3001)
		pullUncBandTotmerged.SetFillColor(1)
		pullUncBandTotmerged.SetLineColor(1)
		pullUncBandTotmerged.SetMarkerSize(0)
		rt.gStyle.SetHatchesLineWidth(1)
		pullUncBandTotmerged.Draw("SAME E2")
		
		pullUncBandNormmerged=rt.TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncNormmerged"))
		for binNo in range(0,hData.GetNbinsX()+2):
			if bkgHTmerged.GetBinContent(binNo)!=0:
				pullUncBandNormmerged.SetPointEYhigh(binNo-1,totBkgTemp2['isL'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
				pullUncBandNormmerged.SetPointEYlow(binNo-1, totBkgTemp2['isL'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
		pullUncBandNormmerged.SetFillStyle(3001)
		pullUncBandNormmerged.SetFillColor(2)
		pullUncBandNormmerged.SetLineColor(2)
		pullUncBandNormmerged.SetMarkerSize(0)
		rt.gStyle.SetHatchesLineWidth(1)
		if not doOneBand: pullUncBandNormmerged.Draw("SAME E2")
		
		pullUncBandStatmerged=rt.TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncStatmerged"))
		for binNo in range(0,hDatamerged.GetNbinsX()+2):
			if bkgHTmerged.GetBinContent(binNo)!=0:
				pullUncBandStatmerged.SetPointEYhigh(binNo-1,totBkgTemp1['isL'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
				pullUncBandStatmerged.SetPointEYlow(binNo-1, totBkgTemp1['isL'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
		pullUncBandStatmerged.SetFillStyle(3001)
		pullUncBandStatmerged.SetFillColor(3)
		pullUncBandStatmerged.SetLineColor(3)
		pullUncBandStatmerged.SetMarkerSize(0)
		rt.gStyle.SetHatchesLineWidth(1)
		if not doOneBand: pullUncBandStatmerged.Draw("SAME E2")

		pullLegendmerged=rt.TLegend(0.14,0.87,0.85,0.96)
		rt.SetOwnership( pullLegendmerged, 0 )   # 0 = release (not keep), 1 = keep
		pullLegendmerged.SetShadowColor(0)
		pullLegendmerged.SetNColumns(3)
		pullLegendmerged.SetFillColor(0)
		pullLegendmerged.SetFillStyle(0)
		pullLegendmerged.SetLineColor(0)
		pullLegendmerged.SetLineStyle(0)
		pullLegendmerged.SetBorderSize(0)
		pullLegendmerged.SetTextFont(42)
		if not doOneBand: 
			pullLegendmerged.AddEntry(pullUncBandStat , "Bkg uncert (stat)" , "f")
			pullLegendmerged.AddEntry(pullUncBandNorm , "Bkg uncert (stat #oplus norm. syst)" , "f")
			pullLegendmerged.AddEntry(pullUncBandTot , "Bkg uncert (stat #oplus all syst)" , "f")
		else: 
			if doAllSys: pullLegendmerged.AddEntry(pullUncBandTot , "Bkg uncert (stat #oplus syst)" , "f")
			else: pullLegendmerged.AddEntry(pullUncBandTot , "Bkg uncert (stat)" , "f")
		pullLegendmerged.Draw("SAME")
		pullmerged.Draw("SAME")
		lPad.RedrawAxis()

	if blind == False and doRealPull:
		lPad.cd()
		pullmerged=hDatamerged.Clone("pullmerged")
		for binNo in range(1,hDatamerged.GetNbinsX()+1):
			binLbl = binNo-1
			if 'NJets' in iPlot: 
				#if binNo == 1 or binNo == 5 or binNo == 10 or binNo == 15: pullmerged.GetXaxis().SetBinLabel(binNo,str(binNo))
				if binLbl%2 == 0: pullmerged.GetXaxis().SetBinLabel(binNo,str(binLbl))
				else: pullmerged.GetXaxis().SetBinLabel(binNo,'')
			if 'NTJets' in iPlot: pullmerged.GetXaxis().SetBinLabel(binNo,str(binLbl))
			if 'NWJets' in iPlot: pullmerged.GetXaxis().SetBinLabel(binNo,str(binLbl))
			if 'NBJets' in iPlot: pullmerged.GetXaxis().SetBinLabel(binNo,str(binLbl))
			if hDatamerged.GetBinContent(binNo)!=0:
				MCerror = 0.5*(totBkgTemp3['isL'+tagStr].GetErrorYhigh(binNo-1)+totBkgTemp3['isL'+tagStr].GetErrorYlow(binNo-1))
				pullmerged.SetBinContent(binNo,(hDatamerged.GetBinContent(binNo)-bkgHTmerged.GetBinContent(binNo))/math.sqrt(MCerror**2+hDatamerged.GetBinError(binNo)**2))
			else: pullmerged.SetBinContent(binNo,0.)
		pullmerged.SetMaximum(3)
		pullmerged.SetMinimum(-3)
		if '53' in sigs[-1]:
			pullmerged.SetFillColor(2)
			pullmerged.SetLineColor(2)
		else:
			pullmerged.SetFillColor(kGray+2)
			pullmerged.SetLineColor(kGray+2)
		formatLowerHist(pullmerged,iPlot)
		pullmerged.GetYaxis().SetTitle('#frac{(obs-bkg)}{uncertainty}')
		pullmerged.Draw("HIST")

		lPad.Update()
		lPad.RedrawAxis()
		frame = lPad.GetFrame()
		lPad.Draw()

	#c1merged.Write()
	savePrefixmerged = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plots/'
	if not os.path.exists(savePrefixmerged): os.system('mkdir '+savePrefixmerged)
	savePrefixmerged+=histPrefixE.replace('_is'+isEMlist[0],'')+isRebinned.replace('_rebinned_stat1p1','')+saveKey
	if '000p0fbinv' in savePrefixmerged: savePrefixmerged=savePrefixmerged.replace('000p0fbinv','abinv')
	if nttaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nT0p_','')
	if nWtaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nW0p_','')
	if nbtaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nB0p_','')
	if njetslist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nJ0p_','')
	if doNormByBinWidth: savePrefixmerged+='_NBBW'
	if yLog: savePrefixmerged+='_logy'
# 	if blind: savePrefixmerged+='_blind'
# 	else:
# 		if doRealPull: savePrefixmerged+='_pull'
# 		if doOneBand: savePrefixmerged+='_totBand'
	if compareShapes: savePrefixmerged+='_shp'

	c1merged.SaveAs(savePrefixmerged+".pdf")
	c1merged.SaveAs(savePrefixmerged+".png")
	c1merged.SaveAs(savePrefixmerged+".eps")
	#c1merged.SaveAs(savePrefixmerged+".root")
	#c1merged.SaveAs(savePrefixmerged+".C")
	for proc in bkgProcList:
		try: del bkghistsmerged[proc+'isL'+tagStr]
		except: pass

if not doNormByBinWidth: 
	out=open(templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plots/'+tempsig.replace('templates','GOFtests').replace('.root','').replace(sigs[-1]+'_','')+saveKey+'.txt','w')
	printTable(table,out)

for sig in sigs: RFiles[sig].Close()

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))


