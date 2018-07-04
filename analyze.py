#!/usr/bin/python

from ROOT import TH1D,TH2D,TTree,TFile
from array import array
from weights import *

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb

def analyze(tTree,process,cutList,doAllSys,iPlot,plotDetails,category):
	print "*****"*20
	print "*****"*20
	print "DISTRIBUTION:", iPlot
	print "            -name in input trees:", plotDetails[0]
	print "            -x-axis label is set to:", plotDetails[2]
	print "            -using the binning as:", plotDetails[1]
	plotTreeName=plotDetails[0]
	xbins=array('d', plotDetails[1])
	xAxisLabel=plotDetails[2]
	isPlot2D = False
	if len(plotDetails)>3: 
		isPlot2D = True
		ybins=array('d', plotDetails[3])
		yAxisLabel=plotDetails[4]
	
	print "/////"*5
	print "PROCESSING: ", process
	print "/////"*5

	# Define categories
	delY  = category['isEM']
	nttag = category['nttag']
	nWtag = category['nWtag']
	nbtag = category['nbtag']
	njets = category['njets']
	catStr = 'is'+delY+'_nT'+nttag+'_nW'+nWtag+'_nB'+nbtag+'_nJ'+njets
	catStr = catStr.replace('_nT0p','').replace('_nW0p','').replace('_nB0p','').replace('_nJ0p','')

	# Define general cuts
	cut  = '(1)'
	cut += ' && (NumAK8Jets >= 2)'
	cut += ' && (Jet0Pt > '+str(cutList['jet1PtCut'])+')'
	cut += ' && (Jet1Pt > '+str(cutList['jet2PtCut'])+')'
	cut += ' && (fabs(Jet0Eta) < 2.4) && (fabs(Jet1Eta) < 2.4)'
	if 'SDM' not in iPlot: 
		cut += ' && (Jet0SDmass > 105) && (Jet0SDmass < 210)'
		cut += ' && (Jet1SDmass > 105) && (Jet1SDmass < 210)'
	if 'Tau32' not in iPlot: cut += ' && (Jet0Tau3/Jet0Tau2 < 0.65) && (Jet1Tau3/Jet1Tau2 < 0.65)'

	weightStr = '1'
	if 'Data' not in process: weightStr += ' * '+str(weight[process])

	# Design the tagging cuts for categories
	delYCut=''
	if delY=='LT': delYCut+=' && deltaY <= '+str(cutList['delYCut'])
	elif delY=='GT': delYCut+=' && deltaY > '+str(cutList['delYCut'])

	CSVM = '0.8'
	nttagString = 'NJetsTtagged_0p81'
	nWtagString = 'NJetsWtagged_0p6_notTtagged'
	nbtagString = '((Jet0SDsubjet0bdisc>'+CSVM+' || Jet0SDsubjet1bdisc>'+CSVM+') + (Jet1SDsubjet0bdisc>'+CSVM+' || Jet1SDsubjet1bdisc>'+CSVM+'))'
	njetsString = 'NJets_JetSubCalc'
	nttagCut = ''
	if 'p' in nttag: nttagCut+=' && '+nttagString+'>='+nttag[:-1]
	else: nttagCut+=' && '+nttagString+'=='+nttag
	if nttag=='0p': nttagCut=''

	nWtagCut = ''
	if 'p' in nWtag: nWtagCut+=' && '+nWtagString+'>='+nWtag[:-1]
	else: nWtagCut+=' && '+nWtagString+'=='+nWtag
	if nWtag=='0p': nWtagCut=''
			
	nbtagCut = ''
	if 'p' in nbtag: nbtagCut+=' && '+nbtagString+'>='+nbtag[:-1]
	else: nbtagCut+=' && '+nbtagString+'=='+nbtag
	if nbtag=='0p': nbtagCut=''

	njetsCut = ''
	if 'p' in njets: njetsCut+=' && '+njetsString+'>='+njets[:-1]
	else: njetsCut+=' && '+njetsString+'=='+njets
	if njets=='0p': njetsCut=''

	fullcut = cut+delYCut+nttagCut+nWtagCut+nbtagCut+njetsCut

	print 'plotTreeName: '+plotTreeName
	print 'deltaY: '+delY+' #ttags: '+nttag+' #Wtags: '+nWtag+' #btags: '+nbtag+' #jets: '+njets
	print "Weights:",weightStr
	print 'Cuts: '+fullcut

	# Declare histograms
	hists = {}
	if isPlot2D: hists[iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process]  = TH2D(iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process,yAxisLabel+xAxisLabel,len(ybins)-1,ybins,len(xbins)-1,xbins)
	else: hists[iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	for key in hists.keys(): hists[key].Sumw2()

	# DRAW histograms
	tTree[process].Draw(plotTreeName+' >> '+iPlot+'_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
	
	for key in hists.keys(): hists[key].SetDirectory(0)	
	return hists
