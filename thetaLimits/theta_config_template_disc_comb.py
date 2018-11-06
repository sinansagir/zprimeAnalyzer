#!/usr/bin/python

import os,sys,math,pickle,json

inputSL = 'dummy.root'
inputAH = 'dummy.root'

rFileName = inputSL.split('/')[-1].replace('.root','')

thisDir = os.getcwd()
		
##################################################################################################################

systslj={
'eff_el':.01,
'eff_mu':.005,
'lumi':.01,
'jec':.02,
'jer':.03,
'btag':.01,
'mistag':.10,
'ttag':.05,
'pdf':.024,
'muRF_ttbar':.04, #B2G-17-017-V9: ~30%, scaled by lumi
'muRF_wjets':.03, #B2G-17-017-V9: ~25%, scaled by lumi
'xsec_ttbar':.03, #B2G-17-017-V9: 20%, scaled by lumi
'xsec_sitop':.06, #B2G-17-017-V9: 50%, scaled by lumi
'xsec_wjets':.03, #B2G-17-017-V9: 25%, scaled by lumi
'xsec_zjets':.06, #B2G-17-017-V9: 50%, scaled by lumi
'xsec_dibos':.06, #B2G-17-017-V9: 50%, scaled by lumi
'xsec_qcd':.06, #B2G-17-017-V9: 50%, scaled by lumi
}
systslj['xsec_other']=math.sqrt(systslj['xsec_sitop']**2+systslj['xsec_wjets']**2+systslj['xsec_zjets']**2+systslj['xsec_dibos']**2+systslj['xsec_qcd']**2+systslj['muRF_wjets']**2)

systsaj={
'lumi':.01,
'jec':.02,
'jer':.03,
'btag':.01,
'mistag':.10,
'ttag':.05,
'pdf':.024,
'muRF_ttbar':.04, #B2G-17-017-V9: ~30%, scaled by lumi
'xsec_ttbar':.03, #B2G-17-017-V9: 20%, scaled by lumi
'modmass':.02,
'closure':.05,
}

##################################################################################################################

def getNSigmaCrossSecMin(model, N=5, errorMax=0.001):
	outFile=open(rFileName+'_'+str(N)+'sigmaSignif.txt','w')
	result={}
	
	signals=model.signal_process_groups.keys()
	#signals.sort(key=lambda x:int(x[re.search("\d",x).start():]))
	
	beta={}
	signif={}
	converged={}
	for signal in signals:
		if not beta.has_key(signal):
			beta[signal]=1
			signif[signal]=-999
			converged[signal]=False
			
	while True:
		
		clean_workdir()
		signif=exp_significance_approx(model)
		
		for signal in signals:
		
			s=signif[signal]
			if abs(s-N)/s < errorMax:
				converged[signal]=True
				result[signal]=beta[signal]
				
			SF=N/s
			model.scale_predictions(SF,signal)  #for models with a single observable
			beta[signal]*=SF
			
			print signal, s
			
		allConverged=True
		for signal in signals:
			if not converged[signal]: allConverged=False
		if allConverged: break
	
	outFile.write("# Cross section for "+str(N)+" sigma significance:\n")
	for signal in signals:
		mass=''.join([str(s) for s in signal.split('_')[0] if s.isdigit()])
		outFile.write(mass+'   '+str(result[signal])+'\n')
		
	for signal in signals:
		model.scale_predictions(1/beta[signal],signal)

##################################################################################################################

