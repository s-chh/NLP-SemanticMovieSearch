import os
from pathlib import Path

def getAllFilesInFolder(folder):
    parDir = Path(__file__).parent.parent
    os.chdir(parDir)
    files = []
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            files.append(file)
            #files.append(file.lower())
    return files