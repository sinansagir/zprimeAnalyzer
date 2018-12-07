for iPlot in lepPt lepEta lepPhi lepRelIso lepAbsIso metPt leadJetPt leadJetEta leadJetPhi subLeadJetPt subLeadJetEta subLeadJetPhi tlepLeadAK4Pt NJetsSel minDR_lepJet ptRel_lepJet WlepPt WlepMass thadPt thadMass thadChi2 tlepPt tlepMass tlepChi2 topAK8Pt topAK8Eta topAK8Phi topAK8Mass topAK8Tau32 topAK8SDMass Ntoptagged zpDeltaR zpDeltaY zpPt zpMass genzpMass genTTorJJMass; do
#for iPlot in zpMass genzpMass genTTorJJMass; do
    echo $iPlot
    #python modifyBinning.py $iPlot
    python plotTemplates.py $iPlot
done
