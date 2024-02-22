import logging
import os
import torch
from vinepilot.config import Project


def train(dataloader, model, loss_fn, optimizer, num_epochs):
    logging.info(f"Train: Model Architecture: {model}")
    model.load_state_dict(torch.load(Project.model_weights))
    model.train()
    min_loss: float = float("inf")
    for epoch in range(num_epochs):
        for batch, (img, segimg, seggray, segrgb, segmulti) in enumerate(dataloader):

            #Forward
            predictions: list = model(img.to(torch.float))
            loss = loss_fn(predictions, segmulti.to(torch.float))

            #Backward
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            #Logging
            logging.debug(f"Train: Epoch: {epoch:<3} Batch: {batch:<4} Loss: {loss.item():<20}")
            if batch % 10 == 0: logging.info(f"Train: Epoch: {epoch:<3} Batch: {batch:<4} Loss: {loss.item():<20}")

            #Save model
            if loss.item() < min_loss: 
                logging.debug(f"Train: Saved model!")
                min_loss = loss.item()
                torch.save(model.state_dict(), Project.model_weights)







        
