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
			'NPV',
			'AK8NJets',
			'AK8Jet1Eta',
			'AK8Jet2Eta',
			'AK8Jet1Phi',
			'AK8Jet2Phi',
			'AK8Jet1Pt',
			'AK8Jet2Pt',
			'AK8Jet1M',
			'AK8Jet2M',
			'AK8Jet1SDM',
			'AK8Jet2SDM',
			'AK8Jet1SDMcorr',
			'AK8Jet2SDMcorr',
			'AK8Jet1Tau32',
			'AK8Jet2Tau32',
			'AK8Jet1Tau21',
			'AK8Jet2Tau21',
			'AK8Jet1MaxSubbDisc',
			'AK8Jet2MaxSubbDisc',
			'AK8Jet1Sub1bDisc',
			'AK8Jet1Sub2bDisc',
			'AK8Jet2Sub1bDisc',
			'AK8Jet2Sub2bDisc',
			'AK8Jet1Mult',
			'AK8Jet2Mult',
			'AK8Jet1CHF',
			'AK8Jet2CHF',
			'DRJ1J2',
			'DEtaJ1J2',
			'DPhiJ1J2',
			'DYJ1J2',
			'RSGPt',
			'RSGMass'
			]

isEMlist = ['LT','GT']
nttaglist = ['0p']
nWtaglist = ['0p']
nbtaglist = ['0p','0','1','2']
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
                  
