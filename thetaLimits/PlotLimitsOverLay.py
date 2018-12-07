#!/usr/bin/python

import ROOT as rt
import os,sys,math
from array import array
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
import CMS_lumi, tdrstyle

rt.gROOT.SetBatch(1)

blind=True
saveKey='_v2'
signal = 'Zp'
lumiStrs = {'36p0':'36','300p0':'300','1000p0':'1000','3000p0':'3000'}
lumiStr = '36p0'
lumiPlot = lumiStrs[lumiStr]
binning = '_rebinned_stat0p1'
discriminant = 'zpMass'

mass_str = ['2000','3000','4000','5000','6000','8000','10000','12000']
theory_xsec = [1.3*1.153,1.3*1.556*0.1,1.3*3.585*0.01,1.3*1.174*0.01,1.3*4.939*0.001,1.3*1.403*0.001,1.3*5.527*0.0001,1.3*2.622*0.0001]
theory_xsec_13tev = [1.3*0.9528,1.3*0.1289,1.3*0.02807,1.3*0.009095]
ljetLim = 'templates_halveStatUnc_2018_10_31'
ajetLim = 'templates_alljets_halveStatUnc_2018_10_31'
theConf = ''
doCLS='_acls' #leave empty for Bayesian and '_acls' for asymptotic CLs limits

limFiles   = [ #compare different limit configurations
              '/user_data/ssagir/Zprime_limits_2018/'+ljetLim+'_comb'+theConf+'_lim/all/limits_templates_'+discriminant+'_'+signal+'M2000'+'_36p0fbinv'+binning+doCLS+'_expected.txt',
              '/user_data/ssagir/Zprime_limits_2018/'+ajetLim+theConf+'_lim/all/limits_templates_'+discriminant+'_'+signal+'M2000'+'_36p0fbinv'+binning+doCLS+'_expected.txt',
              '/user_data/ssagir/Zprime_limits_2018/'+ljetLim+theConf+'_lim/all/limits_templates_'+discriminant+'_'+signal+'M2000'+'_36p0fbinv'+binning+doCLS+'_expected.txt',
#               '/user_data/ssagir/Zprime_limits_2018/'+ljetLim+'_comb'+theConf+'_2xSyst_lim/all/limits_templates_'+discriminant+'_'+signal+'M2000'+'_36p0fbinv'+binning+doCLS+'_expected.txt',
              '/user_data/ssagir/Zprime_limits_2018/'+ljetLim+'_comb'+theConf+'_statOnly_lim/all/limits_templates_'+discriminant+'_'+signal+'M2000'+'_36p0fbinv'+binning+doCLS+'_expected.txt',
              '/user_data/ssagir/Zprime_limits_2018/templates_zpMass_B2G17017alljets_lim/limits_templates_'+discriminant+'_'+signal+'M2000'+'_36p0fbinv_expected.txt',
              '/user_data/ssagir/Zprime_limits_2018/templates_zpMass_B2G17017ljets_lim/limits_templates_'+discriminant+'_'+signal+'M2000'+'_36p0fbinv_expected.txt',
              '/user_data/ssagir/Zprime_limits_2018/templates_zpMass_B2G17017all_lim/limits_templates_'+discriminant+'_'+signal+'M2000'+'_36p0fbinv_expected.txt',
			  ]

limDets    = [
              ['14 TeV -- 0l+1l',rt.kOrange,1],
              ['14 TeV -- 0l',rt.kOrange,2],
              ['14 TeV -- 1l',rt.kOrange,9],
#               ['14 TeV -- 0l+1l (#times2 systematics)',rt.kBlack,2],
              ['14 TeV -- 0l+1l (only stat. unc.)',rt.kBlue,2],
              ['13 TeV -- B2G-17-17 0l',rt.kGreen+3,2],
              ['13 TeV -- B2G-17-17 1l',rt.kGreen+3,9],
              ['13 TeV -- B2G-17-17 0l+1l+2l',rt.kGreen+3,1],
			  ]

limFiles   = [ #compare different limit configurations
              '/user_data/ssagir/Zprime_limits_2018/'+ljetLim+'_comb'+theConf+'_lim/all/limits_templates_'+discriminant+'_'+signal+'M2000'+'_3000p0fbinv'+binning+doCLS+'_expected.txt',
#               '/user_data/ssagir/Zprime_limits_2018/'+ljetLim+theConf+'_comb'+'_2xSyst_lim/all/limits_templates_'+discriminant+'_'+signal+'M2000'+'_3000p0fbinv'+binning+doCLS+'_expected.txt',
              '/user_data/ssagir/Zprime_limits_2018/'+ljetLim+'_comb'+theConf+'_statOnly_lim/all/limits_templates_'+discriminant+'_'+signal+'M2000'+'_3000p0fbinv'+binning+doCLS+'_expected.txt',
			  ]

limDets    = [
              ['w/ YR18 syst. uncert.',rt.kBlack,1],
#               ['with YR18 syst. uncert. #times2',rt.kOrange,2],
              ['w/ Stat. uncert. only',rt.kBlue,9],
			  ]
 
