import os
import re
import subprocess
import shutil

'''
This script will look in a given directory for a set of section folders that each contain a set of student folders.
The script will compile and execute all of the java source code files it finds inside of each of the student folders.

When the script starts you will be asked if you have a configuration file.
If it is the first time you have run the script, you do not have a valid configuration file, answer no.
If you have successfully run the script before, you should have a configuration file with the settings you chose the first time.
It should be called grading.settings and found in the top level directory you entered for the previous run.

There are a number of different settings for the script. Each setting is in the form of a path to either a dirrectory or file on your system.
Other than the top level setting, you can input an empty line to indicate that you are either done giving values, or would like to skip the setting.
When prompted for a setting you wish to skip, simply press enter to continue.

The first, and only required setting is the top level directory.
The path for the top level directory should point to the directory that holds all of the section folders you wish to grade

The dependencies setting allows you to specify a folder to include in the class path when compiling and running the java programs.
The path should point to a directory that contains any extra java files the submissions will need.
You can use this setting to include things like an external library used by the students for an assignment.
**Note: This has not been tested with more sophisticated packaging like a .jar file.
This is only guaranteed to work with a directory containing java source code files.**

The injections setting allows you to specify specific files to copy into each of the student's submissions.
These injected files can static classes the students were given to work with as part of the assignment and their submissions will have access to them.
They can also be driver or test files that use files the students have submitted.
They will behave exactly as if they were included in the student's submitted project.
You can specific as many of these injection files as you would like. Just remember they get copied and compiled for each student.

The input files setting allows you to specify specific files to use as an input source for the programs.
You can specify any number of files you want to use. If you specify more than one, you will be prompted before each run of a program which you would like to use.
These files will replace and keyboard input normally taken by the program.
Any time a program would use a Scanner to read from System.in, it will read from one of these input files instead.
If no input files are specified, the default System.in will be used.

When the program are run, the student's name will be output at the top, followed by the program name.
When a program completes, the script will ask you if you want to run the program again.
If you have given the script more than one input file to use, you will be prompted to pick one to use before each run of a program.
'''


class JavaFile:
    executablePattern = re.compile(r'public\s+static\s+void\s+main')

    def __init__(self, fileName):
        self.fileName = fileName
        self.execName = fileName.split('.')[0]

        with open(self.fileName, 'r') as sourceFile:
            contents = sourceFile.read()
            match = re.search(JavaFile.executablePattern, contents)
            if(match):
                self.executable = True
            else:
                self.executable = False

    def compile(self, dependencies=None):
        if dependencies is None:
            subprocess.run(f'javac {self.fileName}')

        elif dependencies is not None:
            subprocess.run(f'javac -cp "{";".join(dependencies)};." {self.fileName}')

    def run(self, dependencies=None, inputSource=None):
        if (dependencies is None and inputSource is None):
            subprocess.run(f'java {self.execName}')

        elif dependencies is None and inputSource is not None:
            with open(inputSource, 'r') as stdin:
                subprocess.run(f'java {self.execName}', stdin=stdin, text=True)

        elif dependencies is not None and inputSource is None:
            subprocess.run(f'java -cp "{";".join(dependencies)};." {self.execName}')

        elif dependencies is not None and inputSource is not None:
            with open(inputSource, 'r') as stdin:
                subprocess.run(f'java -cp "{";".join(dependencies)};." {self.execName}', stdin=stdin, text=True)


def checkPath(path, isDir=False):
    if not os.path.exists(path):
        print(f'{path} does not exist!')
        return False

    if isDir and not os.path.isdir(path):
        print(f'{path} is not a directory!')
        return False
    elif not isDir and not os.path.isfile(path):
        print(f'{path} is not a file!')
        return False

    return True


def getValidPaths(prompt, paths=None, getDir=False):
    if paths is None:
        paths = []

    path = input(prompt).strip()
    if(path != ''):
        if not checkPath(path, getDir):
            print('Please try again!')
            return getValidPaths(prompt, paths, getDir)

    while path != '':
        paths.append(path)
        path = input(prompt)
        if(path != ''):
            if not checkPath(path, getDir):
                print('Please try again!')
                return getValidPaths(prompt, paths, getDir)

    return paths


