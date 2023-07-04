# hi 4/7/2023
class MaskDataset(Dataset):
    """ Masked faces dataset
        0 = 'no mask'
        1 = 'mask'
    """
    def __init__(self, dataFrame):
        self.dataFrame = dataFrame
        
        self.transformations = Compose([
            ToPILImage(),
            Resize((100, 100)),
            ToTensor(), # [0, 1]
        ])
    
    def __getitem__(self, key):
        row = self.dataFrame.iloc[key]
        return {
            'image': self.transformations(row['image']),
            'mask': tensor([row['mask']], dtype=long),
        }
    
    def __len__(self):
        return len(self.dataFrame.index)