import os
import re
import subprocess

pattern = re.compile(r'(\w+)_(?:\w*?_)?\d+_\d+_([\w\d-]+.java)')
canvasRenamePattern = re.compile(r'(\w+)-\d.java')
inFile = r'C:\Users\Jordan\Desktop\ITSC 1212 Grading\input.txt'
inStacked = r'C:\Users\Jordan\Desktop\ITSC 1212 Grading\inputStacked.txt'

os.chdir('C:/Users/Jordan/Desktop/ITSC 1212 Grading/Take Home Test 3/submissions')

directory = os.getcwd()
files = os.listdir(directory)

for fileName in files:
    print(fileName)
    matches = re.match(pattern, fileName)
    if(matches):
        studentName = matches.group(1)
        programName = matches.group(2)
        programRenamed = re.match(canvasRenamePattern, programName)
        if(programRenamed):
            programName = programRenamed.group(1) + '.java'
        
        if(not(os.path.exists(studentName))):
            os.mkdir(studentName)

        os.rename(f'{directory}\{fileName}', f'{directory}/{studentName}/{programName}')
        os.chdir(f'{studentName}')
        subprocess.run('javac '+ programName)

        os.startfile(f'{directory}\{studentName}\{programName}')
        
        response = 'y'
        while(response not in ['n', 'N', 'no', 'No']):
            print(programName)
            if(response in ['s', 'stack', 'S', 'Stack']):
                subprocess.run(['java', programName[0: -5]], stdin = open(inStacked, 'r'))
            elif response in ['y', 'Y', 'yes', 'Yes']:
                subprocess.run(['java', programName[0: -5]])
            else:
                subprocess.run(['java', programName[0: -5]], stdin = open(inFile, 'r'))
            response = input("Would you like to run the program again: ")

        os.chdir(f'..')
