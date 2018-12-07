#!/usr/bin/python

import os,sys
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
import ROOT as rt
import CMS_lumi, tdrstyle

rt.gROOT.SetBatch(1)

lumi="15 ab^{-1}" #for plots
lumiInTemplates='15000p0fbinv'
catList = ['isE','isM']
iPlots = ['genzpMass','zpMass']
massList = range(4000,12000+1,2000)
sigs = ['ZpM'+str(mass) for mass in massList]
isRebinned = ''#'_rebinned_stat1p0'
saveKey = ''
theDir = './kinematics_SR_halveStatUnc_2018_10_31/'
yLog  = False

Rfiles = {}
for sig in sigs:
	for iPlot in iPlots: Rfiles[sig+'_'+iPlot] = rt.TFile(theDir+'templates_'+iPlot+'_'+sig+'_'+lumiInTemplates+'.root')
siglegs = {sigs[0]:'RSG (4 TeV)', sigs[1]:'RSG (6 TeV)',sigs[2]:'RSG (8 TeV)',sigs[3]:'RSG (10 TeV)',sigs[4]:'RSG (12 TeV)'}
sigColors = {sigs[0]:rt.kBlack, sigs[1]:rt.kRed,sigs[2]:rt.kOrange,sigs[3]:rt.kBlue,sigs[4]:rt.kGreen+3}
sigLines = {sigs[0]:1, sigs[1]:3,sigs[2]:5,sigs[3]:7,sigs[4]:7,'zpMass':3,'genzpMass':1}
# siglegs = {sigs[0]:'Z\' 30% width (4 TeV)', sigs[1]:'Z\' 30% width (6 TeV)',sigs[2]:'Z\' 30% width (8 TeV)',sigs[3]:'Z\' 30% width (10 TeV)',sigs[4]:'Z\' 30% width (12 TeV)'}
# sigColors = {sigs[0]:rt.kBlack, sigs[1]:rt.kRed,sigs[2]:rt.kOrange,sigs[3]:rt.kBlue,sigs[4]:rt.kGreen+3}
# sigLines = {sigs[0]:1, sigs[1]:3,sigs[2]:5,sigs[3]:7,sigs[4]:7,'zpMass':3,'genzpMass':1}

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.lumi_13TeV= "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation"
CMS_lumi.lumi_sqrtS = str(lumi)+" (27 TeV)" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 600; 
W_ref = 800; 
W = W_ref
H = H_ref

iPeriod = 0 #see CMS_lumi.py module for usage!

# references for T, B, L, R
T = 0.10*H_ref
B = 0.12*H_ref
L = 0.12*W_ref
R = 0.04*W_ref

tagPosX = 0.76
tagPosY = 0.50

def formatUpperHist(histogram):
	histogram.GetXaxis().SetLabelSize(0)
	histogram.GetXaxis().SetNdivisions(506)

	histogram.GetXaxis().SetLabelSize(0.045)
	histogram.GetXaxis().SetTitleSize(0.055)
	histogram.GetXaxis().SetTitleOffset(0.95)
	histogram.GetYaxis().SetLabelSize(0.045)
	histogram.GetYaxis().SetTitleSize(0.055)
	histogram.GetYaxis().SetTitleOffset(1.15)
	histogram.GetXaxis().SetNdivisions(506)

	histogram.GetYaxis().CenterTitle()
	histogram.SetMinimum(0.0101)
	if not yLog: 
		histogram.SetMinimum(0.015)
	if yLog:
		uPad.SetLogy()
		histogram.SetMaximum(2e2*histogram.GetMaximum())
	else: histogram.SetMaximum(1.1*histogram.GetMaximum())

hSigs = {}
for sig in sigs:
	for iPlot in iPlots:
		hSigs[sig+'_'+iPlot] = Rfiles[sig+'_'+iPlot].Get(iPlot+'_'+lumiInTemplates+'_'+catList[0]+'__sig').Clone(iPlot+'_'+lumiInTemplates+'_'+sig)
		for cat in catList:
			if cat==catList[0]: continue
			hSigs[sig+'_'+iPlot].Add(Rfiles[sig+'_'+iPlot].Get(iPlot+'_'+lumiInTemplates+'_'+cat+'__sig'))
		#hSigs[sig+'_'+iPlot].Rebin(2)
		print sig,iPlot,cat,hSigs[sig+'_'+iPlot].Integral()
		#if iPlot=='zpMass': hSigs[sig+'_'+iPlot].Scale(5.)
		#hSigs[sig+'_'+iPlot].Scale(1./hSigs[sig+'_'+iPlot].Integral())
		hSigs[sig+'_'+iPlot].SetLineColor(sigColors[sig])
		hSigs[sig+'_'+iPlot].SetFillStyle(0)
		if len(iPlots)==1: hSigs[sig+'_'+iPlot].SetLineStyle(1)#lines[sig])
		else: hSigs[sig+'_'+iPlot].SetLineStyle(sigLines[iPlot])
		hSigs[sig+'_'+iPlot].SetLineWidth(3)

