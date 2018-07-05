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
signal = 'RSG'
lumiPlot = '36.0'
lumiStr = '36p0'

mass_str = ['3000','4000','5000']
theory_xsec = [0.1507,0.03617,0.01158][:len(mass_str)]#pb
scale_up = [0,0,0][:len(mass_str)]#%
scale_dn = [0,0,0][:len(mass_str)]#%
pdf_up   = [0,0,0][:len(mass_str)]#%
pdf_dn   = [0,0,0][:len(mass_str)]#%

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
sigma3=array('d',[0 for i in range(len(mass))])
sigma3err=array('d',[0 for i in range(len(mass))])
sigma5=array('d',[0 for i in range(len(mass))])
sigma5err=array('d',[0 for i in range(len(mass))])

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
CMS_lumi.lumi_sqrtS = "36 fb^{-1} (14 TeV)" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

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

def PlotLimits(limitDir,limitFile,chiral,tempKey):
    histPrefix=discriminant+'_'+str(lumiStr)+'fb'+chiral
    ljust_i = 10
    print
    print 'mass'.ljust(ljust_i), 'observed'.ljust(ljust_i), 'expected'.ljust(ljust_i), '-2 Sigma'.ljust(ljust_i), '-1 Sigma'.ljust(ljust_i), '+1 Sigma'.ljust(ljust_i), '+2 Sigma'.ljust(ljust_i)
    
    limExpected = 3
    limObserved = 3
    for i in range(len(mass)):        
        try:
        	if blind: fobs = open(limitDir+cutString+limitFile.replace(signal+'M3000',signal+'M'+mass_str[i]), 'rU')
        	else: fobs = open(limitDir+cutString+limitFile.replace(signal+'M3000',signal+'M'+mass_str[i]).replace('expected','observed'), 'rU')
        	linesObs = fobs.readlines()
        	fobs.close()
        	
        	fexp = open(limitDir+cutString+limitFile.replace(signal+'M3000',signal+'M'+mass_str[i]), 'rU')
        	linesExp = fexp.readlines()
        	fexp.close()
        	
        	f3sigma = open(limitDir+cutString+limitFile.replace(signal+'M3000',signal+'M'+mass_str[i]).replace('expected','3sigmaSignif').replace('limits_',''), 'rU')
        	lines3sigma = f3sigma.readlines()
        	f3sigma.close()
        	
        	f5sigma = open(limitDir+cutString+limitFile.replace(signal+'M3000',signal+'M'+mass_str[i]).replace('expected','5sigmaSignif').replace('limits_',''), 'rU')
        	lines5sigma = f5sigma.readlines()
        	f5sigma.close()
        	
        except: 
        	obs[i],obserr[i],exp[i],experr[i],exp68L[i],exp68H[i],exp95L[i],exp95H[i],sigma3[i],sigma3err[i],sigma5[i],sigma5err[i] = 0,0,0,0,0,0,0,0,0,0,0,0
        	print "SKIPPING SIGNAL: "+mass_str[i]
        	continue
        
        obs[i] = float(linesObs[1].strip().split()[1])
        obserr[i] = 0        
        exp[i] = float(linesExp[1].strip().split()[1])
        experr[i] = 0
        exp68L[i] = float(linesExp[1].strip().split()[4])
        exp68H[i] = float(linesExp[1].strip().split()[5])
        exp95L[i] = float(linesExp[1].strip().split()[2])
        exp95H[i] = float(linesExp[1].strip().split()[3])
        sigma3[i] = float(lines3sigma[1].strip().split()[0])
        sigma3err[i] = 0
        sigma5[i] = float(lines5sigma[1].strip().split()[0])
        sigma5err[i] = 0
    
        if i!=0:
        	if(exp[i]>theory_xsec[i] and exp[i-1]<theory_xsec[i-1]) or (exp[i]<theory_xsec[i] and exp[i-1]>theory_xsec[i-1]):
        		limExpected,ycross = getSensitivity(i,exp)
        	if(obs[i]>theory_xsec[i] and obs[i-1]<theory_xsec[i-1]) or (obs[i]<theory_xsec[i] and obs[i-1]>theory_xsec[i-1]):
        		limObserved,ycross = getSensitivity(i,obs)
        		
        exp95L[i]=(exp[i]-exp95L[i])
        exp95H[i]=abs(exp[i]-exp95H[i])
        exp68L[i]=(exp[i]-exp68L[i])
        exp68H[i]=abs(exp[i]-exp68H[i])

        round_i = 3
        print str(int(mass[i])).ljust(ljust_i), '& '+str(round(obs[i],round_i)).ljust(ljust_i), '& '+str(round(exp[i],round_i)).ljust(ljust_i), '& '+str(round(exp95L[i],round_i)).ljust(ljust_i), '& '+str(round(exp68L[i],round_i)).ljust(ljust_i), '& '+str(round(exp68H[i],round_i)).ljust(ljust_i), '& '+str(round(exp95H[i],round_i)).ljust(ljust_i)+' \\\\'
    print
    signExp = "="
    signObs = "="
    if limExpected==3: signExp = "<"
    if limObserved==3: signObs = "<"
    print "Expected lower limit "+signExp,round(limExpected,2),"TeV"
    print "Observed lower limit "+signObs,round(limObserved,2),"TeV"
    print

    massv = rt.TVectorD(len(mass),mass)
    expv  = rt.TVectorD(len(mass),exp)
    exp68Hv = rt.TVectorD(len(mass),exp68H)
    exp68Lv = rt.TVectorD(len(mass),exp68L)
    exp95Hv = rt.TVectorD(len(mass),exp95H)
    exp95Lv = rt.TVectorD(len(mass),exp95L)

    obsv = rt.TVectorD(len(mass),obs)
    masserrv = rt.TVectorD(len(mass),masserr)
    obserrv = rt.TVectorD(len(mass),obserr)
    experrv = rt.TVectorD(len(mass),experr)
    
    sigma3v = rt.TVectorD(len(mass),sigma3)
    sigma5v = rt.TVectorD(len(mass),sigma5)
    sigma3errv = rt.TVectorD(len(mass),sigma3err)
    sigma5errv = rt.TVectorD(len(mass),sigma5err)

    observed = rt.TGraphAsymmErrors(massv,obsv,masserrv,masserrv,obserrv,obserrv)
    observed.SetLineColor(rt.kBlack)
    observed.SetLineWidth(2)
    observed.SetMarkerStyle(20)
    expected = rt.TGraphAsymmErrors(massv,expv,masserrv,masserrv,experrv,experrv)
    expected.SetLineColor(rt.kBlue)
    expected.SetLineWidth(2)
    expected.SetLineStyle(2)
    expected68 = rt.TGraphAsymmErrors(massv,expv,masserrv,masserrv,exp68Lv,exp68Hv)
    expected68.SetFillColor(rt.kGreen+1)
    expected95 = rt.TGraphAsymmErrors(massv,expv,masserrv,masserrv,exp95Lv,exp95Hv)
    expected95.SetFillColor(rt.kOrange)
    
    sigma3gr = rt.TGraphAsymmErrors(massv,sigma3v,masserrv,masserrv,sigma3errv,sigma3errv)
    sigma3gr.SetLineColor(rt.kBlue)
    sigma3gr.SetLineWidth(2)
    sigma3gr.SetMarkerStyle(20)
    sigma5gr = rt.TGraphAsymmErrors(massv,sigma5v,masserrv,masserrv,sigma5errv,sigma5errv)
    sigma5gr.SetLineColor(rt.kGreen)
    sigma5gr.SetLineWidth(2)
    sigma5gr.SetMarkerStyle(20)

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

    XaxisTitle = "g^{RS}_{KK} mass [TeV]"
    YaxisTitle = "#sigma(g^{RS}_{KK}) [pb]"

