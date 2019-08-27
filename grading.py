import os
import re
import subprocess
import info

inputFiles = info.inputFiles

inFile = inputFiles[0]
inStacked = inputFiles[1]

directory = info.workingDirectory
os.chdir(directory)
studentFolders = os.listdir(directory)

for dir in studentFolders:
    print(dir)
    os.chdir(dir)

    files = os.listdir('.')

    #remove .class files
    for fileName in files:
        if('.class' in fileName):
            files.remove(fileName)

    # compile files
    for fileName in files:
        print(fileName)
        subprocess.run(f'javac {fileName}')
    
    # run files
    for fileName in files:
        execName = fileName.split('.')[0]
        subprocess.run(f'java {execName}')
    
    os.chdir('..')
