
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
        
#        clean_workdir()
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
    model = build_model_from_rootfile(input,include_mc_uncertainties=True)#,histogram_filter = (lambda s: s.count('jec')==0 and s.count('jer')==0)

    model.fill_histogram_zerobins()
    model.set_signal_processes('sig')
    
    procs = model.processes
    obsvs = model.observables.keys()

#     for obs in obsvs:
# 		if 'isE' in obs:
# 			model.add_lognormal_uncertainty('elIdSys', math.log(1.02), '*', obs)
# 			model.add_lognormal_uncertainty('elIsoSys', math.log(1.01), '*', obs)
# 		elif 'isM' in obs:
# 			model.add_lognormal_uncertainty('muIdSys', math.log(1.03), '*', obs)
# 			model.add_lognormal_uncertainty('muIsoSys', math.log(1.01), '*', obs)
    model.add_lognormal_uncertainty('lumi', math.log(1.025), '*', '*')
    model.add_lognormal_uncertainty('xsec', math.log(1.08), 'tt', '*')
    model.add_lognormal_uncertainty('xsec', math.log(1.08), 'qcd', '*')
    			
    return model

model = get_model()

##################################################################################################################

model_summary(model)

#plot_exp, plot_obs = bayesian_limits(model,'all', n_toy = 100000, n_data = 1000)
plot_exp, plot_obs = bayesian_limits(model,'expected')#, n_toy = 5000, n_data = 500)
plot_exp.write_txt('limits_'+rFileName+'_expected.txt')
#plot_obs.write_txt('limits_'+rFileName+'_observed.txt')

#N sigma discovery reaches (NOTE that this implementation currently works only with utils/theta-auto.py, check if this is OK or if it can be implemented in utils2 easily!!!)
getNSigmaCrossSecMin(model,5,0.01)
getNSigmaCrossSecMin(model,3,0.01)

report.write_html('htmlout_'+rFileName)