# limFiles   = [ #compare different optimized selections and discriminants
#               '/user_data/ssagir/Zprime_limits_2018/'+ajetLim+theConf+'_lim/all/limits_templates_'+discriminant+'_'+signal+'M2000'+'_3000p0fbinv'+binning+doCLS+'_expected.txt',
#               '/user_data/ssagir/Zprime_limits_2018/'+ljetLim+theConf+'_lim/all/limits_templates_'+discriminant+'_'+signal+'M2000'+'_3000p0fbinv'+binning+doCLS+'_expected.txt',
#               '/user_data/ssagir/Zprime_limits_2018/'+ljetLim+'_comb'+theConf+'_lim/all/limits_templates_'+discriminant+'_'+signal+'M2000'+'_3000p0fbinv'+binning+doCLS+'_expected.txt',
# 			  ]
# 
# limDets    = [
#               ['Fully hadronic',rt.kOrange,2],
#               ['Single-lepton',rt.kBlue,9],
#               ['Combination',rt.kBlack,1],
# 			  ]

# limFiles   = [ #compare different optimized selections and discriminants
#               '/user_data/ssagir/Zprime_limits_2018/'+ajetLim+theConf+'_lim/all/limits_templates_'+discriminant+'_'+signal+'M2000'+'_3000p0fbinv'+doCLS+'_expected.txt',
#               '/user_data/ssagir/Zprime_limits_2018/'+ljetLim+theConf+'_lim/nobtagcats/limits_templates_'+discriminant+'_'+signal+'M2000'+'_3000p0fbinv'+binning+doCLS+'_expected.txt',
#               '/user_data/ssagir/Zprime_limits_2018/'+ljetLim+'_comb'+theConf+'_lim/nobtagcats/limits_templates_'+discriminant+'_'+signal+'M2000'+'_3000p0fbinv'+binning+doCLS+'_expected.txt',
#               '/user_data/ssagir/Zprime_limits_2018/templates_alljets_halveNTMJ_2018_9_20_preARCwMCstat_lim/all/limits_templates_'+discriminant+'_'+signal+'M2000'+'_3000p0fbinv'+doCLS+'_expected.txt',
#               '/user_data/ssagir/Zprime_limits_2018/templates_zpMass_mergeprocs_halveNTMJ_2018_8_29_preARCwMCstat_lim/nobtagcats/limits_templates_'+discriminant+'_'+signal+'M2000'+'_3000p0fbinv'+doCLS+'_expected.txt',
#               '/user_data/ssagir/Zprime_limits_2018/templates_zpMass_mergeprocs_halveNTMJ_2018_8_29_comb_preARCwMCstat_lim/nobtagcats/limits_templates_'+discriminant+'_'+signal+'M2000'+'_3000p0fbinv'+doCLS+'_expected.txt',
# 			  ]
# 
# limDets    = [
#               ['0l',rt.kOrange,1],
#               ['1l',rt.kBlue,1],
#               ['0l+1l',rt.kBlack,1],
#               ['0l -- NTMJ/2',rt.kOrange,2],
#               ['1l -- NTMJ/2',rt.kBlue,2],
#               ['0l+1l -- NTMJ/2',rt.kBlack,2],
# 			  ]
			  
scale_up = [0,0,0,0,0,0,0,0,0,0,0][:len(mass_str)]#%
scale_dn = [0,0,0,0,0,0,0,0,0,0,0][:len(mass_str)]#%
pdf_up   = [0,0,0,0,0,0,0,0,0,0,0][:len(mass_str)]#%
pdf_dn   = [0,0,0,0,0,0,0,0,0,0,0][:len(mass_str)]#%

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
CMS_lumi.extraText = "Simulation Preliminary"

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 600; 
W_ref = 800; 
W = W_ref
H = H_ref

iPeriod = 0 #see CMS_lumi.py module for usage!

# references for T, B, L, R
T = 0.10*H_ref
B = 0.125*H_ref
L = 0.12*W_ref
R = 0.05*W_ref

xrange_min=mass[0]
xrange_max=mass[-1]
yrange_min=.0008
yrange_max=8.0

observed = {}
expected = {}
ind=0
for limFile in limFiles:
	exp=array('d',[0 for i in range(len(mass))])
	if 'B2G17017' in limFile: exp=array('d',[0 for i in range(len(mass)-1)])
	expecteds_ = []
	for i in range(len(mass)):
		if 'B2G17017' in limFile and mass[i]>5: continue
		try:
			fexp = open(limFile.replace(signal+'M2000',signal+'M'+mass_str[i]), 'rU')
			linesExp = fexp.readlines()
			fexp.close()
			exp[i] = float(linesExp[1].strip().split()[1])
		except: 
			print "Continuing",limFile.replace(signal+'M2000',signal+'M'+mass_str[i])
			pass
		expecteds_.append([mass[i],exp[i]])
	expected[limFile] = rt.TGraph(len(expecteds_))
	for i in range(len(expecteds_)): expected[limFile].SetPoint(i,expecteds_[i][0],expecteds_[i][1])					
	expected[limFile].SetLineColor(limDets[ind][1])
	expected[limFile].SetLineWidth(3)
	expected[limFile].SetLineStyle(limDets[ind][2])
	ind+=1

