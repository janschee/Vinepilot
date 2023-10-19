from vinepilot.model.data import VinePilotDataloader, VinePilotDataset

dataloader = VinePilotDataloader(VinePilotDataset)
for batch, (image_tensor, label) in enumerate(dataloader()):
    print(batch, label)

