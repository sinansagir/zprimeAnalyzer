#!/usr/bin/python

from ROOT import TFile
import math

theDir = 'templates_alljets_2018_10_31'
lumiList = ['3000','15000']
sigList = ['RSG_4000','RSG_6000','RSG_8000','RSG_10000','RSG_12000']
bkgList = ['ttbar','qcd']
#catList = ['l0','l1','l2','h0','h1','h2']
catList = ['0b','1b','2b']
scaleStatUnc = True #scales the statistical uncertainties by 1/sqrt(newTargetlumi/36000)
if scaleStatUnc: theDir=theDir.replace('alljets','alljets_halveStatUnc')

inFile = TFile(theDir+'/thetarsg_15000_Oct30.root')
outFiles = {}
for lumi in lumiList: 
	for sig in sigList:
		outFiles[sig+lumi] = TFile(theDir+'/templates_zpMass_ZpM'+sig.replace('RSG_','')+'_'+lumi+'p0fbinv.root','RECREATE')
		for cat in catList:
			newCatName = '_isE_nB'+cat.replace('b','')
			histName = 'zpMass_'+lumi+'p0fbinv'+newCatName
			hSig = inFile.Get(cat+'__'+sig).Clone(histName+'__sig')
			hSig.Scale(float(lumi)/15000.)
			if scaleStatUnc:
				for ibin in range(1,hSig.GetNbinsX()+1):
					hSig.SetBinError(ibin,hSig.GetBinError(ibin)/math.sqrt(float(lumi)/36.))
			hSig.Write()
			for bkg in bkgList:
				hBKG = inFile.Get(cat+'__'+bkg).Clone(histName+'__'+bkg.replace('TTinc','ttbar').replace('QCD','qcd'))
				hBKG.Scale(float(lumi)/15000.)
				if scaleStatUnc:
					for ibin in range(1,hBKG.GetNbinsX()+1):
						hBKG.SetBinError(ibin,hBKG.GetBinError(ibin)/math.sqrt(float(lumi)/36.))
				hBKG.Write()
			hData = inFile.Get(cat+'__'+bkgList[0]).Clone(histName+'__DATA')
			hData.Scale(float(lumi)/15000.)
			if scaleStatUnc:
				for ibin in range(1,hData.GetNbinsX()+1):
					hData.SetBinError(ibin,hData.GetBinError(ibin)/math.sqrt(float(lumi)/36.))
			hData.Write()
		outFiles[sig+lumi].Close()
sigList = ['Zprime_M4000_W1200','Zprime_M6000_W1800','Zprime_M8000_W2400','Zprime_M10000_W3000','Zprime_M12000_W3600']
inFile = TFile(theDir+'/thetazp_15000_Oct30.root')
outFiles = {}
for lumi in lumiList: 
	for sig in sigList:
		outFiles[sig+lumi] = TFile(theDir+'/templates_zpMass_ZpW30'+sig.split('_')[1]+'_'+lumi+'p0fbinv.root','RECREATE')
		for cat in catList:
			newCatName = '_isE_nB'+cat.replace('b','')
			histName = 'zpMass_'+lumi+'p0fbinv'+newCatName
			hSig = inFile.Get(cat+'__'+sig).Clone(histName+'__sig')
			hSig.Scale(float(lumi)/15000.)
			if scaleStatUnc:
				for ibin in range(1,hSig.GetNbinsX()+1):
					hSig.SetBinError(ibin,hSig.GetBinError(ibin)/math.sqrt(float(lumi)/36.))
			hSig.Write()
			for bkg in bkgList:
				hBKG = inFile.Get(cat+'__'+bkg).Clone(histName+'__'+bkg.replace('TTinc','ttbar').replace('QCD','qcd'))
				hBKG.Scale(float(lumi)/15000.)
				if scaleStatUnc:
					for ibin in range(1,hBKG.GetNbinsX()+1):
						hBKG.SetBinError(ibin,hBKG.GetBinError(ibin)/math.sqrt(float(lumi)/36.))
				hBKG.Write()
			hData = inFile.Get(cat+'__'+bkgList[0]).Clone(histName+'__DATA')
			hData.Scale(float(lumi)/15000.)
			if scaleStatUnc:
				for ibin in range(1,hData.GetNbinsX()+1):
					hData.SetBinError(ibin,hData.GetBinError(ibin)/math.sqrt(float(lumi)/36.))
			hData.Write()
		outFiles[sig+lumi].Close()

# for lumi in lumiList: 
# 	for sig in sigList:
# 		outFiles[sig+lumi] = TFile(theDir+'/templates_zpMass_ZpM'+sig.replace('zprime','')+'000_'+lumi+'p0fbinv.root','RECREATE')
# 		for cat in catList:
# 			newCatName = cat.replace('l','_isE_nB').replace('h','_isM_nB')
# 			hSig = inFile.Get('had'+cat+'__'+sig).Clone('had'+newCatName+'__sig')
# 			hSig.Scale(float(lumi)/15000.)
# 			hSig.Write()
# 			for bkg in bkgList:
# 				hBKG = inFile.Get('had'+cat+'__'+bkg).Clone('had'+newCatName+'__'+bkg.replace('TTinc','ttbar').replace('QCD','qcd'))
# 				hBKG.Scale(float(lumi)/15000.)
# 				hBKG.Write()
# 			hData = inFile.Get('had'+cat+'__'+bkgList[0]).Clone('had'+newCatName+'__DATA')
# 			hData.Scale(float(lumi)/15000.)
# 			hData.Write()
# 		outFiles[sig+lumi].Close()
inFile.Close()