canvas = rt.TCanvas("c4","c4",50,50,W,H)
canvas.SetFillColor(0)
canvas.SetBorderMode(0)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.SetLeftMargin( L/W )
canvas.SetRightMargin( R/W )
canvas.SetTopMargin( T/H )
canvas.SetBottomMargin( B/H )
#canvas.SetTickx(0)
#canvas.SetTicky(0)
canvas.SetLogy()

XaxisTitle = "RSG mass [TeV]"
YaxisTitle = "#sigma(RSG #rightarrow t#bar{t}) [pb]"
if 'W' in signal: 
	XaxisTitle = "Z' 30% width mass [TeV]"
	YaxisTitle = "#sigma(Z' #rightarrow t#bar{t}) [pb]"

expected[limFiles[0]].Draw('AL')
expected[limFiles[0]].GetYaxis().SetRangeUser(yrange_min,yrange_max)
expected[limFiles[0]].GetXaxis().SetRangeUser(xrange_min,xrange_max)
expected[limFiles[0]].GetXaxis().SetTitle(XaxisTitle)
expected[limFiles[0]].GetYaxis().SetTitle(YaxisTitle)

for limFile in limFiles:
	if limFile == limFiles[0]: continue
	expected[limFile].Draw("same")
#expected[limFiles[3]].Draw("same")

theory.SetLineColor(2)
theory.SetLineStyle(2)
theory.SetLineWidth(3)
if 'W' not in signal: theory.Draw("same")

theory13tev.SetLineColor(1)
theory13tev.SetLineStyle(2)
theory13tev.SetLineWidth(3)
#theory13tev.Draw("same")

#leg = rt.TLegend(.50,.64,.94,.89) # top right
leg = rt.TLegend(.53,.64,.96,.89) # top right
#if len(limFiles)==3: leg = rt.TLegend(.47,.59,.94,.89) # top right
if len(limFiles)==3: leg = rt.TLegend(.53,.59,.96,.89) # top right
#leg.AddEntry(theory13tev, "Signal cross section (13 TeV)", "l")
if 'W' not in signal: leg.AddEntry(theory, "Signal cross section", "l")
i=-1
for limFile in limFiles:
	i+=1
	leg.AddEntry(expected[limFile], limDets[i][0], "l")

#draw the lumi text on the canvas
CMS_lumi.lumi_sqrtS = "3 ab^{-1} (14 TeV)"#lumiPlot+" fb^{-1} (14 TeV)" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)

leg.SetShadowColor(0)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetLineColor(0)
leg.Draw() 

folder=ljetLim+theConf+'_comb'+'plots'
# canvas.SaveAs(folder+'/comparison36fbinv'+saveKey+doCLS+'.pdf')
# canvas.SaveAs(folder+'/comparison36fbinv'+saveKey+doCLS+'.png')
# canvas.SaveAs(folder+'/comparison36fbinv'+saveKey+doCLS+'.eps')
# canvas.SaveAs(folder+'/combosystcomparisonlumiall'+saveKey+doCLS+'.pdf')
# canvas.SaveAs(folder+'/combosystcomparisonlumiall'+saveKey+doCLS+'.png')
# canvas.SaveAs(folder+'/combosystcomparisonlumiall'+saveKey+doCLS+'.eps')
canvas.SaveAs(folder+'/combosystcomparison3abinv'+saveKey+doCLS+'.pdf')
canvas.SaveAs(folder+'/combosystcomparison3abinv'+saveKey+doCLS+'.png')
canvas.SaveAs(folder+'/combosystcomparison3abinv'+saveKey+doCLS+'.eps')
# canvas.SaveAs(folder+'/combochnscomparisonlumiall'+saveKey+doCLS+'.pdf')
# canvas.SaveAs(folder+'/combochnscomparisonlumiall'+saveKey+doCLS+'.png')
# canvas.SaveAs(folder+'/combochnscomparisonlumiall'+saveKey+doCLS+'.eps')
# canvas.SaveAs(folder+'/combochnscomparison3abinv'+saveKey+doCLS+'.pdf')
# canvas.SaveAs(folder+'/combochnscomparison3abinv'+saveKey+doCLS+'.png')
# canvas.SaveAs(folder+'/combochnscomparison3abinv'+saveKey+doCLS+'.eps')
# canvas.SaveAs('templates_zpMass_mergeprocs_halveNTMJ_2018_8_29_comb_preARCwMCstatplots/ntmjhalvecomparison3abinv'+doCLS+'.pdf')
# canvas.SaveAs('templates_zpMass_mergeprocs_halveNTMJ_2018_8_29_comb_preARCwMCstatplots/ntmjhalvecomparison3abinv'+doCLS+'.png')
# canvas.SaveAs('templates_zpMass_mergeprocs_halveNTMJ_2018_8_29_comb_preARCwMCstatplots/ntmjhalvecomparison3abinv'+doCLS+'.eps')
