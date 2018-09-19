#!/usr/bin/python

import os,sys,pickle

input = 'dummy.root'

rFileName = input.split('/')[-1].replace('.root','')

thisDir = os.getcwd()

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
		
		#clean_workdir()
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

def get_model():
	model = build_model_from_rootfile(inputSL,include_mc_uncertainties=False)#,histogram_filter = (lambda s: s.count('jec')==0 and s.count('jer')==0)
	
	model.fill_histogram_zerobins()
	model.set_signal_processes('sig')
	
	procs = model.processes
	obsvs = model.observables.keys()
	
	for obs in obsvs:
		if 'isE' in obs:
			try: model.add_lognormal_uncertainty('eff_el', math.log(1.01), '*', obs)
			except: pass
		elif 'isM' in obs:
			try: model.add_lognormal_uncertainty('eff_mu', math.log(1.005), '*', obs)
			except: pass
	try: model.add_lognormal_uncertainty('lumi', math.log(1.01), '*', '*')
	except: pass
	try: model.add_lognormal_uncertainty('jec', math.log(1.035), '*', '*')
	except: pass
	try: model.add_lognormal_uncertainty('jer', math.log(1.03), '*', '*')
	except: pass
	if 'nobtagcats' not in thisDir:
		try: model.add_lognormal_uncertainty('btag', math.log(1.05), '*', '*')
		except: pass
	try: model.add_lognormal_uncertainty('ttag', math.log(1.05), '*', '*')
	except: pass
	try: model.add_lognormal_uncertainty('pdf', math.log(1.024), '*', '*')
	except: pass
	for proc in procs:
		if proc=='ttbar':
			try: model.add_lognormal_uncertainty('xsec_ttbar', math.log(1.03), proc, '*') #B2G-17-017-V9: 20%, scaled by lumi
			except: pass
			try: model.add_lognormal_uncertainty('muRF_ttbar', math.log(1.04), proc, '*')
			except: pass
		elif proc=='sitop':
			try: model.add_lognormal_uncertainty('xsec_sitop', math.log(1.06), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
			except: pass
		elif proc=='wjets':
			try: model.add_lognormal_uncertainty('xsec_wjets', math.log(1.03), proc, '*') #B2G-17-017-V9: 25%, scaled by lumi
			except: pass
			try: model.add_lognormal_uncertainty('muRF_wjets', math.log(1.03), proc, '*')
			except: pass
		elif proc=='zjets':
			try: model.add_lognormal_uncertainty('xsec_zjets', math.log(1.06), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
			except: pass
		elif proc=='dibos':
			try: model.add_lognormal_uncertainty('xsec_dibos', math.log(1.06), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
			except: pass
		elif proc=='qcd':
			try: model.add_lognormal_uncertainty('xsec_qcd', math.log(1.06), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
			except: pass
		elif proc=='other':
			try: model.add_lognormal_uncertainty('xsec_other', math.log(1.12), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
			except: pass
			
	return model

def get_model_statOnly():
	model = build_model_from_rootfile(input,include_mc_uncertainties=True)#,histogram_filter = (lambda s: s.count('jec')==0 and s.count('jer')==0)
	
	model.fill_histogram_zerobins()
	model.set_signal_processes('sig')
			
	return model

def get_model_2xSyst():
	model = build_model_from_rootfile(inputSL,include_mc_uncertainties=False)#,histogram_filter = (lambda s: s.count('jec')==0 and s.count('jer')==0)
	
	model.fill_histogram_zerobins()
	model.set_signal_processes('sig')
	
	procs = model.processes
	obsvs = model.observables.keys()
	
	for obs in obsvs:
		if 'isE' in obs:
			try: model.add_lognormal_uncertainty('eff_el', math.log(1.02), '*', obs)
			except: pass
		elif 'isM' in obs:
			try: model.add_lognormal_uncertainty('eff_mu', math.log(1.01), '*', obs)
			except: pass
	try: model.add_lognormal_uncertainty('lumi', math.log(1.02), '*', '*')
	except: pass
	try: model.add_lognormal_uncertainty('jec', math.log(1.07), '*', '*')
	except: pass
	try: model.add_lognormal_uncertainty('jer', math.log(1.06), '*', '*')
	except: pass
	if 'nobtagcats' not in thisDir:
		try: model.add_lognormal_uncertainty('btag', math.log(1.10), '*', '*')
		except: pass
	try: model.add_lognormal_uncertainty('ttag', math.log(1.10), '*', '*')
	except: pass
	try: model.add_lognormal_uncertainty('pdf', math.log(1.048), '*', '*')
	except: pass
	for proc in procs:
		if proc=='ttbar':
			try: model.add_lognormal_uncertainty('xsec_ttbar', math.log(1.06), proc, '*') #B2G-17-017-V9: 20%, scaled by lumi
			except: pass
			try: model.add_lognormal_uncertainty('muRF_ttbar', math.log(1.08), proc, '*')
			except: pass
		elif proc=='sitop':
			try: model.add_lognormal_uncertainty('xsec_sitop', math.log(1.12), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
			except: pass
		elif proc=='wjets':
			try: model.add_lognormal_uncertainty('xsec_wjets', math.log(1.06), proc, '*') #B2G-17-017-V9: 25%, scaled by lumi
			except: pass
			try: model.add_lognormal_uncertainty('muRF_wjets', math.log(1.06), proc, '*')
			except: pass
		elif proc=='zjets':
			try: model.add_lognormal_uncertainty('xsec_zjets', math.log(1.12), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
			except: pass
		elif proc=='dibos':
			try: model.add_lognormal_uncertainty('xsec_dibos', math.log(1.12), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
			except: pass
		elif proc=='qcd':
			try: model.add_lognormal_uncertainty('xsec_qcd', math.log(1.12), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
			except: pass
		elif proc=='other':
			try: model.add_lognormal_uncertainty('xsec_other', math.log(1.24), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
			except: pass
			
	return model
		
model = get_model()

##################################################################################################################

model_summary(model)

doLimits = True
if doLimits:
	#plot_exp, plot_obs = bayesian_limits(model,'expected', n_toy = 100000, n_data = 1000, run_theta = 'True')
	plot_exp, plot_obs = bayesian_limits(model,'expected', n_toy = 5000, n_data = 500, run_theta = 'True')
	plot_exp.write_txt('limits_'+rFileName+'_expected.txt')
else: #N sigma discovery reaches (NOTE that this implementation currently works only with utils/theta-auto.py, check if this is OK or if it can be implemented in utils2 easily!!!)
	getNSigmaCrossSecMin(model,5,0.01)
	getNSigmaCrossSecMin(model,3,0.01)

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
