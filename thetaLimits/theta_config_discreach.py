#!/usr/bin/python

input = 'dummy.root'

rFileName = input.split('/')[-1].replace('.root','')

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
	model = build_model_from_rootfile(input,include_mc_uncertainties=False)#,histogram_filter = (lambda s: s.count('jec')==0 and s.count('jer')==0)
	
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
	try: model.add_lognormal_uncertainty('pileup', math.log(1.03), '*', '*')
	except: pass
	try: model.add_lognormal_uncertainty('jec', math.log(1.035), '*', '*')
	except: pass
	try: model.add_lognormal_uncertainty('jer', math.log(1.03), '*', '*')
	except: pass
	try: model.add_lognormal_uncertainty('btag', math.log(1.10), '*', '*')
	except: pass
	try: model.add_lognormal_uncertainty('ttag', math.log(1.10), '*', '*')
	except: pass
	try: model.add_lognormal_uncertainty('pdf', math.log(1.024), '*', '*')
	except: pass
	try: model.add_lognormal_uncertainty('muRF', math.log(1.10), '*', '*')
	except: pass
	for proc in procs:
		if proc=='tt':
			try: model.add_lognormal_uncertainty('xsec_ttbar', math.log(1.03), proc, '*') #B2G-17-017-V9: 20%
			except: pass
			try: model.add_lognormal_uncertainty('toppt', math.log(1.06), proc, '*')
			except: pass
		elif proc=='sitop':
			try: model.add_lognormal_uncertainty('xsec_sitop', math.log(1.06), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
			except: pass
		elif proc=='wjets':
			try: model.add_lognormal_uncertainty('xsec_wjets', math.log(1.03), proc, '*') #B2G-17-017-V9: 25%, scaled by lumi
			except: pass
		elif proc=='zjets':
			try: model.add_lognormal_uncertainty('xsec_zjets', math.log(1.06), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
			except: pass
		elif proc=='vv':
			try: model.add_lognormal_uncertainty('xsec_dibos', math.log(1.06), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
			except: pass
		elif proc=='qcd':
			try: model.add_lognormal_uncertainty('xsec_qcd', math.log(1.06), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
			except: pass
			
	return model

def get_model_statOnly():
	model = build_model_from_rootfile(input,include_mc_uncertainties=True)#,histogram_filter = (lambda s: s.count('jec')==0 and s.count('jer')==0)
	
	model.fill_histogram_zerobins()
	model.set_signal_processes('sig')
			
	return model

def get_model_2xSyst():
	model = build_model_from_rootfile(input,include_mc_uncertainties=False)#,histogram_filter = (lambda s: s.count('jec')==0 and s.count('jer')==0)
	
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
	try: model.add_lognormal_uncertainty('pileup', math.log(1.06), '*', '*')
	except: pass
	try: model.add_lognormal_uncertainty('jec', math.log(1.07), '*', '*')
	except: pass
	try: model.add_lognormal_uncertainty('jer', math.log(1.06), '*', '*')
	except: pass
	try: model.add_lognormal_uncertainty('btag', math.log(1.20), '*', '*')
	except: pass
	try: model.add_lognormal_uncertainty('ttag', math.log(1.20), '*', '*')
	except: pass
	try: model.add_lognormal_uncertainty('pdf', math.log(1.048), '*', '*')
	except: pass
	try: model.add_lognormal_uncertainty('muRF', math.log(1.20), '*', '*')
	except: pass
	for proc in procs:
		if proc=='tt':
			try: model.add_lognormal_uncertainty('xsec_ttbar', math.log(1.06), proc, '*') #B2G-17-017-V9: 20%
			except: pass
			try: model.add_lognormal_uncertainty('toppt', math.log(1.12), proc, '*')
			except: pass
		elif proc=='sitop':
			try: model.add_lognormal_uncertainty('xsec_sitop', math.log(1.12), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
			except: pass
		elif proc=='wjets':
			try: model.add_lognormal_uncertainty('xsec_wjets', math.log(1.06), proc, '*') #B2G-17-017-V9: 25%, scaled by lumi
			except: pass
		elif proc=='zjets':
			try: model.add_lognormal_uncertainty('xsec_zjets', math.log(1.12), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
			except: pass
		elif proc=='vv':
			try: model.add_lognormal_uncertainty('xsec_dibos', math.log(1.12), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
			except: pass
		elif proc=='qcd':
			try: model.add_lognormal_uncertainty('xsec_qcd', math.log(1.12), proc, '*') #B2G-17-017-V9: 50%, scaled by lumi
			except: pass
			
	return model
	
model = get_model()

##################################################################################################################

model_summary(model)

#plot_exp, plot_obs = bayesian_limits(model,'all', n_toy = 100000, n_data = 1000)
# plot_exp, plot_obs = bayesian_limits(model,'expected', n_toy = 5000, n_data = 500)
# plot_exp.write_txt('limits_'+rFileName+'_expected.txt')
#plot_obs.write_txt('limits_'+rFileName+'_observed.txt')

#N sigma discovery reaches (NOTE that this implementation currently works only with utils/theta-auto.py, check if this is OK or if it can be implemented in utils2 easily!!!)
getNSigmaCrossSecMin(model,5,0.001)
getNSigmaCrossSecMin(model,3,0.001)

#report.write_html('htmlout_'+rFileName)

