import os
import re
import subprocess
import info
import shutil

'''

'''
class JavaFile:
    def __init__(self, fileName):
        self.fileName = fileName


preConfiguredFile = r'C:\Users\Jordan\Documents\School\TA Tools\grading.settings'
injections = []
inputFiles = []
newConfig = False
if preConfiguredFile != '':
    with open(preConfiguredFile, 'r') as configuration:
        topLevel = configuration.readline()
        dependencies = configuration.readline()
        settingInjections = True
        for line in configuration:
            if line.strip() == 'Input:':
                settingInjections = False
                continue
            if settingInjections:
                injections.append(line)
            else:
                inputFiles.append(line)
else:
    topLevel = input('Enter the path of the directory that contains all of the section folders: ')
    dependencies = input('Enter the path to any additional class files each submission need to function: ')

    if 'y' in input('Do you have any files to inject into each submission? (y/n)'):
        inject = input('Enter the full path and name of an extra file you want to include with each submission: ')
        while inject != '':
            injections.append(inject)
            inject = input('Enter the full path and name of an extra file you want to include with each submission: ')

    if 'y' in input('Do you have any prewritten input files? (y/n)'):
        inputFilePath = input("Enter the full path of an input file: ")
        while inputFilePath != '':
            inputFiles.append(inputFilePath)
            inputFilePath = input("Enter the full path of an input file: ")

    newConfig = True

# Clean up data
topLevel = topLevel.strip().replace("\\", '/')
dependencies = dependencies.strip().replace("\\", '/')
for i in range(len(injections)):
    injections[i] = injections[i].strip().replace("\\", '/')
for i in range(len(inputFiles)):
    inputFiles[i] = inputFiles[i].strip().replace("\\", '/')

if(newConfig):
    with open('grading.settings', 'w') as configuration:
        print(topLevel, file=configuration)
        print(dependencies, file=configuration)

        for injection in injections:
            print(injection, file=configuration)

        print('Input:', file=configuration)
        for inputFile in inputFiles:
            print(inputFile, file=configuration)

print(topLevel)
print(dependencies)
print(injections)
print(inputFiles)

os.chdir(topLevel)
sections = os.listdir(topLevel)
for section in sections:
    if(section == 'None'):
        continue
    print(f'Section {section}')
    os.chdir(section)

    studentFolders = os.listdir()
    for dir in studentFolders:
        print(dir)
        if os.path.isdir(dir):
            os.chdir(dir)
        else:
            continue
        
        files = os.listdir('.')

        # remove .class files
        for fileName in files:
            if('.class' in fileName):
                files.remove(fileName)

        # Inject and compile injections
        for injection in injections:
            fileName = injection.split('/')[-1]
            print(fileName)
            shutil.copy(injection, f'{os.getcwd()}/{fileName}')
            subprocess.run(f'javac -cp {dependencies}:. {fileName}')

        # compile files
        for fileName in files:
            print(fileName)
            subprocess.run(f'javac -cp {dependencies};. {fileName}')

        # Run injections
        for injection in injections:
            fileName = injection.split('/')[-1]
            execName = fileName.split('.')[0]
            inputFile = inputFiles[0].split('/')[-1]
            shutil.copy(inputFiles[0], f'{inputFile}')

            stdin = open(inputFile, 'r')
            subprocess.run(f'java -cp {dependencies};. {execName}', stdin=stdin, text=True)
            stdin.close()

        quit()
        # run files
        for fileName in files:
            execName = fileName.split('.')[0]
            subprocess.run(f'java -cp {dependencies};. {execName}')

        os.chdir('..')
    os.chdir('..')