dependencies = []
injections = []
inputFiles = []
newConfig = False
if 'y' in input("Do you have a valid configuration file? (y/n): "):
    preConfiguredFile = input("Enter the path and name of the configuration file: ")
    with open(preConfiguredFile, 'r') as configuration:
        reading = 'top'
        for line in configuration:
            line = line.strip()

            # Change state when prompt line is found
            if line.startswith('Input:'):
                reading = 'input'
                continue
            elif line.startswith('Depend:'):
                reading = 'dependencies'
                continue
            elif line.startswith('Inject:'):
                reading = 'injections'
                continue
            elif line.startswith('#'):
                # Skip comments
                continue

            # Assign line to proper list based on current reading state
            if reading == 'injections':
                injections.append(line)
            elif reading == 'input':
                inputFiles.append(line)
            elif reading == 'dependencies':
                dependencies.append(line)
            elif reading == 'top':
                topLevel = line
            else:
                print(f'Invalid state for configuration reading: {reading}')
else:
    topLevel = input('Enter the path of the directory that contains all of the section folders you want to grade: ')
    while not os.path.exists(topLevel) or not os.path.isdir(topLevel):
        print(f'{topLevel} is not a valid path to a directory!')
        topLevel = input('Enter the path of the directory that contains all of the section folders you want to grade: ')

    if 'y' in input('Do the submissions require any external files (dependencies) to function properly? (y/n): '):
        dependencies = getValidPaths('Enter the path to a directory that contains the external class files each submission needs to function: ', getDir=True)

    if 'y' in input('Do you have any files to inject into each submission? (y/n): '):
        injections = getValidPaths('Enter the path to an extra file you want to include with each submission: ')

    if 'y' in input('Do you have any prewritten input files? (y/n): '):
        inputFilePath = getValidPaths("Enter the path to an input file: ")

    newConfig = True


# Clean up data
def cleanPath(path):
    return path.strip().replace('\\', '/')

topLevel = topLevel.strip().replace("\\", '/')
dependencies = [cleanPath(dependency) for dependency in dependencies]
injections = [cleanPath(injection) for injection in injections]
inputFiles = [cleanPath(inputFile) for inputFile in inputFiles]

if(newConfig):
    with open(f'{topLevel}/grading.settings', 'w') as configuration:
        print(topLevel, file=configuration)

        print("Depend:", file=configuration)
        for dependency in dependencies:
            print(dependency, file=configuration)

        print("Inject:", file=configuration)
        for injection in injections:
            print(injection, file=configuration)

        print('Input:', file=configuration)
        for inputFile in inputFiles:
            print(inputFile, file=configuration)

if not dependencies:
    dependencies = None

os.chdir(topLevel)
sections = os.listdir(topLevel)
for section in sections:
    # Skip the None folder and any files in the directory
    if(section == 'None' or not os.path.isdir(section)):
        continue
    print(f'Section {section}')
    os.chdir(section)

    studentFolders = os.listdir()
    for studentName in studentFolders:
        if os.path.isdir(studentName):
            os.chdir(studentName)
        else:
            continue

        # Copy injections into current directory
        for injection in injections:
            fileName = injection.split('/')[-1]
            shutil.copy(injection, f'{os.getcwd()}/{fileName}')

        files = os.listdir('.')

        javaFiles = []
        for fileName in files:
            extension = fileName.split('.')[-1]
            if extension == 'class':
                continue
            elif extension == 'java':
                javaFile = JavaFile(fileName)
                javaFile.compile(dependencies)
                javaFiles.append(javaFile)

        # Execute the programs
        for javaFile in javaFiles:
            if not javaFile.executable:
                continue

            print('+'*8, studentName, '+'*8, sep='|')
            repeat = 'y'
            while 'y' in repeat:
                print('~'*3, javaFile.fileName, '~'*3, sep='')
                javaFile.compile(dependencies)
                if len(inputFiles) > 0:
                    if len(inputFiles) == 1:
                        inputFile = inputFiles[0]
                    else:
                        for i, inputFile in enumerate(inputFiles):
                            print(i+1, inputFile, sep=': ')

                        inputFileIndex = input("Enter the index of the input file you would like to use: ")
                        inputFile = inputFiles[int(inputFileIndex)-1]

                    javaFile.run(dependencies=dependencies, inputSource=inputFile)
                else:
                    javaFile.run(dependencies=dependencies)

                repeat = input("Would you like to run this program again? (y/n): ")

        os.chdir('..')
    os.chdir('..')
