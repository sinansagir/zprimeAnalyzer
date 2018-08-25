#!/usr/bin/python

import ROOT as rt
from array import array
import os,sys,math
from math import *
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
import CMS_lumi, tdrstyle

rt.gROOT.SetBatch(1)

blind=True
saveKey=''
signal = 'Zp'
lumiStrs = {'36p0':'36','300p0':'300','1000p0':'1000','3000p0':'3000'}
lumiStr = '36p0'
lumiPlot = lumiStrs[lumiStr]
binning = '_rebinned_stat1p1'
discriminant = 'zpMass'

mass_str = ['2000','3000','4000','5000','6000']
theory_xsec = [1.3*1.153,1.3*1.556*0.1,1.3*3.585*0.01,1.3*1.174*0.01,1.3*4.939*0.001]
theory_xsec_13tev = [1.3*0.9528,1.3*0.1289,1.3*0.02807,1.3*0.009095]

limFiles   = [ #compare different optimized selections and discriminants
              '/user_data/ssagir/Zprime_limits_2018/templates_zpMass_2018_8_23_lim/btagcats/limits_templates_'+discriminant+'_'+signal+'M2000'+'_3000p0fbinv'+binning+'_expected.txt',
              '/user_data/ssagir/Zprime_limits_2018/templates_zpMass_2018_8_23_lim/btagcats/limits_templates_'+discriminant+'_'+signal+'M2000'+'_1000p0fbinv'+binning+'_expected.txt',
              '/user_data/ssagir/Zprime_limits_2018/templates_zpMass_2018_8_23_lim/btagcats/limits_templates_'+discriminant+'_'+signal+'M2000'+'_300p0fbinv'+binning+'_expected.txt',
              '/user_data/ssagir/Zprime_limits_2018/templates_zpMass_2018_8_23_lim/btagcats/limits_templates_'+discriminant+'_'+signal+'M2000'+'_36p0fbinv'+binning+'_expected.txt',
              '/user_data/ssagir/Zprime_limits_2018/templates_zpMass_2018_8_23_2xSyst_lim/btagcats/limits_templates_'+discriminant+'_'+signal+'M2000'+'_36p0fbinv'+binning+'_expected.txt',
              '/user_data/ssagir/Zprime_limits_2018/templates_zpMass_2018_8_23_statOnly_lim/btagcats/limits_templates_'+discriminant+'_'+signal+'M2000'+'_36p0fbinv'+binning+'_expected.txt',
              '/user_data/ssagir/Zprime_limits_2018/templates_zpMass_B2G17017ljets_lim/limits_templates_'+discriminant+'_'+signal+'M2000'+'_36p0fbinv'+binning+'_expected.txt',
              '/user_data/ssagir/Zprime_limits_2018/templates_zpMass_B2G17017all_lim/limits_templates_'+discriminant+'_'+signal+'M2000'+'_36p0fbinv'+binning+'_expected.txt',
			  ]

limLegs    = [
              '3000 fb^{-1} (14 TeV)',
              '1000 fb^{-1} (14 TeV)',
              '300 fb^{-1} (14 TeV)',
              '36 fb^{-1} (14 TeV)',
              '36 fb^{-1} (14 TeV) -- #times2 systematics',
              '36 fb^{-1} (14 TeV) -- stat. only',
              '36 fb^{-1} (13 TeV) -- B2G-17-17 l+jets',
              '36 fb^{-1} (13 TeV) -- B2G-17-17 0l+1l+2l',
#               '2#times systematics',
#               'statistical uncertainty only',
#               'B2G-17-17 l+jets',
			  ]

scale_up = [0,0,0,0,0][:len(mass_str)]#%
scale_dn = [0,0,0,0,0][:len(mass_str)]#%
pdf_up   = [0,0,0,0,0][:len(mass_str)]#%
pdf_dn   = [0,0,0,0,0][:len(mass_str)]#%

mass   =array('d', [float(item)/1e3 for item in mass_str])
masserr=array('d',[0 for i in range(len(mass))])
exp   =array('d',[0 for i in range(len(mass))])
experr=array('d',[0 for i in range(len(mass))])
obs   =array('d',[0 for i in range(len(mass))])
obserr=array('d',[0 for i in range(len(mass))]) 
exp68H=array('d',[0 for i in range(len(mass))])
exp68L=array('d',[0 for i in range(len(mass))])
exp95H=array('d',[0 for i in range(len(mass))])
exp95L=array('d',[0 for i in range(len(mass))])

theory_xsec_up = [math.sqrt(scale**2+pdf**2)*xsec/100 for xsec,scale,pdf in zip(theory_xsec,scale_up,pdf_up)]
theory_xsec_dn = [math.sqrt(scale**2+pdf**2)*xsec/100 for xsec,scale,pdf in zip(theory_xsec,scale_dn,pdf_dn)]

theory_xsec_v    = rt.TVectorD(len(mass),array('d',theory_xsec))
theory_xsec_up_v = rt.TVectorD(len(mass),array('d',theory_xsec_up))
theory_xsec_dn_v = rt.TVectorD(len(mass),array('d',theory_xsec_dn))      

