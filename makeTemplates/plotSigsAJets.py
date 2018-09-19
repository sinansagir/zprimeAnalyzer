#!/usr/bin/python

import os,sys
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
import ROOT as rt
import CMS_lumi, tdrstyle

rt.gROOT.SetBatch(1)

lumi=3000 #for plots
catList = ['isE','isM']
iPlots = ['zp_m']#,'zp_m']
signals = ['rsg2','rsg3','rsg4','rsg5','rsg6']
#signals = ['rsg2','rsg4','rsg6']
isRebinned = ''#'_rebinned_stat1p0'
theDir = './templates_alljets_2018_9_11/'
yLog  = False

Rfiles = {}
for sig in signals: Rfiles[sig] = rt.TFile(theDir+'outfile_'+sig+'.root')
legs   = {'rsg2':'RSG (2 TeV)','rsg3':'RSG (3 TeV)','rsg4':'RSG (4 TeV)','rsg5':'RSG (5 TeV)','rsg6':'RSG (6 TeV)'}
colors = {'rsg2':rt.kBlack,    'rsg3':rt.kRed,      'rsg4':rt.kOrange,   'rsg5':rt.kBlue,     'rsg6':rt.kGreen+3}
lines  = {'rsg2':1,            'rsg3':3,            'rsg4':5,            'rsg5':7,            'rsg6':7,'zp_m':3,'zp_m_gen':1}

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.lumi_13TeV= "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation"
CMS_lumi.lumi_sqrtS = str(lumi)+" fb^{-1} (14 TeV)" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

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

tagPosX = 0.78
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
for sig in signals:
	for iPlot in iPlots:
		hSigs[sig+'_'+iPlot] = Rfiles[sig].Get(iPlot+'_full_3000000').Clone(iPlot+'_3000p0fb_'+sig)
		#hSigs[sig+'_'+iPlot].Rebin(2)
		print sig,iPlot,hSigs[sig+'_'+iPlot].Integral()
		#hSigs[sig+'_'+iPlot].Scale(1./hSigs[sig+'_'+iPlot].Integral())
		hSigs[sig+'_'+iPlot].SetLineColor(colors[sig])
		hSigs[sig+'_'+iPlot].SetFillStyle(0)
		if len(iPlots)==1: hSigs[sig+'_'+iPlot].SetLineStyle(1)#lines[sig])
		else: hSigs[sig+'_'+iPlot].SetLineStyle(lines[iPlot])
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

formatUpperHist(hSigs[signals[0]+'_'+iPlots[0]])
uPad.cd()

hSigs[signals[0]+'_'+iPlots[0]].SetMinimum(0.00101)
#hSigs[signals[0]+'_'+iPlots[0]].SetMaximum(5.e1*hSigs[signals[0]+'_'+iPlots[0]].GetMaximum())
hSigs[signals[0]+'_'+iPlots[0]].SetMaximum(1.2*hSigs[signals[0]+'_'+iPlots[0]].GetMaximum())
#hSigs[signals[0]+'_'+iPlots[0]].GetXaxis().SetRangeUser(0, 4000)
hSigs[signals[0]+'_'+iPlots[0]].GetXaxis().SetTitle("M(t#bar{t})")
hSigs[signals[0]+'_'+iPlots[0]].GetYaxis().SetTitle("Events")
hSigs[signals[0]+'_'+iPlots[0]].Draw("HIST")
for sig in signals: 
	for iPlot in iPlots:
		if sig==signals[0] and iPlot==iPlots[0]: continue
		hSigs[sig+'_'+iPlot].Draw("SAME HIST")
uPad.RedrawAxis()

chLatex = rt.TLatex()
chLatex.SetNDC()
chLatex.SetTextSize(0.04)
chLatex.SetTextAlign(21) # align center
flvString = 'fully hadronic'
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
if len(iPlots)>1:
	leg.AddEntry(hSigs[signals[0]+'_'+iPlots[0]],"Generated","l")
	leg.AddEntry(hSigs[signals[0]+'_'+iPlots[1]],"Reconstructed","l")
for sig in signals: 
	leg.AddEntry(hSigs[sig+'_'+iPlots[0]],legs[sig],"l")
leg.Draw("same")

#draw the lumi text on the canvas
CMS_lumi.CMS_lumi(uPad, iPeriod, iPos)

if len(iPlots)==1:
	c1.SaveAs(theDir+'/'+iPlots[0]+'_signals_alljets'+".eps")
	c1.SaveAs(theDir+'/'+iPlots[0]+'_signals_alljets'+".pdf")
	c1.SaveAs(theDir+'/'+iPlots[0]+'_signals_alljets'+".png")
else:
	c1.SaveAs(theDir+'/signals_alljets'+".eps")
	c1.SaveAs(theDir+'/signals_alljets'+".pdf")
	c1.SaveAs(theDir+'/signals_alljets'+".png")
	
for sig in Rfiles.keys(): Rfiles[sig].Close()