c1 = rt.TCanvas("c1","c1",50,50,W,H)
c1.SetFillColor(0)
c1.SetBorderMode(0)
c1.SetFrameFillStyle(0)
c1.SetFrameBorderMode(0)
#c1.SetTickx(0)
#c1.SetTicky(0)

yDiv=0.0
uPad=rt.TPad("uPad","",0,yDiv,1,1) #for actual plots

uPad.SetLeftMargin( L/W )
uPad.SetRightMargin( R/W )
uPad.SetTopMargin( T/H )
uPad.SetBottomMargin( B/H )

uPad.SetFillColor(0)
uPad.SetBorderMode(0)
uPad.SetFrameFillStyle(0)
uPad.SetFrameBorderMode(0)
#uPad.SetTickx(0)
#uPad.SetTicky(0)
uPad.Draw()

formatUpperHist(hSigs[sigs[0]+'_'+iPlots[0]])
uPad.cd()

hSigs[sigs[0]+'_'+iPlots[0]].SetMinimum(0.00101)
#hSigs[sigs[0]+'_'+iPlots[0]].SetMaximum(5.e1*hSigs[sigs[0]+'_'+iPlots[0]].GetMaximum())
hSigs[sigs[0]+'_'+iPlots[0]].SetMaximum(1.2*hSigs[sigs[0]+'_'+iPlots[0]].GetMaximum())
#hSigs[sigs[0]+'_'+iPlots[0]].GetXaxis().SetRangeUser(0, 4000)
#hSigs[sigs[0]+'_'+iPlots[0]].GetXaxis().SetTitle("M(t#bar{t}) [GeV]")
hSigs[sigs[0]+'_'+iPlots[0]].GetYaxis().SetTitle("Events")
hSigs[sigs[0]+'_'+iPlots[0]].Draw("HIST")
for sig in sigs: 
	for iPlot in iPlots:
		if sig==sigs[0] and iPlot==iPlots[0]: continue
		hSigs[sig+'_'+iPlot].Draw("SAME HIST")
uPad.RedrawAxis()

chLatex = rt.TLatex()
chLatex.SetNDC()
chLatex.SetTextSize(0.04)
chLatex.SetTextAlign(21) # align center
flvString = 'e/#mu+jets'
chLatex.DrawLatex(tagPosX, tagPosY, flvString)
	
leg = rt.TLegend(0.65,0.6,0.93,0.87)
rt.SetOwnership( leg, 0 )   # 0 = release (not keep), 1 = keep
leg.SetShadowColor(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetLineColor(0)
leg.SetLineStyle(0)
leg.SetBorderSize(0) 
leg.SetNColumns(1)
leg.SetTextFont(62)#42)
leg.SetColumnSeparation(0.05)
if len(iPlots)!=1:
	leg.AddEntry(hSigs[sigs[0]+'_'+iPlots[0]],"Generated","l")
	leg.AddEntry(hSigs[sigs[0]+'_'+iPlots[1]],"Reconstructed","l")
for sig in sigs: 
	leg.AddEntry(hSigs[sig+'_'+iPlots[0]],siglegs[sig],"l")
leg.Draw("same")

#draw the lumi text on the canvas
CMS_lumi.CMS_lumi(uPad, iPeriod, iPos)

if len(iPlots)==1:
	c1.SaveAs(theDir+'/'+iPlots[0]+'_signals27TeV_ljets'+saveKey+".eps")
	c1.SaveAs(theDir+'/'+iPlots[0]+'_signals27TeV_ljets'+saveKey+".pdf")
	c1.SaveAs(theDir+'/'+iPlots[0]+'_signals27TeV_ljets'+saveKey+".png")
else:
	c1.SaveAs(theDir+'/signals27TeV_ljets'+saveKey+".eps")
	c1.SaveAs(theDir+'/signals27TeV_ljets'+saveKey+".pdf")
	c1.SaveAs(theDir+'/signals27TeV_ljets'+saveKey+".png")
	
for sig in Rfiles.keys(): Rfiles[sig].Close()