theory_xsec_gr = rt.TGraphAsymmErrors(rt.TVectorD(len(mass),mass),theory_xsec_v,rt.TVectorD(len(mass),masserr),rt.TVectorD(len(mass),masserr),theory_xsec_dn_v,theory_xsec_up_v)
theory_xsec_gr.SetFillStyle(3001)
theory_xsec_gr.SetFillColor(rt.kRed)
			   
theory = rt.TGraph(len(mass))
for i in range(len(mass)):
	theory.SetPoint(i, mass[i], theory_xsec[i])
theory13tev = rt.TGraph(len(theory_xsec_13tev))
for i in range(len(theory_xsec_13tev)):
	theory13tev.SetPoint(i, mass[i], theory_xsec_13tev[i])

def getSensitivity(index, exp):
	a1=mass[index]-mass[index-1]
	b1=mass[index]-mass[index-1]
	c1=0
	a2=exp[index]-exp[index-1]
	b2=theory_xsec[index]-theory_xsec[index-1]
	c2=theory_xsec[index-1]-exp[index-1]
	s = (c1*b2-c2*b1)/(a1*b2-a2*b1)
	t = (a1*c2-a2*c1)/(a1*b2-a2*b1)
	return mass[index-1]+s*(mass[index]-mass[index-1]), exp[index-1]+s*(exp[index]-exp[index-1])

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
H  = H_ref

iPeriod = 0 #see CMS_lumi.py module for usage!

# references for T, B, L, R
T = 0.08*H_ref
B = 0.14*H_ref 
L = 0.14*W_ref
R = 0.04*W_ref

xrange_min=mass[0]
xrange_max=mass[-1]
yrange_min=.001+.00001
yrange_max=10.45

observed = {}
expected = {}
crossingList = {}
ind=0
skipped=[]
for limFile in limFiles:
	exp=array('d',[0 for i in range(len(mass))])
	obs=array('d',[0 for i in range(len(mass))])

	expecteds_ = []
	observeds_ = []
	for i in range(len(mass)):
		try:
			fexp = open(limFile.replace(signal+'M2000',signal+'M'+mass_str[i]), 'rU')
			linesExp = fexp.readlines()
			fexp.close()
		except: continue

		if not blind: fobs = open(limFile.replace(signal+'M2000',signal+'M'+mass_str[i]).replace('_expected.txt','_observed.txt'), 'rU')
		else: fobs = open(limFile.replace(signal+'M2000',signal+'M'+mass_str[i]), 'rU')
		linesObs = fobs.readlines()
		fobs.close()

		obs[i] = float(linesObs[1].strip().split()[1])
		exp[i] = float(linesExp[1].strip().split()[1])
		
		expecteds_.append([mass[i],exp[i]])
		observeds_.append([mass[i],obs[i]])

	observed[limFile] = rt.TGraph(len(observeds_))
	expected[limFile] = rt.TGraph(len(expecteds_))
	for i in range(len(expecteds_)):
		observed[limFile].SetPoint(i,observeds_[i][0],observeds_[i][1])
		expected[limFile].SetPoint(i,expecteds_[i][0],expecteds_[i][1])

	ind+=1
	observed[limFile].SetLineColor(rt.kBlack)
	observed[limFile].SetLineWidth(2)
	observed[limFile].SetMarkerStyle(20)							
	expected[limFile].SetLineColor(ind)
	expected[limFile].SetLineWidth(2)
	expected[limFile].SetLineStyle(1)
                                               
canvas = rt.TCanvas("canvas","Limits", 1000, 800)
canvas.SetBottomMargin(0.15)
canvas.SetRightMargin(0.06)
canvas.SetLogy()
	
XaxisTitle = "g^{RS}_{KK} mass [TeV]"
YaxisTitle = "#sigma(g^{RS}_{KK}) [pb]"
expected[limFiles[0]].Draw('AL')
expected[limFiles[0]].GetYaxis().SetRangeUser(yrange_min,yrange_max)
expected[limFiles[0]].GetXaxis().SetRangeUser(xrange_min,xrange_max)
expected[limFiles[0]].GetXaxis().SetTitle(XaxisTitle)
expected[limFiles[0]].GetYaxis().SetTitle(YaxisTitle)

for limFile in limFiles:
	if limFile == limFiles[0]: continue
	expected[limFile].Draw("same")
expected[limFiles[3]].Draw("same")

theory.SetLineColor(2)
theory.SetLineStyle(2)
theory.SetLineWidth(2)
theory.Draw("same")

theory13tev.SetLineColor(1)
theory13tev.SetLineStyle(2)
theory13tev.SetLineWidth(2)
theory13tev.Draw("same")

leg = rt.TLegend(.5,.55,.93,.94)
leg.AddEntry(theory13tev, "Signal cross section (13 TeV)", "l")
leg.AddEntry(theory, "Signal cross section (14 TeV)", "l")
i=-1
for limFile in limFiles:
	i+=1
	leg.AddEntry(expected[limFile], limLegs[i], "l")

#draw the lumi text on the canvas
# CMS_lumi.lumi_sqrtS = lumiPlot+" fb^{-1} (14 TeV)" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
# CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)

leg.SetShadowColor(0)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetLineColor(0)
leg.Draw() 

folder='templates_zpMass_2018_8_23_limplots'
canvas.SaveAs(folder+'/comparisonljets'+'.pdf')
canvas.SaveAs(folder+'/comparisonljets'+'.png')
canvas.SaveAs(folder+'/comparisonljets'+'.eps')

