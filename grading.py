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



'''
        os.chdir(f'{studentName}')

        subprocess.run('javac ' + programName)

        os.startfile(f'{directory}\{studentName}\{programName}')

        response = 'y'
        while(response not in ['n', 'N', 'no', 'No']):
            print(programName)

            if(response in ['s', 'stack', 'S', 'Stack']):
                subprocess.run(['java',
                               programName[0: -5]],
                               stdin=open(inStacked, 'r'))

            elif response in ['y', 'Y', 'yes', 'Yes']:
                subprocess.run(['java',
                               programName[0: -5]])

            else:
                subprocess.run(['java',
                               programName[0: -5]],
                               stdin=open(inFile, 'r'))

            response = input("Would you like to run the program again: ")

        os.chdir(f'..')
'''
