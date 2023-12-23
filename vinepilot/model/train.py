import logging
import os
import torch

from vinepilot.config import Project

def train(dataloader, model, loss_fn, optimizer, num_epochs):
    model_weights: str = os.path.normpath(os.path.join(Project.model_dir, "./best_model.pth"))
    logging.debug(f"Train: Model: {model}")
    #model.load_state_dict(torch.load(model_weights))
    model.train()
    min_loss: float = float("inf")
    for epoch in range(num_epochs):
        for batch, (img, seggray, segrgb) in enumerate(dataloader):

            #Forward
            predictions: list = model(img)
            loss = loss_fn(predictions, seggray)

            #Backward
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            #Save model
            if loss.item() < min_loss: 
                logging.debug(f"Train: Saved model!")
                min_loss = loss.item()
                torch.save(model.state_dict(), model_weights)

            #Logging
            logging.debug(f"Train: Epoch: {epoch:<3} Batch: {batch:<4} Loss: {loss.item():<20}")
            if batch % 10 == 0: logging.info(f"Train: Epoch: {epoch:<3} Batch: {batch:<4} Loss: {loss.item():<20}")




        
