#!/usr/bin/python

import ROOT as rt
import os,sys,math,pickle
from array import array
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
					postfitFile='templates_'+discriminant+'_'+signal+'M2000'+'_'+lumiStr+'fbinv'+binning+'.p'.replace(signal+'M2000',signal+'M'+theMass)
					print limitDir+cutString+postfitFile
					parVals=pickle.load(open(limitDir+cutString+postfitFile,'rb'))
					sigproc = 'sig'
					nuisNam = []
					nuisVal = []
					nuisErr = []
					for nuis in sorted(parVals[sigproc].keys()):
						if nuis=='__cov' or nuis=='__nll': continue
						print nuis,"=",parVals[sigproc][nuis][0][0],"+/-",parVals[sigproc][nuis][0][1]
						if nuis=='beta_signal': continue
						nuisNam.append(nuis)
						nuisVal.append(parVals[sigproc][nuis][0][0])
						nuisErr.append(parVals[sigproc][nuis][0][1])

					nuisVal = []
					nuisErr = []
					for i in range(len(nuisNam)):
						nuis = nuisNam[i]
						nuisVal.append(parVals[sigproc][nuis][0][0])
						nuisErr.append(parVals[sigproc][nuis][0][1])
					nNuis = len(nuisNam)

					g   = rt.TGraphAsymmErrors(nNuis)
					g68 = rt.TGraph(2*nNuis+7)
					g95 = rt.TGraph(2*nNuis+7)
					for i in range(nNuis):
						g.SetPoint(i, nuisVal[i], i+1.5)
						g.SetPointEXlow(i, nuisErr[i])
						g.SetPointEXhigh(i, nuisErr[i])
					for a in xrange(0, nNuis+3):
						g68.SetPoint(a, -1, a)
						g95.SetPoint(a, -1.99, a)
						g68.SetPoint(a+1+nNuis+2, 1, nNuis+2-a)
						g95.SetPoint(a+1+nNuis+2, 1.99, nNuis+2-a)

					g.SetLineStyle(1)
					g.SetLineWidth(1)
					g.SetLineColor(1)
					g.SetMarkerStyle(21)
					g.SetMarkerSize(1.25)
					g68.SetFillColor(rt.kGreen)
					g95.SetFillColor(rt.kYellow)

					canvas = rt.TCanvas('PostFit', 'PostFit', 800, 1200)
					canvas.SetTopMargin(0.06)
					canvas.SetRightMargin(0.06)
					canvas.SetBottomMargin(0.12)
					canvas.SetLeftMargin(0.3)
					canvas.SetTickx()
					canvas.SetTicky()
	
					g95.Draw('AF')
					g68.Draw('F')
					g.Draw('P')


					prim_hist = g95.GetHistogram() 
					ax_1 = prim_hist.GetYaxis()
					ax_2 = prim_hist.GetXaxis()

					g95.SetTitle('')
					ax_2.SetTitle('post-fit values')
					#ax_2.SetTitle('deviation in units of #sigma')
					ax_1.SetTitleSize(0.050)
					ax_2.SetTitleSize(0.050)
					ax_1.SetTitleOffset(1.4)
					ax_2.SetTitleOffset(1.0)
					ax_1.SetLabelSize(0.05)
					#ax_2.SetLabelSize(0.05)
					ax_1.SetRangeUser(0, nNuis+2)
					ax_2.SetRangeUser(-2.2, 2.2)

					ax_1.Set(nNuis+2, 0, nNuis+2)
					ax_1.SetNdivisions(-414)
					ax_2.SetNdivisions(5,rt.kTRUE)
					for i in range(nNuis):
						ax_1.SetBinLabel(i+2, nuisNamPlot[nuisNam[i]])

					g95.GetHistogram().Draw('axis,same')
					canvas.Modified()
					canvas.Update()

					histPrefix=discriminant+theMass+'_'+lumiStr+'fbinv'
					folder = '.'
					outDir=folder+'/'+limitDir.split('/')[-3]+'plots'
					if not os.path.exists(outDir): os.system('mkdir '+outDir)
					plotName = 'postFitNuis_'+histPrefix+''+binning+saveKey+'_'+tempKey
					canvas.SaveAs(outDir+'/'+plotName+'.eps')
					canvas.SaveAs(outDir+'/'+plotName+'.pdf')
					canvas.SaveAs(outDir+'/'+plotName+'.png')

