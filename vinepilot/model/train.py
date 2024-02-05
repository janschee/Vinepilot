import logging
import os
import torch

from vinepilot.config import Project

#TODO: This seems a little out of place here. Find better solution!
frame_img = os.path.join(Project.vineyards_dir, "./vineyard_000/frame_000.png")
target_img = os.path.join(Project.vineyards_dir, "./vineyard_000/target_000.png")
pred_img = os.path.join(Project.vineyards_dir, "./vineyard_000/pred_000.png")
pred_rgb_img = os.path.join(Project.vineyards_dir, "./vineyard_000/pred_rgb_000.png")


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







        
