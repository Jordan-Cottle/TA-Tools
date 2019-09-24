import os
import shutil
import re
import info

import openpyxl

''' info.py requirements

    info.workingDirectory
        - A string representing a path to a directory to place script output.
        - Student folders will be created inside of this directory, with their programs located inside

    info.submissionDirectory
        - A string representing a path to the directory where the student submissions are located
        - Simply unzip the bulk download from canvas and use the extracted folder's path for this variable

    info.outputDirectory
        - A string representing a path to the directory where organized submissions should be placed
        - This can be any valid path on your computer
'''


class Student:
    sections = {
        '001': {},
        '002': {},
        '003': {},
        '007': {},
        '008': {},
        '009': {},

        # Use to hold students until section is found
        None: {}
    }

    def __new__(cls, name, section=None):
        ''' Check to make sure student doesn't exist before creating a new Student '''
        if name in Student.sections[section]:
            return Student.sections[section][name]
        else:
            student = super(Student, cls).__new__(cls)
            return student

    def __init__(self, name, section=None):
        if name in Student.sections[section]:
            # Do not initialize
            return
        
        print(f'Creating {name}')
        
        self.name = name
        self.section = section
        self.submissions = []

        Student.sections[self.section][self.name] = self
    
    def addSubmission(self, submission):
        self.submissions.append(submission)

    def setSection(self, section):
        del Student.sections[self.section][self.name]

        self.section = section

        Student.sections[self.section][self.name] = self

    def __eq__(self, value):
        if type(value) != type(self):
            raise NotImplementedError(f"Cannot compare {type(self)} with {type(value)}!")
        return self.name == value.name and self.section == value.section

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f'{self.name}'
    
    def __repr__(self):
        return f'{self.name}: {self.section}'


class StudentSubmission:
    '''Represents a file submitted by a student

    Contains a number of methods to help with renaming, compiling, and executing
    '''

    canvasPattern = re.compile(r'(\w+)_(?:\w*?_)?\d+_\d+_([\w\d-]+.java)')
    duplicateNamePattern = re.compile(r'(\w+)-\d+.java')

    def __new__(cls, fileName, parentDirectory=None):
        matches = re.match(StudentSubmission.canvasPattern, fileName)
        if(matches):
            return object.__new__(cls)
        else:
            print(f"{fileName} not recognized by the pattern matcher!")
            return None

    def __init__(self, fileName, parentDirectory=None):
        matches = re.match(StudentSubmission.canvasPattern, fileName)
        if(matches):
            self.student = Student(matches.group(1))
            self.programName = matches.group(2)
            duplicateName = re.match(StudentSubmission.duplicateNamePattern, self.programName)
            if(duplicateName):
                self.programName = duplicateName.group(1) + '.java'
            
            self.execName = self.programName.split('.')[0]
        else:
            raise ValueError(f"{fileName} not recognized by the pattern matcher!")

        if parentDirectory is None:
            self.parentDirectory = os.getcwd()
        else:
            self.parentDirectory = parentDirectory
        
        self.fileName = fileName
    
    def rename(self, newName):
        ''' Renames the file associated with this submission '''
        shutil.copy(f'{self.parentDirectory}/{self.fileName}',
                    f'{self.parentDirectory}/{newName}')
        
        self.fileName = newName
    
    def move(self, newDirectory):
        ''' Moves the file associated with this submission to a new directory'''
        shutil.copy(f'{self.parentDirectory}/{self.fileName}',
                    f'{newDirectory}/{self.fileName}')

        self.parentDirectory = newDirectory

    def __repr__(self):
        return f'StudentSubmission("{self.fileName}")'

    def __str__(self):
        return f'{self.fileName}'

outputDirectory = info.outputDirectory

if(not(os.path.exists(outputDirectory))):
            os.mkdir(outputDirectory)

os.chdir(outputDirectory)

directory = info.submissionDirectory
files = os.listdir(directory)

# Create StudentSubmissions
studentFiles = (StudentSubmission(file) for file in files)

submissions = []
for submission in studentFiles:
    if submission is None:
        continue
    print(submission.student, submission, sep=': ')
    submissions.append(submission)


# Organize students by section
for section in Student.sections:
    if section is None:
        continue
    numStudents = int(input(f'Enter the number of students in section {section}: '))
    count = 0
    print(section)
    for name, student in list(Student.sections[None].items()):
        inSection = 'y' in input(f'Is {name} in section {section}?')
        if inSection:
            student.setSection(section)
            count += 1
        
        if count == numStudents:
            break

for section in Student.sections:
    print(Student.sections[section])
quit()



for fileName in files:
    print(fileName)
    matches = re.match(canvasPattern, fileName)
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

        
