class MaskDetectorTrainer(pl.LightningModule):
    """ MaskDetectorTrainer PyTorch Lightning class
    """
    def __init__(self, maskDFPath: Path=None):
        super(MaskDetectorTrainer, self).__init__()
        self.maskDFPath = maskDFPath
        
        self.trainAcc = Accuracy()
        self.valAcc = Accuracy()
        
        self.convLayer1 = convLayer1 = Sequential(
            Conv2d(3, 32, kernel_size=(3, 3), padding=(1, 1)),
            ReLU(),
            MaxPool2d(kernel_size=(2, 2))
        )
        
        self.convLayer2 = convLayer2 = Sequential(
            Conv2d(32, 64, kernel_size=(3, 3), padding=(1, 1)),
            ReLU(),
            MaxPool2d(kernel_size=(2, 2))
        )
        
        self.convLayer3 = convLayer3 = Sequential(
            Conv2d(64, 128, kernel_size=(3, 3), padding=(1, 1), stride=(3,3)),
            ReLU(),
            MaxPool2d(kernel_size=(2, 2))
        )
        
        self.linearLayers = linearLayers = Sequential(
            Linear(in_features=2048, out_features=1024),
            ReLU(),
            Linear(in_features=1024, out_features=2),
        )
        
        # Initialize layers' weights
        for sequential in [convLayer1, convLayer2, convLayer3, linearLayers]:
            for layer in sequential.children():
                if isinstance(layer, (Linear, Conv2d)):
                    init.xavier_uniform_(layer.weight)
    
    def forward(self, x: Tensor):
        """ forward pass
        """
        out = self.convLayer1(x)
        out = self.convLayer2(out)
        out = self.convLayer3(out)
        out = out.view(-1, 2048)
        out = self.linearLayers(out)
        return out