import os
import shutil
import re
import info

pattern = re.compile(r'(\w+)_(?:\w*?_)?\d+_\d+_([\w\d-]+.java)')
canvasRenamePattern = re.compile(r'(\w+)-\d.java')

workingDirectory = info.workingDirectory

if(not(os.path.exists(workingDirectory))):
            os.mkdir(workingDirectory)

os.chdir(workingDirectory)

directory = info.submissionDirectory
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

        shutil.copy(f'{directory}/{fileName}',
                  f'{workingDirectory}/{studentName}/{programName}')