def get_model_ljets(incMCstat=True, isStatOnly=False, systFact=1):
	model = build_model_from_rootfile(inputSL,include_mc_uncertainties=incMCstat,histogram_filter = (lambda s: s.count('jec')==0))# and s.count('jer')==0)
	
	model.fill_histogram_zerobins()
	model.set_signal_processes('sig')
		
	if not isStatOnly:
		procs = model.processes
		obsvs = model.observables.keys()
		for obs in obsvs:
			if 'isE' in obs:
				try: model.add_lognormal_uncertainty('eff_el', math.log(1.0+systFact*systslj['eff_el']), '*', obs)
				except: pass
			elif 'isM' in obs:
				try: model.add_lognormal_uncertainty('eff_mu', math.log(1.0+systFact*systslj['eff_mu']), '*', obs)
				except: pass
		try: model.add_lognormal_uncertainty('lumi', math.log(1.0+systFact*systslj['lumi']), '*', '*')
		except: pass
		try: model.add_lognormal_uncertainty('jec', math.log(1.0+systFact*systslj['jec']), '*', '*')
		except: pass
		try: model.add_lognormal_uncertainty('jer', math.log(1.0+systFact*systslj['jer']), '*', '*')
		except: pass
		if any(['_nB' in obs for obs in obsvs]):
			try: model.add_lognormal_uncertainty('btag', math.log(1.0+systFact*systslj['btag']), '*', '*')
			except: pass
			try: model.add_lognormal_uncertainty('mistag', math.log(1.0+systFact*systslj['mistag']), '*', '*')
			except: pass
		try: model.add_lognormal_uncertainty('ttag', math.log(1.0+systFact*systslj['ttag']), '*', '*')
		except: pass
		try: model.add_lognormal_uncertainty('pdf', math.log(1.0+systFact*systslj['pdf']), '*', '*')
		except: pass
		for proc in procs:
			if proc=='ttbar':
				try: model.add_lognormal_uncertainty('xsec_ttbar', math.log(1.0+systFact*systslj['xsec_ttbar']), proc, '*') #B2G-17-017-V9: 20%, scaled by lumi
				except: pass
				try: model.add_lognormal_uncertainty('muRF_ttbar', math.log(1.0+systFact*systslj['muRF_ttbar']), proc, '*') #B2G-17-017-V9: ~30%, scaled by lumi
				except: pass
			elif proc=='sitop':
				try: model.add_lognormal_uncertainty('xsec_sitop', math.log(1.0+systFact*systslj['xsec_sitop']), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
				except: pass
			elif proc=='wjets':
				try: model.add_lognormal_uncertainty('xsec_wjets', math.log(1.0+systFact*systslj['xsec_wjets']), proc, '*') #B2G-17-017-V9: 25%, scaled by lumi
				except: pass
				try: model.add_lognormal_uncertainty('muRF_wjets', math.log(1.0+systFact*systslj['muRF_wjets']), proc, '*') #B2G-17-017-V9: ~25%, scaled by lumi
				except: pass
			elif proc=='zjets':
				try: model.add_lognormal_uncertainty('xsec_zjets', math.log(1.0+systFact*systslj['xsec_zjets']), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
				except: pass
			elif proc=='dibos':
				try: model.add_lognormal_uncertainty('xsec_dibos', math.log(1.0+systFact*systslj['xsec_dibos']), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
				except: pass
			elif proc=='qcd':
				try: model.add_lognormal_uncertainty('xsec_qcd', math.log(1.0+systFact*systslj['xsec_qcd']), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
				except: pass
			elif proc=='other':
				try: model.add_lognormal_uncertainty('xsec_other', math.log(1.0+systFact*systslj['xsec_other']), proc, '*')
				except: pass
			
	return model

##################################################################################################################

def get_model_alljets(incMCstat=True, isStatOnly=False, systFact=1):
	model = build_model_from_rootfile(inputAH,include_mc_uncertainties=incMCstat,histogram_filter = (lambda s: s.count('jec')==0))# and s.count('jer')==0)
	
	model.fill_histogram_zerobins()
	model.set_signal_processes('sig')
	
	if not isStatOnly:
		procs = model.processes
		for proc in procs:
			if proc!='qcd':
				try: model.add_lognormal_uncertainty('lumi', math.log(1.0+systFact*systsaj['lumi']), proc, '*')
				except: pass
				try: model.add_lognormal_uncertainty('jec', math.log(1.0+systFact*systsaj['jec']), proc, '*')
				except: pass
				try: model.add_lognormal_uncertainty('jer', math.log(1.0+systFact*systsaj['jer']), proc, '*')
				except: pass
				try: model.add_lognormal_uncertainty('btag', math.log(1.0+systFact*systsaj['btag']), proc, '*')
				except: pass
				try: model.add_lognormal_uncertainty('mistag', math.log(1.0+systFact*systsaj['mistag']), proc, '*')
				except: pass
				try: model.add_lognormal_uncertainty('ttag', math.log(1.0+systFact*systsaj['ttag']), proc, '*')
				except: pass
				try: model.add_lognormal_uncertainty('pdf', math.log(1.0+systFact*systsaj['pdf']), proc, '*')
				except: pass
			if proc=='ttbar':
				try: model.add_lognormal_uncertainty('xsec_ttbar', math.log(1.0+systFact*systsaj['xsec_ttbar']), proc, '*')
				except: pass
				try: model.add_lognormal_uncertainty('muRF_ttbar', math.log(1.0+systFact*systsaj['muRF_ttbar']), proc, '*')
				except: pass
			if proc=='qcd':
				try: model.add_lognormal_uncertainty('modmass', math.log(1.0+systFact*systsaj['modmass']), proc, '*')
				except: pass
				try: model.add_lognormal_uncertainty('closure', math.log(1.0+systFact*systsaj['closure']), proc, '*')
				except: pass
			
	return model	

##################################################################################################################

model = get_model_ljets()
alljetsModel = get_model_alljets()
model.combine(alljetsModel)
model_summary(model)

##################################################################################################################

xsec = {}
xsec['ZpM2000']  = 1.3*1.153
xsec['ZpM3000']  = 1.3*1.556*0.1
xsec['ZpM4000']  = 1.3*3.585*0.01
xsec['ZpM5000']  = 1.3*1.174*0.01
xsec['ZpM6000']  = 1.3*4.939*0.001
xsec['ZpM8000']  = 1.3*1.403*0.001
xsec['ZpM10000'] = 1.3*5.527*0.0001
xsec['ZpM12000'] = 1.3*2.622*0.0001
xsec['ZpW30M2000']  = xsec['ZpM2000']
xsec['ZpW30M3000']  = xsec['ZpM3000']
xsec['ZpW30M4000']  = xsec['ZpM4000']
xsec['ZpW30M5000']  = xsec['ZpM5000']
xsec['ZpW30M6000']  = xsec['ZpM6000']
xsec['ZpW30M8000']  = xsec['ZpM8000']
xsec['ZpW30M10000'] = xsec['ZpM10000']
xsec['ZpW30M12000'] = xsec['ZpM12000']
xs=xsec[rFileName.split('_')[2]]
print "xsec["+rFileName.split('_')[2]+"] =",xs

##################################################################################################################

doLimits = True
if doLimits:
	#exp, obs = bayesian_limits(model, what='expected', n_toy = 100000, n_data = 1000, run_theta = 'True')
	exp, obs = bayesian_limits(model, what='expected', n_toy = 5000, n_data = 500, run_theta = 'True')
	exp.write_txt('limits_'+rFileName+'_expected.txt')
	options = Options()
	options.set('minimizer', 'strategy', 'robust')
	options.set('minimizer', 'minuit_tolerance_factor', '100')
	exp_acls, obs_acls = asymptotic_cls_limits(model, use_data=False, signal_process_groups={'': ['sig']}, beta_signal_expected=0.0, bootstrap_model=False, options=options)#, input=None, n=1)
	f_acls = open('limits_'+rFileName+'_acls_expected.txt', 'w')
	print >>f_acls, exp_acls
	f_acls.close()
# 	exp_cls, obs_cls = cls_limits(model, use_data=False, signal_process_groups={'': ['sig']}, options=options)#, nuisance_prior=None, frequentist_bootstrapping=False, cls_options={}, seed=None)
# 	f_cls = open('limits_'+rFileName+'_cls_expected.txt', 'w')
# 	print >>f_cls, exp_cls
# 	f_cls.close()

else: #N sigma discovery reaches (NOTE that this implementation currently works only with utils/theta-auto.py, check if this is OK or if it can be implemented in utils2 easily!!!)
	getNSigmaCrossSecMin(model,3,0.01)
	getNSigmaCrossSecMin(model,5,0.01)

#report.write_html('htmlout_'+rFileName)

doPostfit=True
if doLimits and doPostfit:
	options = Options()
	options.set('minimizer', 'strategy', 'robust')
	options.set('minimizer', 'minuit_tolerance_factor', '100000')
	parVals = mle(model, input='toys:0.0', n=1, with_error=True, with_covariance=True, options = options)

	parameter_values = {}
	for syst in parVals['sig'].keys():
		if syst=='__nll' or syst=='__cov': continue
		else:
			print syst,"=",parVals['sig'][syst][0][0],"+/-",parVals['sig'][syst][0][1]
			parameter_values[syst] = parVals['sig'][syst][0][0]

	pickle.dump(parVals,open(rFileName+'.p','wb'))

	histos = evaluate_prediction(model, parameter_values, include_signal=False)
	write_histograms_to_rootfile(histos, 'histos-mle_'+rFileName+'.root')

	from numpy import linalg
	import numpy as np

	theta_res = parVals['sig']
	param_list = []
	for k, res in theta_res.iteritems():
		#print k,',',res
		if any(k == i for i in ['__nll','__cov']): continue
		err_sq = res[0][1]*res[0][1]
		param_list.append((k, err_sq))

	cov_matrix = theta_res['__cov'][0]
	ind_dict = {}
	for i in xrange(cov_matrix.shape[0]):
		for ii in xrange(cov_matrix.shape[1]):
			entry = cov_matrix[i,ii]
			for proc, val in param_list:
				if abs(val-entry) < 1e-9:
					if i != ii:
						print "WARNING row and column index don't match"
					ind_dict[i] = proc
				if i not in ind_dict.keys():
					ind_dict[i] = 'beta_signal'

	cov_matrix = np.matrix(cov_matrix)
	diag_matrix = np.matrix(np.sqrt(np.diag(np.diag(cov_matrix))))

	inv_matrix = diag_matrix.I
	corr_matrix = inv_matrix * cov_matrix * inv_matrix

	corr_hist = ROOT.TH2D("correlation_matrix","",len(param_list),0,len(param_list),len(param_list),0,len(param_list))
	cov_hist = ROOT.TH2D("covariance_matrix","",len(param_list),0,len(param_list),len(param_list),0,len(param_list))
	
	for i in xrange(corr_matrix.shape[0]):
		if i not in ind_dict.keys(): continue
		corr_hist.GetXaxis().SetBinLabel(i+1, ind_dict.get(i,'unknown'))
		corr_hist.GetYaxis().SetBinLabel(i+1, ind_dict.get(i,'unknown'))
		cov_hist.GetXaxis().SetBinLabel(i+1, ind_dict.get(i,'unknown'))
		cov_hist.GetYaxis().SetBinLabel(i+1, ind_dict.get(i,'unknown'))
		corr_hist.SetLabelSize(0.03,'x')
		cov_hist.SetLabelSize(0.03,'x')
		corr_hist.GetZaxis().SetRangeUser(-1,1)
		for ii in xrange(corr_matrix.shape[1]):
			entry_corr = corr_matrix[i,ii]
			entry_cov = cov_matrix[i,ii]
			corr_hist.Fill(i,ii,entry_corr)
			cov_hist.Fill(i,ii,entry_cov)

	matrices = ROOT.TFile('mle_covcorr_'+rFileName+'.root','RECREATE')
	cov_hist.Write()
	corr_hist.Write()
	matrices.Close()
