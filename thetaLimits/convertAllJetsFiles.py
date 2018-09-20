#!/usr/bin/python

from ROOT import TFile

theDir = 'templates_alljets_2018_9_20'
lumiList = ['36','300','1000','3000']
sigList = ['rsg2','rsg3','rsg4','rsg5','rsg6']
bkgList = ['TTinc','QCD']
catList = ['l0','l1','l2','h0','h1','h2']

inFiles = {}
outFiles = {}
for lumi in lumiList: 
	inFiles[lumi] = TFile(theDir+'/theta_'+lumi+'.root')
	for sig in sigList:
		outFiles[sig+lumi] = TFile(theDir+'/templates_zpMass_ZpM'+sig.replace('rsg','')+'000_'+lumi+'p0fbinv.root','RECREATE')
		for cat in catList:
			hSig = inFiles[lumi].Get('had'+cat+'__'+sig).Clone('had'+cat+'__sig')
			hSig.Write()
			for bkg in bkgList:
				hBKG = inFiles[lumi].Get('had'+cat+'__'+bkg).Clone('had'+cat+'__'+bkg.replace('TTinc','ttbar').replace('QCD','qcd'))
				hBKG.Write()
		outFiles[sig+lumi].Close()
	inFiles[lumi].Close()