#     expected95.Draw("a3")
#     expected95.GetYaxis().SetRangeUser(.001+.00001,1.45)
#     expected95.GetXaxis().SetRangeUser(mass[0],mass[-1])
#     expected95.GetXaxis().SetTitle(XaxisTitle)
#     expected95.GetXaxis().SetTitleOffset(1)
#     expected95.GetYaxis().SetTitle(YaxisTitle)
#     expected95.GetYaxis().SetTitleOffset(1)
# 		
#     expected68.Draw("3same")
#     expected.Draw("same")
    expected.Draw("AL")
    expected.GetYaxis().SetRangeUser(.001+.00001,1.45)
    expected.GetXaxis().SetRangeUser(mass[0],mass[-1])
    expected.GetXaxis().SetTitle(XaxisTitle)
    expected.GetXaxis().SetTitleOffset(1)
    expected.GetYaxis().SetTitle(YaxisTitle)
    expected.GetYaxis().SetTitleOffset(1)
    
    sigma3gr.Draw("same")
    sigma5gr.Draw("same")

    if not blind: observed.Draw("cpsame")
    theory_xsec_gr.SetLineColor(2)
    theory_xsec_gr.SetLineStyle(1)
    theory_xsec_gr.SetLineWidth(2)
    theory_xsec_gr.Draw("3same") 
    theory.SetLineColor(2)
    theory.SetLineStyle(1)
    theory.SetLineWidth(2)
    theory.Draw("same")                                                             
        
    #draw the lumi text on the canvas
    CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)

    legend = rt.TLegend(.37,.69,.94,.89) # top right
    if not blind: legend.AddEntry(observed, "95% CL observed", "lp")
    legend.AddEntry(expected68, "68% expected", "f")
    legend.AddEntry(expected, "Median expected", "l")
    legend.AddEntry(expected95, "95% expected", "f")
    legend.AddEntry(theory_xsec_gr, "Signal cross section", "lf")
    legend.AddEntry(sigma3gr , '3#sigma', "l")
    legend.AddEntry(sigma5gr , '5#sigma', "l")

    legend.SetShadowColor(0)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.SetNColumns(2)
    legend.Draw()
    
    canvas.cd()
    canvas.Update()
    canvas.RedrawAxis()
    frame = canvas.GetFrame()
    frame.Draw()

    folder = '.'
    outDir=folder+'/'+limitDir.split('/')[-3]+'plots'
    if not os.path.exists(outDir): os.system('mkdir '+outDir)
    plotName = 'SignificancePlot_'+histPrefix+'_rebinned_stat'+str(binning).replace('.','p')+saveKey+'_'+tempKey
    if blind: plotName+='_blind'
    canvas.SaveAs(outDir+'/'+plotName+'.eps')
    canvas.SaveAs(outDir+'/'+plotName+'.pdf')
    canvas.SaveAs(outDir+'/'+plotName+'.png')
    return round(limExpected,2), round(limObserved,2)

