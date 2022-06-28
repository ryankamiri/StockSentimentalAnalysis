import json
import os
from datetime import datetime
import shutil

from sqlalchemy import true

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