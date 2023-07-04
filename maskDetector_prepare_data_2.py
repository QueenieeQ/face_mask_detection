maskNum = maskDF[maskDF['mask']==1].shape[0]
nonMaskNum = maskDF[maskDF['mask']==0].shape[0]
nSamples = [nonMaskNum, maskNum]
normedWeights = [1 - (x / sum(nSamples)) for x in nSamples]
self.crossEntropyLoss = CrossEntropyLoss(weight=torch.tensor(normedWeights))