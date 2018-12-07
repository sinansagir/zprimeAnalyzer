import os,sys,datetime,itertools

thisDir = os.getcwd()
outputDir = thisDir+'/'

region='SR' #PS,SR,TTCR,WJCR
categorize=0 #1==categorize into t/W/b/j, 0==only split into flavor

cTime=datetime.datetime.now()
date='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
time='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
if region=='TTCR': pfix='ttbar'
elif region=='WJCR': pfix='wjets'
else: pfix='templates'
if not categorize: pfix='kinematics_'+region
pfix+='_'+date#+'_'+time

iPlotList = [#distribution name as defined in "doHists.py"
# 			'lepPt',
# 			'lepEta',
# 			'lepPhi',
# 			'lepRelIso',
# 			'lepAbsIso',
# 			'metPt',
# 			'leadJetPt',
# 			'leadJetEta',
# 			'leadJetPhi',
# 			'subLeadJetPt',
# 			'subLeadJetEta',
# 			'subLeadJetPhi',
# 			'tlepLeadAK4Pt',
# 			'NJetsSel',
# 			'minDR_lepJet',
# 			'ptRel_lepJet',
# 			'WlepPt',
# 			'WlepMass',
# 			'thadPt',
# 			'thadMass',
# 			'thadChi2',
# 			'tlepPt',
# 			'tlepMass',
# 			'tlepChi2',
# 			'topAK8Pt',
# 			'topAK8Eta',
# 			'topAK8Phi',
# 			'topAK8Mass',
# 			'topAK8Tau32',
# 			'topAK8SDMass',
# 			'Ntoptagged',
# 			'zpDeltaR',
# 			'zpDeltaY',
# 			'zpPt',
			'zpMass',
			'genzpMass',
			'genTTorJJMass'
			]

isEMlist = ['E','M']
nttaglist = ['0','1']
nWtaglist = ['0p']
nbtaglist = ['0p']#,'0','1','2']
njetslist = ['0p']
if not categorize: 	
	nttaglist = ['0p']
	nWtaglist = ['0p']
	nbtaglist = ['0p']
catList = list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist,njetslist))

outDir = outputDir+pfix
if not os.path.exists(outDir): os.system('mkdir '+outDir)
os.system('cp ../analyze.py doHists.py ../weights.py ../samples.py doCondorTemplates.py doCondorTemplates.sh '+outDir+'/')
os.chdir(outDir)

count=0
for iplot in iPlotList:
	for cat in catList:
		catDir = cat[0]+'_nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]+'_nJ'+cat[4]
		catDir = catDir.replace('_nT0p','').replace('_nW0p','').replace('_nB0p','').replace('_nJ0p','')
		print "iPlot: "+iplot+", cat: "+catDir
		if not os.path.exists(outDir+'/'+catDir): os.system('mkdir '+catDir)
		os.chdir(catDir)
		os.system('cp '+outputDir+'/doCondorTemplates.sh '+outDir+'/'+catDir+'/'+cat[0]+'T'+cat[1]+'W'+cat[2]+'B'+cat[3]+'J'+cat[4]+iplot+'.sh')			
	
		dict={'dir':outputDir,'iPlot':iplot,'region':region,'isCategorized':categorize,
			  'isEM':cat[0],'nttag':cat[1],'nWtag':cat[2],'nbtag':cat[3],'njets':cat[4],
			  'exeDir':outDir+'/'+catDir}
	
		jdf=open('condor.job','w')
		jdf.write(
"""universe = vanilla
Executable = %(exeDir)s/%(isEM)sT%(nttag)sW%(nWtag)sB%(nbtag)sJ%(njets)s%(iPlot)s.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
request_memory = 3072
Output = condor_%(iPlot)s.out
Error = condor_%(iPlot)s.err
Log = condor_%(iPlot)s.log
Notification = Error
Arguments = %(dir)s %(iPlot)s %(region)s %(isCategorized)s %(isEM)s %(nttag)s %(nWtag)s %(nbtag)s %(njets)s
Queue 1"""%dict)
		jdf.close()

		os.system('condor_submit condor.job')
		os.chdir('..')
		count+=1

print "Total jobs submitted:", count
                  
