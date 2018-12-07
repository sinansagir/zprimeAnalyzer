#!/usr/bin/python

from ROOT import TH1D,TH2D,TTree,TFile
from array import array
from weights import *

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb

def analyze(tTree,process,cutList,doAllSys,iPlot,plotDetails,category):
	
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
	isEM  = category['isEM']
	nttag = category['nttag']
	nWtag = category['nWtag']
	nbtag = category['nbtag']
	njets = category['njets']
	catStr = 'is'+isEM+'_nT'+nttag+'_nW'+nWtag+'_nB'+nbtag+'_nJ'+njets
	catStr = catStr.replace('_nT0p','').replace('_nW0p','').replace('_nB0p','').replace('_nJ0p','')

	# Define general cuts
	cut  = '((isSingEl && lepPt>80) || (isSingMu && lepPt>55))'
	cut += ' && ((isSingEl && metPt>120) || (isSingMu && metPt>50))'
# 	cut += ' && (isSingEl || (metPt+lepPt)>150)'
# 	cut += ' && ((isSingEl && leadJetPt>185) || (isSingMu && leadJetPt>150))'
# 	cut += ' && ((isSingEl && subLeadJetPt>50) || (isSingMu && subLeadJetPt>50))'
	cut += ' && (isSingEl || (metPt+lepPt)>200)'
	cut += ' && (leadJetPt>250) && (subLeadJetPt>100)'
	cut += ' && (minDR_lepJet>0.4 || ptRel_lepJet>25)'
	if 'Chi2' not in iPlot: cut += ' && ((thadChi2+tlepChi2)<30)'
	if iPlot!='zpDeltaR': cut += ' && (zpDeltaR > 1)'
	if 'topAK8' in iPlot: cut += ' && (Ntoptagged == 1)'

	weightStr = '1'
	if 'Data' not in process: weightStr += ' * '+str(weight[process])

	# Design the tagging cuts for categories
	isEMCut=''
	if isEM=='E': isEMCut+=' && (isSingEl==1 && isSingMu==0) '
	elif isEM=='M': isEMCut+=' && (isSingMu==1 && isSingEl==0) '

	CSVM = '0.8'
	nttagString = 'Ntoptagged'
	nWtagString = 'NJetsWtagged_0p6_notTtagged'
	nbtagString = ''
	if nttag=='0': nbtagString = 'tlepLeadAK4BTag'
	elif nttag=='1': nbtagString = 'topAK8BTag'
	elif nttag=='0p': nbtagString = '((Ntoptagged==0 && tlepLeadAK4BTag) || (Ntoptagged==1 && topAK8BTag))'
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

	fullcut = cut+isEMCut+nttagCut+nWtagCut+nbtagCut+njetsCut

	print 'plotTreeName: '+plotTreeName
	print 'isEM: '+isEM+' #ttags: '+nttag+' #Wtags: '+nWtag+' #btags: '+nbtag+' #jets: '+njets
	print "Weights:",weightStr
	print 'Cuts: '+fullcut

	# Declare histograms
	hists = {}
	if isPlot2D: hists[iPlot+'_'+lumiStr+'fbinv_'+catStr+'_'+process]  = TH2D(iPlot+'_'+lumiStr+'fbinv_'+catStr+'_'+process,yAxisLabel+xAxisLabel,len(ybins)-1,ybins,len(xbins)-1,xbins)
	else: hists[iPlot+'_'+lumiStr+'fbinv_'+catStr+'_'+process]  = TH1D(iPlot+'_'+lumiStr+'fbinv_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	if doAllSys:
		systList = ['jec']#,'jer']
		for syst in systList:
			for ud in ['Up','Down']:
				if isPlot2D: hists[iPlot+syst+ud+'_'+lumiStr+'fbinv_'+catStr+'_'+process] = TH2D(iPlot+syst+ud+'_'+lumiStr+'fbinv_'+catStr+'_'+process,yAxisLabel+xAxisLabel,len(ybins)-1,ybins,len(xbins)-1,xbins)
				else: hists[iPlot+syst+ud+'_'+lumiStr+'fbinv_'+catStr+'_'+process] = TH1D(iPlot+syst+ud+'_'+lumiStr+'fbinv_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	for key in hists.keys(): hists[key].Sumw2()

	# DRAW histograms
	tTree[process].Draw(plotTreeName+' >> '+iPlot+'_'+lumiStr+'fbinv_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
	if doAllSys:
		if tTree[process+'jecUp']:
			tTree[process+'jecUp'].Draw(plotTreeName   +' >> '+iPlot+'jecUp_'  +lumiStr+'fbinv_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
			tTree[process+'jecDown'].Draw(plotTreeName +' >> '+iPlot+'jecDown_'+lumiStr+'fbinv_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
# 		if tTree[process+'jerUp']:
# 			tTree[process+'jerUp'].Draw(plotTreeName   +' >> '+iPlot+'jerUp_'  +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
# 			tTree[process+'jerDown'].Draw(plotTreeName +' >> '+iPlot+'jerDown_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
	
	for key in hists.keys(): hists[key].SetDirectory(0)	
	return hists
