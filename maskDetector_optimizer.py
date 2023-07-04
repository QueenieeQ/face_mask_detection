
def configure_optimizers(self) -> Optimizer:
    return Adam(self.parameters(), lr=0.00001)