iPlotList=['RSGMass']
tempKeys = ['all']
cutString=''
dirs = {
		'RSGKK':'templates_2018_4_29_test',
		}
dirKeyList = ['RSGKK']
binnings = ['0p5']#,'0p75','1p0','1p1']

expLims = {}
obsLims = {}
for discriminant in iPlotList:
	for dirKey in dirKeyList:
		dir = dirs[dirKey]
		expLims[dirKey+discriminant] = {}
		obsLims[dirKey+discriminant] = {}
		for binning in binnings:
			expLims[dirKey+discriminant][binning] = []
			obsLims[dirKey+discriminant][binning] = []
			for tempKey in tempKeys:
				limitDir='/user_data/ssagir/Zprime_limits_2018/'+dir+'/'+tempKey+'/'
				limitFile='/limits_templates_'+discriminant+'_'+signal+'M3000'+'_'+str(lumiStr)+'fb_rebinned_stat'+str(binning).replace('.','p')+'_expected.txt'	
				print limitDir+cutString+limitFile
				expTemp,obsTemp = PlotLimits(limitDir,limitFile,'',tempKey)
				expLims[dirKey+discriminant][binning].append(expTemp)
				obsLims[dirKey+discriminant][binning].append(obsTemp)

for discriminant in iPlotList:
	print discriminant
	for dirKey in dirKeyList: print dirKey,
	print
	for ind in range(len(tempKeys)):
		print "////////////////////////////////"
		print "Channel Configuration: "+tempKeys[ind]
		print "////////////////////////////////"
		for binning in binnings:
			for dirKey in dirKeyList:
				print dirKey+'_'+binning,
		print
		print "Expected:"
		for binning in binnings:
			for dirKey in dirKeyList: 
				print expLims[dirKey+discriminant][binning][ind],
		print
		print "Observed:"
		for binning in binnings:
			for dirKey in dirKeyList: 
				print obsLims[dirKey+discriminant][binning][ind],
		print

