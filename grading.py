import os
import re
import subprocess
import info

''' info.py requirements

    info.workingDirectory
        - A path to a directory where student folders are located.
        - The script will find all subdirectories directly inside of this path
        - All java files contained within each subdirectory will be executed
'''

inputFiles = info.inputFiles

inFile = inputFiles[0]
inStacked = inputFiles[1]

directory = info.outputDirectory
os.chdir(directory)

sections = os.listdir(directory)
for section in sections:
    if(section == 'others'):
        continue
    print(f'Section {section}')
    os.chdir(section)

    studentFolders = os.listdir()
    students = []
    for dir in studentFolders:
        print(dir)
        os.chdir(dir)
        files = os.listdir('.')

        # remove .class files
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
    os.chdir('..')
