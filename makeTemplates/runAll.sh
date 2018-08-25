for iPlot in lepPt lepEta lepPhi lepRelIso lepAbsIso metPt leadJetPt subLeadJetPt tlepLeadAK4Pt NJetsSel minDR_lepJet ptRel_lepJet deltaR_ljets0 deltaR_ljets1 WlepPt WlepMass thadPt thadMass thadChi2 tlepPt tlepMass tlepChi2 topAK8Pt topAK8Mass topAK8Tau32 topAK8SDMass Ntoptagged zpDeltaR zpDeltaY zpPt zpMass genzpMass; do
    echo $iPlot
    #python modifyBinning.py $iPlot
    python plotTemplates.py $iPlot
done
