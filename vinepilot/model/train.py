import logging 

def train(dataloader, model, loss_fn, optimizer, num_epochs):
    size: int = len(dataloader.dataset)
    model.train()
    for epoch in range(num_epochs):
        for batch, (image_tensor, label, valid) in enumerate(dataloader):
            if not valid: continue

            #Forward
            predictions: list = model(image_tensor)
            loss = loss_fn(predictions, label)

            #Backward
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            if batch % 10 == 0: logging.info(f"Epoch: {epoch:<3} Batch: {batch:<4} Loss: {loss.item():<20}")





        
