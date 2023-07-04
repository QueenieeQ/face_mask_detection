def prepare_data(self) -> None:
    """ Prepare train/test datasets and calculate weight vector
        for CrossEntropyLoss
    """
    self.maskDF = maskDF = pd.read_csv(self.maskDFPath)
    train, validate = train_test_split(maskDF, test_size=0.3, random_state=0,
                                       stratify=maskDF['mask'])
    self.trainDF = MaskDataset(train)
    self.validateDF = MaskDataset(validate)