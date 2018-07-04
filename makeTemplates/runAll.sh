for iPlot in NPV AK8NJets AK8Jet1Eta AK8Jet2Eta AK8Jet1Phi AK8Jet2Phi AK8Jet1Pt AK8Jet2Pt AK8Jet1M AK8Jet2M AK8Jet1SDM AK8Jet2SDM AK8Jet1SDMcorr AK8Jet2SDMcorr AK8Jet1Tau32 AK8Jet2Tau32 AK8Jet1Tau21 AK8Jet2Tau21 AK8Jet1MaxSubbDisc AK8Jet2MaxSubbDisc AK8Jet1Sub1bDisc AK8Jet1Sub2bDisc AK8Jet2Sub1bDisc AK8Jet2Sub2bDisc AK8Jet1Mult AK8Jet2Mult AK8Jet1CHF AK8Jet2CHF DRJ1J2 DEtaJ1J2 DPhiJ1J2 DYJ1J2 RSGPt RSGMass; do
    echo $iPlot
    #python modifyBinning.py $iPlot
    python plotTemplates.py $iPlot
done
