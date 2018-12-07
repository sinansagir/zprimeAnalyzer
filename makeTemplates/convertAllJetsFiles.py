#!/usr/bin/python

from ROOT import TFile
import math

theDir = 'templates_alljets_2018_10_31'
lumiList = ['36','300','1000','3000']
sigList = ['rsg2','rsg3','rsg4','rsg5','rsg6','rsg8','rsg10','rsg12']
bkgList = ['TTinc','QCD']
catList = ['l0','l1','l2','h0','h1','h2']
scaleStatUnc = False #scales the statistical uncertainties by 1/sqrt(newTargetlumi/36000)
if scaleStatUnc: theDir=theDir.replace('alljets','alljets_halveStatUnc')

inFiles = {}
outFiles = {}
for lumi in lumiList: 
	inFiles[lumi] = TFile(theDir+'/thetarsg_'+lumi+'000.root')
	for sig in sigList:
		outFiles[sig+lumi] = TFile(theDir+'/templates_zpMass_ZpM'+sig.replace('rsg','')+'000_'+lumi+'p0fbinv.root','RECREATE')
		for cat in catList:
			newCatName = cat.replace('l','_isE_nB').replace('h','_isM_nB')
			histName = 'zpMass_'+lumi+'p0fbinv'+newCatName
			hSig = inFiles[lumi].Get('had'+cat+'__'+sig).Clone(histName+'__sig')
			hSigUp = inFiles[lumi].Get('had'+cat+'__'+sig+'__jec__up').Clone(histName+'__sig__jec__plus')
			hSigDn = inFiles[lumi].Get('had'+cat+'__'+sig+'__jec__down').Clone(histName+'__sig__jec__minus')
			if scaleStatUnc:
				for ibin in range(1,hSig.GetNbinsX()+1):
					hSig.SetBinError(ibin,hSig.GetBinError(ibin)/math.sqrt(float(lumi)/36.))
					hSigUp.SetBinError(ibin,hSigUp.GetBinError(ibin)/math.sqrt(float(lumi)/36.))
					hSigDn.SetBinError(ibin,hSigDn.GetBinError(ibin)/math.sqrt(float(lumi)/36.))
			hSig.Write()
			hSigUp.Write()
			hSigDn.Write()
			for bkg in bkgList:
				hBKG = inFiles[lumi].Get('had'+cat+'__'+bkg).Clone(histName+'__'+bkg.replace('TTinc','ttbar').replace('QCD','qcd'))
				hBKGup = inFiles[lumi].Get('had'+cat+'__'+bkg+'__jec__up').Clone(histName+'__'+bkg.replace('TTinc','ttbar').replace('QCD','qcd')+'__jec__plus')
				hBKGdn = inFiles[lumi].Get('had'+cat+'__'+bkg+'__jec__down').Clone(histName+'__'+bkg.replace('TTinc','ttbar').replace('QCD','qcd')+'__jec__minus')
				if scaleStatUnc:
					for ibin in range(1,hBKG.GetNbinsX()+1):
						hBKG.SetBinError(ibin,hBKG.GetBinError(ibin)/math.sqrt(float(lumi)/36.))
						hBKGup.SetBinError(ibin,hBKGup.GetBinError(ibin)/math.sqrt(float(lumi)/36.))
						hBKGdn.SetBinError(ibin,hBKGdn.GetBinError(ibin)/math.sqrt(float(lumi)/36.))
				#if bkg=='QCD': hBKG.Scale(0.5)
				hBKG.Write()
				hBKGup.Write()
				hBKGdn.Write()
			hData = inFiles[lumi].Get('had'+cat+'__'+bkgList[0]).Clone(histName+'__DATA')
			if scaleStatUnc:
				for ibin in range(1,hData.GetNbinsX()+1):
					hData.SetBinError(ibin,hData.GetBinError(ibin)/math.sqrt(float(lumi)/36.))
			hData.Write()
		outFiles[sig+lumi].Close()
	inFiles[lumi].Close()

sigList = ['ZPrime_M2000_W600','ZPrime_M3000_W900','ZPrime_M4000_W1200','ZPrime_M5000_W1500','ZPrime_M6000_W1800','ZPrime_M8000_W2400','ZPrime_M10000_W3000','ZPrime_M12000_W3600']
inFiles = {}
outFiles = {}
for lumi in lumiList: 
	inFiles[lumi] = TFile(theDir+'/thetazp_'+lumi+'000.root')
	for sig in sigList:
		outFiles[sig+lumi] = TFile(theDir+'/templates_zpMass_ZpW30'+sig.split('_')[1]+'_'+lumi+'p0fbinv.root','RECREATE')
		for cat in catList:
			newCatName = cat.replace('l','_isE_nB').replace('h','_isM_nB')
			histName = 'zpMass_'+lumi+'p0fbinv'+newCatName
			hSig = inFiles[lumi].Get('had'+cat+'__'+sig).Clone(histName+'__sig')
			hSigUp = inFiles[lumi].Get('had'+cat+'__'+sig+'__jec__up').Clone(histName+'__sig__jec__plus')
			hSigDn = inFiles[lumi].Get('had'+cat+'__'+sig+'__jec__down').Clone(histName+'__sig__jec__minus')
			if scaleStatUnc:
				for ibin in range(1,hSig.GetNbinsX()+1):
					hSig.SetBinError(ibin,hSig.GetBinError(ibin)/math.sqrt(float(lumi)/36.))
					hSigUp.SetBinError(ibin,hSigUp.GetBinError(ibin)/math.sqrt(float(lumi)/36.))
					hSigDn.SetBinError(ibin,hSigDn.GetBinError(ibin)/math.sqrt(float(lumi)/36.))
			hSig.Write()
			hSigUp.Write()
			hSigDn.Write()
			for bkg in bkgList:
				hBKG = inFiles[lumi].Get('had'+cat+'__'+bkg).Clone(histName+'__'+bkg.replace('TTinc','ttbar').replace('QCD','qcd'))
				hBKGup = inFiles[lumi].Get('had'+cat+'__'+bkg+'__jec__up').Clone(histName+'__'+bkg.replace('TTinc','ttbar').replace('QCD','qcd')+'__jec__plus')
				hBKGdn = inFiles[lumi].Get('had'+cat+'__'+bkg+'__jec__down').Clone(histName+'__'+bkg.replace('TTinc','ttbar').replace('QCD','qcd')+'__jec__minus')
				if scaleStatUnc:
					for ibin in range(1,hBKG.GetNbinsX()+1):
						hBKG.SetBinError(ibin,hBKG.GetBinError(ibin)/math.sqrt(float(lumi)/36.))
						hBKGup.SetBinError(ibin,hBKGup.GetBinError(ibin)/math.sqrt(float(lumi)/36.))
						hBKGdn.SetBinError(ibin,hBKGdn.GetBinError(ibin)/math.sqrt(float(lumi)/36.))
				#if bkg=='QCD': hBKG.Scale(0.5)
				hBKG.Write()
				hBKGup.Write()
				hBKGdn.Write()
			hData = inFiles[lumi].Get('had'+cat+'__'+bkgList[0]).Clone(histName+'__DATA')
			if scaleStatUnc:
				for ibin in range(1,hData.GetNbinsX()+1):
					hData.SetBinError(ibin,hData.GetBinError(ibin)/math.sqrt(float(lumi)/36.))
			hData.Write()
		outFiles[sig+lumi].Close()
	inFiles[lumi].Close()
