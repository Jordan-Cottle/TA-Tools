import os
import shutil
import re

import openpyxl

'''
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

    students = {}

    def __new__(cls, name, section=None):
        ''' Check to make sure student doesn't exist before creating a new Student '''
        if name in Student.students:
            print(f'{name} found')
            return Student.students[name]
        else:
            print(f'{name} not found, creating new student!')
            student = super(Student, cls).__new__(cls)
            return student

    def __init__(self, name, section=None):
        if name in Student.students:
            # Do not initialize
            return

        print(f'Initializing {name}')

        self.name = name
        self.section = section
        self.submissions = []

        Student.sections[self.section][self.name] = self
        Student.students[self.name] = self

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
        os.rename(f'{self.parentDirectory}/{self.fileName}',
                  f'{self.parentDirectory}/{newName}')

        self.fileName = newName

    def move(self, newDirectory):
        ''' Copies the file associated with this submission to a new directory'''
        shutil.copy(f'{self.parentDirectory}/{self.fileName}',
                    f'{newDirectory}/{self.fileName}')

        self.parentDirectory = newDirectory

    def __repr__(self):
        return f'StudentSubmission("{self.fileName}")'

    def __str__(self):
        return f'{self.fileName}'

workingDirectory = input("Enter the path to the directory that contains the submissions folder: ")
outputDirectory = f'{workingDirectory}/organizedSubmissions'
submissionDirectory = f'{workingDirectory}/submissions'

if(not(os.path.exists(outputDirectory))):
            os.mkdir(outputDirectory)

os.chdir(workingDirectory)

files = os.listdir(submissionDirectory)

# Create StudentSubmissions
studentFiles = (StudentSubmission(file, submissionDirectory) for file in files)

submissions = []
for submission in studentFiles:
    if submission is None:
        continue
    submissions.append(submission)

# Read in students from files
for section in Student.sections:
    fileName = f'{workingDirectory}/{section}.section'
    if os.path.exists(fileName) and os.path.isfile(fileName):
        with open(fileName, 'r') as sectionFile:
            for name in sectionFile:
                if len(name) < 3:
                    print(f'{name} too short!')
                    continue
                student = Student(name.strip())
                student.setSection(section)

# Organize students by section by hand
for section in Student.sections:
    print(len(Student.sections[None]))
    if len(Student.sections[None]) == 0:
        break

    if section is None:
        for name in list(Student.sections[None]):
            s = input(f'Enter the section that {name} is in: ')
            student = Student(name)
            student.setSection(s)
        continue

    sectionList = Student.sections[section]

    print(f"Currently listed in section {section}")
    for name in sectionList:
        print(name)

    name = ''
    while not name.startswith('-'):
        name = input(
            f"Enter the start of last name for a student in section {section} to search for or '-' to stop: "
            ).lower()

        if name.startswith('-'):
            continue

        hits = []
        for studentName in Student.sections[None]:
            if studentName.startswith(name):
                hits.append(studentName)

        if not hits:
            print("No submission found!")
            continue

        for hit in hits:
            inSection = 'y' in input(f'Is {hit} in section {section}?')
            if inSection:
                student = Student(hit)
                student.setSection(section)

    print(f"Currently listed in section {section}")
    for name in sectionList:
        print(name)

# Write or read text file for each section containing student's names
for section in Student.sections:
    fileName = f'{outputDirectory}/{section}.section'
    with open(fileName, 'w') as sectionFile:
        for student in Student.sections[section]:
            print(student, file=sectionFile)

for submission in submissions:
    section = submission.student.section
    name = submission.student.name
    destination = f'{outputDirectory}/{section}/{name}'

    if(not(os.path.exists(destination))):
            os.makedirs(destination)

    submission.move(destination)
    submission.rename(submission.programName)
