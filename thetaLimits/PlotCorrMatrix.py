#!/usr/bin/python

import ROOT as rt
import os,sys,math,pickle
from array import array
from pal import *
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
import CMS_lumi, tdrstyle

rt.gROOT.SetBatch(1)

saveKey=''
signal = 'Zp'
lumiStrs = {'36p0':'36','300p0':'300','1000p0':'1000','3000p0':'3000'}
mass_str = ['2000','3000','4000','5000','6000']

nuisNamPlot = {
'lumi':'lumi',
'eff_el':'Efficiency (e)',
'eff_mu':'Efficiency (#mu)',
'pileup':'Pileup',
'jer':'JER',
'jec':'JEC',
'pdf':'PDF',
'muRF':'muRF',
'btag':'b tagging',
'ttag':'t tagging',
'toppt':'top p_{T}',
'xsec_ttbar':'xsec_ttbar',
'xsec_sitop':'xsec_sitop',
'xsec_wjets':'xsec_wjets',
'xsec_zjets':'xsec_zjets',
'xsec_dibos':'xsec_dibos',
'xsec_qcd':'xsec_qcd',
'beta_signal':'beta_signal',
'closure':'closure',
'modmass':'modmass',
}

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.lumi_13TeV= "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation"

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 600; 
W_ref = 800; 
W = W_ref
H = H_ref

iPeriod = 0 #see CMS_lumi.py module for usage!

# references for T, B, L, R
T = 0.08*H_ref
B = 0.14*H_ref 
L = 0.14*W_ref
R = 0.04*W_ref

iPlotList=['zpMass']
tempKeys = ['postfit']
cutString=''
dirs = {
		'Zp20180812_17017fullsel':'templates_17017fullsel_zpMass_2018_8_12',
		'Zp20180812_17017fullselDRgt1':'templates_17017fullselDRgt1_zpMass_2018_8_12_lim',
		'Zp20180814':'templates_zpMass_2018_8_14_lim',
		'Zp20180817':'templates_zpMass_2018_8_17_lim',
		'Zp20180823':'templates_zpMass_2018_8_23_lim',
		'Zp20180824alljets':'templates_alljets_2018_8_24_lim',
		'Zp20180829':'templates_zpMass_2018_8_29_lim',
		'Zp20180829statOnly':'templates_zpMass_2018_8_29_statOnly_lim',
		}
dirKeyList = ['Zp20180829']
binnings = ['1p1']
theMass = mass_str[2]

expLims = {}
obsLims = {}
for lumiStr in lumiStrs.keys():
	for discriminant in iPlotList:
		for dirKey in dirKeyList:
			dir = dirs[dirKey]
			expLims[dirKey+discriminant+lumiStr] = {}
			obsLims[dirKey+discriminant+lumiStr] = {}
			for binning_ in binnings:
				binning='_rebinned_stat'+binning_
				if len(binning_)==0: binning=''
				expLims[dirKey+discriminant+lumiStr][binning_] = []
				obsLims[dirKey+discriminant+lumiStr][binning_] = []
				for tempKey in tempKeys:
					limitDir='/user_data/ssagir/Zprime_limits_2018/'+dir+'/'+tempKey+'/'
					postfitFile='mle_covcorr_templates_'+discriminant+'_'+signal+'M2000'+'_'+lumiStr+'fbinv'+binning+'.root'.replace(signal+'M2000',signal+'M'+theMass)
					print limitDir+cutString+postfitFile
					RFile = rt.TFile(limitDir+cutString+postfitFile)
					hist = RFile.Get('correlation_matrix').Clone()
					for ibin in range(1,hist.GetXaxis().GetNbins()+1): 
						label = hist.GetXaxis().GetBinLabel(ibin)
						hist.GetXaxis().SetBinLabel(ibin,nuisNamPlot[label])
						hist.GetYaxis().SetBinLabel(ibin,nuisNamPlot[label])

					rt.gStyle.SetOptStat(0)
					rt.gStyle.SetPaintTextFormat("1.2f");
					canvas = rt.TCanvas("canvas","canv",1200,800)
					#canvas.SetLogy()
					#canvas.SetTopMargin(0.10)
					canvas.SetBottomMargin(0.12)
					canvas.SetRightMargin(0.12)
					canvas.SetLeftMargin(.16)

					#gStyle.SetPalette(57)
					set_palette(name="kBird")
					hist.Draw("COLZ TEXT")

					histPrefix=discriminant+theMass+'_'+lumiStr+'fbinv'
					folder = '.'
					outDir=folder+'/'+limitDir.split('/')[-3]+'plots'
					if not os.path.exists(outDir): os.system('mkdir '+outDir)
					plotName = 'correlation_matrix_'+histPrefix+''+binning+saveKey+'_'+tempKey
					canvas.SaveAs(outDir+'/'+plotName+'.eps')
					canvas.SaveAs(outDir+'/'+plotName+'.pdf')
					canvas.SaveAs(outDir+'/'+plotName+'.png')
					RFile.Close()
