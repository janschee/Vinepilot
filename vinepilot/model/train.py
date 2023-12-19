import logging 

def train(dataloader, model, loss_fn, optimizer, num_epochs):
    model.train()
    for epoch in range(num_epochs):
        for batch, (img, segimg) in enumerate(dataloader):

            #Forward
            predictions: list = model(img)
            loss = loss_fn(predictions, segimg)

            #Backward
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            #Logging
            logging.debug(f"Epoch: {epoch:<3} Batch: {batch:<4} Loss: {loss.item():<20}")
            if batch % 10 == 0: logging.info(f"Epoch: {epoch:<3} Batch: {batch:<4} Loss: {loss.item():<20}")





        
