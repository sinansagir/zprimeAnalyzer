#!/usr/bin/python

import os,sys,fnmatch

thisDir = os.getcwd()
templateDir = thisDir+'/../makeTemplates/templates_zpMass_mergeprocs_2018_8_29'
templateDirAH = thisDir+'/templates_alljets_2018_9_11'
thetaConfigTemp = thisDir+'/theta_config_comb_template.py'
doLimits = True #else, it will run 3 and 5 sigma reaches
do2xSyst = False
doStatOnly = False

toFilter0 = []
toFilter0 = ['__'+item+'__' for item in toFilter0]

limitConfs = {#'<limit type>':[filter list]
			  #'all':[],
			  #'isE':['isM'], #only electron channel
			  #'isM':['isE'], #only muon channel
			  'btagcats':['M__','E__','E_nB','M_nB','nT0__','nT1__'],
			  'nobtagcats':['M__','E__','_nB'],
			  }

limitType = '_comb_cls'
if do2xSyst: limitType += '_2xSyst'
if doStatOnly: limitType += '_statOnly'
limordisc = {0:'_disc',1:'_lim'}
outputDir = '/user_data/ssagir/Zprime_limits_2018/'+templateDir.split('/')[-1]+limitType+limordisc[doLimits]+'/' #prevent writing these (they are large) to brux6 common area
if not os.path.exists(outputDir): os.system('mkdir '+outputDir)
print outputDir

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)
            
rootfilelist = []
i=0
for rootfile in findfiles(templateDir, '*.root'):
    if 'rebinned_stat1p1' not in rootfile: continue
    #if '3000p0fb' not in rootfile: continue
    if 'plots' in rootfile: continue
    if 'YLD' in rootfile: continue
    rootfilelist.append(rootfile)
    i+=1

f = open(thetaConfigTemp, 'rU')
thetaConfigLines = f.readlines()
f.close()

thetaVersion = {0:'utils',1:'utils2'}
def makeThetaConfig(rFile,outDir,toFilter):
	with open(outDir+'/'+rFile.split('/')[-1].replace('.root','.py'),'w') as fout:
		for line in thetaConfigLines:
			if line.startswith('inputSL ='): fout.write('inputSL = \''+rFile+'\'\n')
			elif line.startswith('inputAH ='): fout.write('inputAH = \''+rFile.replace(templateDir,templateDirAH).replace('_rebinned_stat1p1','')+'\'\n')
			elif line.startswith('	model = build_model_from_rootfile(inputSL'): 
				if len(toFilter)!=0:
					statUnc = 'False'
					if doStatOnly: statUnc = 'True'
					model='	model = build_model_from_rootfile(inputSL,include_mc_uncertainties='+statUnc+',histogram_filter = (lambda s:  s.count(\''+toFilter[0]+'\')==0'
					for item in toFilter: 
						if item!=toFilter[0]: model+=' and s.count(\''+item+'\')==0'
					model+='))'
					fout.write(model)
				else: fout.write(line)
			elif line.startswith('model = get_model_ljets'):
				if do2xSyst: fout.write('model = get_model_ljets_2xSyst()\n')
				elif doStatOnly: fout.write('model = get_model_ljets_statOnly()\n')
				else: fout.write(line)
			elif line.startswith('alljetsModel = get_model_alljets'):
				if do2xSyst: fout.write('alljetsModel = get_model_alljets_2xSyst()\n')
				elif doStatOnly: fout.write('alljetsModel = get_model_alljets_statOnly()\n')
				else: fout.write(line)
			elif line.startswith('doLimits = '):
				if doLimits: fout.write('doLimits = True\n')
				else: fout.write('doLimits = False\n')
			else: fout.write(line)
	with open(outDir+'/'+rFile.split('/')[-1].replace('.root','.sh'),'w') as fout:
		fout.write('#!/bin/sh \n')
		fout.write('cd /home/ssagir/CMSSW_7_3_0/src/\n')
		fout.write('source /cvmfs/cms.cern.ch/cmsset_default.sh\n')
		fout.write('cmsenv\n')
		fout.write('cd '+outDir+'\n')
		fout.write('/home/ssagir/CMSSW_7_3_0/src/theta/'+thetaVersion[doLimits]+'/theta-auto.py ' + outDir+'/'+rFile.split('/')[-1].replace('.root','.py'))

count=0
for limitConf in limitConfs:
	toFilter = toFilter0 + limitConfs[limitConf]
	print limitConf,'=',toFilter
	for file in rootfilelist:
		fileName = file.split('/')[-1]
		signal = fileName.split('_')[2]
		outDir = outputDir+limitConf+'/'
		print signal
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
		os.chdir(outDir)
		fileDir = ''
		if templateDir.split('/')[-1]!=file.split('/')[-2]:
			fileDir = file.split('/')[-2]
			if not os.path.exists(outDir+fileDir): os.system('mkdir '+fileDir)
			os.chdir(fileDir)
		outDir=outDir+fileDir
		makeThetaConfig(file,outDir,toFilter)

		dict={'configdir':outDir,'configfile':file.split('/')[-1].replace('.root','')}

		jdf=open(file.split('/')[-1].replace('.root','.job'),'w')
		jdf.write(
"""universe = vanilla
Executable = %(configfile)s.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Notification = Error
request_memory = 3072
Output = %(configfile)s.out
Error = %(configfile)s.err
Log = %(configfile)s.log

Queue 1"""%dict)
		jdf.close()

		os.system('chmod +x '+file.split('/')[-1].replace('.root','.sh'))
		os.system('condor_submit '+file.split('/')[-1].replace('.root','.job'))
		os.chdir('..')
		count+=1
print "Total number of jobs submitted:", count
                  
