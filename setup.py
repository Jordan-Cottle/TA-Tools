import os
import shutil
import re
import info

''' info.py requirements

    info.workingDirectory
        - A string representing a path to a directory to place script output.
        - Student folders will be created inside of this directory, with their programs located inside

    info.submissionDirectory
        - A string representing a path to the directory where the student submissions are located
        - Simply unzip the bulk download from canvas and use the extracted folder's path for this variable
'''

pattern = re.compile(r'(\w+)_(?:\w*?_)?\d+_\d+_([\w\d-]+.java)')
canvasRenamePattern = re.compile(r'(\w+)-\d+.java')

outputDirectory = info.outputDirectory

if(not(os.path.exists(outputDirectory))):
            os.mkdir(outputDirectory)

os.chdir(outputDirectory)

directory = info.submissionDirectory
files = os.listdir(directory)
myStudents = set()
notMyStudents = set()

studentDict = info.studentList
for section in studentDict:
    for student in studentDict[section]:
        myStudents.add(student)

for fileName in files:
    print(fileName)
    matches = re.match(pattern, fileName)
    if(matches):
        studentName = matches.group(1)
        programName = matches.group(2)
        programRenamed = re.match(canvasRenamePattern, programName)
        if(programRenamed):
            programName = programRenamed.group(1) + '.java'

        if studentName not in myStudents:
            outputFolder = 'others'
        else:
            if studentName in studentDict['003']:
                outputFolder = '003'
            else:
                outputFolder = '009'

        destination = f'{outputDirectory}/{outputFolder}/{studentName}'
        if(not(os.path.exists(destination))):
            os.makedirs(destination)

        shutil.copy(f'{directory}/{fileName}',
                    f'{destination}/{fileName}')
