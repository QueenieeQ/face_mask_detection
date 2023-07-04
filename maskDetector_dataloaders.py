def train_dataloader(self) -> DataLoader:
    return DataLoader(self.trainDF, batch_size=32, shuffle=True, num_workers=4)

def val_dataloader(self) -> DataLoader:
    return DataLoader(self.validateDF, batch_size=32, num_workers=4)