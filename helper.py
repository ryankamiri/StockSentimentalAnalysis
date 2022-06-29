import json
import os
from datetime import datetime
import shutil
import matplotlib.pyplot as plt
import numpy as np

def writeData(filename, data):
    #Create data dir
    dataPath = "data"
    if not os.path.exists(dataPath):
        os.makedirs(dataPath)

    #Create archive dir
    archivePath = "archive"
    if not os.path.exists(archivePath):
        os.makedirs(archivePath)
    
    #Move file to archive
    currentFile = findFilename(filename, dataPath)
    shutil.move(os.path.join(dataPath, findFilename(filename, dataPath)), os.path.join(archivePath, currentFile))

    with open(f'{dataPath}/{filename}{datetime.now().strftime("_%I-%M%p_%m-%d-%y")}.json', "w+", encoding="utf-8") as _file:
        _file.write(json.dumps(data, indent=4))

def findFilename(keyword, path=None):
    for filename in os.listdir(path):
        if keyword in filename:
            return filename

def articleExists(data, article):
    for a in data:
        if a["link"] == article["link"]:
            return True
    return False

# Plot validation and training curves separately

def plot_loss_curves(history):
  """
  Returns separate curves for training and validation
  """
  loss = history.history["loss"]
  val_loss = history.history["val_loss"]
  
  accuracy = history.history["accuracy"]
  val_accuracy = history.history["val_accuracy"]

  epochs = range(len(history.history["loss"]))

  # plot loss
  plt.plot(epochs, loss, label="training_loss")
  plt.plot(epochs, val_loss, label="val_loss")
  plt.title("loss")
  plt.xlabel("epochs")
  plt.legend()

  # plot accuracy
  plt.figure()
  plt.plot(epochs, accuracy, label="accuracy")
  plt.plot(epochs, val_accuracy, label="val_accuracy")
  plt.title("accuracy")
  plt.xlabel("epochs")
  plt.legend()
  plt.show()