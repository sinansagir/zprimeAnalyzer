#!/usr/bin/python

import os,sys
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
import ROOT as rt
import CMS_lumi, tdrstyle

rt.gROOT.SetBatch(1)

lumi=3 #for plots
iPlots = ['zp_m_gen','zp_m']
sigs = ['rsg2','rsg3','rsg4','rsg5','rsg6','rsg8','rsg10','rsg12']
sigs = ['rsg3','rsg6','rsg12']
isRebinned = ''#'_rebinned_stat1p0'
saveKey = '_v2'
theDir = './templates_alljets_halveStatUnc_2018_10_31/'
yLog  = False

Rfiles = {}
for sig in sigs: Rfiles[sig] = rt.TFile(theDir+'outfile_'+sig+'.root')
# siglegs = {sigs[0]:'RSG (3 TeV)', sigs[1]:'RSG (6 TeV)',sigs[2]:'RSG (8 TeV)',sigs[3]:'RSG (10 TeV)',sigs[4]:'RSG (12 TeV)'}
# sigColors = {sigs[0]:rt.kBlack, sigs[1]:rt.kRed,sigs[2]:rt.kOrange,sigs[3]:rt.kBlue,sigs[4]:rt.kGreen+3}
# sigLines = {sigs[0]:1, sigs[1]:3,sigs[2]:5,sigs[3]:7,sigs[4]:7,'zp_m':3,'zp_m_gen':1}
# scFact = {sigs[0]:1, sigs[1]:1,sigs[2]:1,sigs[3]:1,sigs[4]:1,'zp_m':3,'zp_m_gen':1}
siglegs = {'rsg3':'RSG (3 TeV)', 'rsg6':'RSG (6 TeV)','rsg8':'RSG (8 TeV)','rsg10':'RSG (10 TeV)','rsg12':'RSG (12 TeV)'}
sigColors = {'rsg3':rt.kOrange, 'rsg6':rt.kRed,'rsg8':rt.kBlack,'rsg10':rt.kBlue,'rsg12':rt.kGreen+3}
sigLines = {'rsg3':1, 'rsg6':1,'rsg8':1,'rsg10':1,'rsg12':1,'zp_m':3,'zp_m_gen':1}
scFact = {'rsg3':1, 'rsg6':1,'rsg8':1,'rsg10':1,'rsg12':1,'zp_m':3,'zp_m_gen':1}

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.lumi_13TeV= "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.lumi_sqrtS = str(lumi)+" ab^{-1} (14 TeV)" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

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
R = 0.05*W_ref

tagPosX = 0.66
tagPosY = 0.35

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

	#histogram.GetYaxis().CenterTitle()
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
		hSigs[sig+'_'+iPlot] = Rfiles[sig].Get(iPlot+'_full_3000000').Clone(iPlot+'_3000p0fb_'+sig)
		#hSigs[sig+'_'+iPlot].Rebin(2)
		print sig,iPlot,hSigs[sig+'_'+iPlot].Integral()
		#hSigs[sig+'_'+iPlot].Scale(1./hSigs[sig+'_'+iPlot].Integral())
		#hSigs[sig+'_'+iPlot].Scale(scFact[sig])
		hSigs[sig+'_'+iPlot].SetLineColor(sigColors[sig])
		hSigs[sig+'_'+iPlot].SetFillStyle(0)
		if len(iPlots)==1: hSigs[sig+'_'+iPlot].SetLineStyle(1)#sigLines[sig])
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

hSigs[sigs[0]+'_'+iPlots[0]].SetMinimum(0.001)
#hSigs[sigs[0]+'_'+iPlots[0]].SetMaximum(5.e1*hSigs[sigs[0]+'_'+iPlots[0]].GetMaximum())
hSigs[sigs[0]+'_'+iPlots[0]].SetMaximum(1.2*hSigs[sigs[0]+'_'+iPlots[0]].GetMaximum())
#hSigs[sigs[0]+'_'+iPlots[0]].GetXaxis().SetRangeUser(0, 4000)
hSigs[sigs[0]+'_'+iPlots[0]].GetXaxis().SetTitle("m_{t#bar{t}} [GeV]")
hSigs[sigs[0]+'_'+iPlots[0]].GetYaxis().SetTitle("Events")
hSigs[sigs[0]+'_'+iPlots[0]].Draw("HIST")
for sig in reversed(sigs): 
	for iPlot in iPlots:
		#if sig==sigs[0] and iPlot==iPlots[0]: continue
		hSigs[sig+'_'+iPlot].Draw("SAME HIST")
uPad.RedrawAxis()

chLatex = rt.TLatex()
chLatex.SetNDC()
chLatex.SetTextSize(0.05)
chLatex.SetTextAlign(21) # align center
flvString = 'Fully hadronic'
chLatex.DrawLatex(tagPosX, tagPosY, flvString)
	
leg = rt.TLegend(0.65,0.5,0.93,0.87)
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
for sig in sigs: 
	leg.AddEntry(hSigs[sig+'_'+iPlots[0]],siglegs[sig],"l")
if len(iPlots)>1:
	dummy = rt.TH1D("","",1,0,1)
	dummy.SetLineColor(2)
	dummy.SetLineWidth(6)
	dummyGen = rt.TH1D("","",1,0,1)
	dummyGen.SetLineColor(rt.kBlack)
	dummyGen.SetFillStyle(0)
	dummyGen.SetLineWidth(6)
	dummyGen.SetLineStyle(sigLines[iPlots[0]])
	dummyGen.SetLineWidth(3)
	dummyRec = rt.TH1D("","",1,0,1)
	dummyRec.SetLineColor(rt.kBlack)
	dummyRec.SetFillStyle(0)
	dummyRec.SetLineWidth(6)
	dummyRec.SetLineStyle(sigLines[iPlots[1]])
	dummyRec.SetLineWidth(3)
	leg.AddEntry(dummy,"","")
	leg.AddEntry(dummyGen,"Generated","l")
	leg.AddEntry(dummyRec,"Reconstructed","l")
leg.Draw("same")

#draw the lumi text on the canvas
CMS_lumi.CMS_lumi(uPad, iPeriod, iPos)

if len(iPlots)==1:
	c1.SaveAs(theDir+'/'+iPlots[0]+'_signals_alljets'+saveKey+".eps")
	c1.SaveAs(theDir+'/'+iPlots[0]+'_signals_alljets'+saveKey+".pdf")
	c1.SaveAs(theDir+'/'+iPlots[0]+'_signals_alljets'+saveKey+".png")
else:
	c1.SaveAs(theDir+'/signals_alljets'+saveKey+".eps")
	c1.SaveAs(theDir+'/signals_alljets'+saveKey+".pdf")
	c1.SaveAs(theDir+'/signals_alljets'+saveKey+".png")
	
for sig in Rfiles.keys(): Rfiles[sig].Close()
