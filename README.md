# VinePilot: Semantic Segmentation for Autonomous Driving in Vineyards

## Project Goal
The project aims to generate datasets and train machine learning models to facilitate vision-based autonomous driving in vineyards.

## Approach
A self-supervised learning approach is employed to train the model. The image below illustrates the general concept.
![Overview](overview.jpeg)

## Project Structure
- **Config:** Contains configurations and paths for the project.
- **Data:** Includes the source vineyard video (not uploaded) and predictions.
- **Model:** Encompasses model training and inference, loss calculation, and optimizer settings.
- **Tools:** AutoSeg, a tool designed for automatic annotation.
- **Utils:** Houses useful functions for image manipulation.

## Dataset
- The dataset currently consists of a 10-minute video, walking through a vineyard.
- The dataset is automatically annotated using manual feature engineering.
- The annotations have a high degree of noise and uncertainty.

> **_NOTE:_** This repository is not intended for reproduction and thus does not include the dataset or setup instructions.

## Model
Architecture: UNet: https://arxiv.org/abs/1505.04597