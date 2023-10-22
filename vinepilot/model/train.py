
def train(dataloader, model, loss_fn, optimizer):
    size: int = len(dataloader.dataset)
    model.train()
    for batch, (image_tensor, label, valid) in enumerate(dataloader):
        if not valid: continue

        #Forward
        predictions: list = model(image_tensor)
        loss = loss_fn(predictions, label)

        #Backward
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        if batch % 10 == 0: print(f"Batch: {batch}, Loss: {loss.item()}")





        
