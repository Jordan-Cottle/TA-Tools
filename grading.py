import os
import re
import subprocess
import shutil

'''

'''
class JavaFile:
    executablePattern = re.compile(r'public\s+static\s+void\s+main\s*\(\s*String\s*\[\s*\]\s*\w+\s*\)\s*{')
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
        if dependencies == None:
            subprocess.run(f'javac {self.fileName}')
        
        elif dependencies != None:
            subprocess.run(f'javac -cp {dependencies};. {self.fileName}')
    
    def run(self, dependencies=None, inputSource=None):
        if (dependencies == None and inputSource == None):
            subprocess.run(f'java {self.execName}')

        elif dependencies == None and inputSource != None:
            with open(inputSource, 'r') as stdin:
                subprocess.run(f'java {self.execName}', stdin=stdin, text=True)

        elif dependencies != None and inputSource == None:
            subprocess.run(f'java -cp {dependencies};. {self.execName}')

        elif dependencies != None and inputSource != None:
            with open(inputSource, 'r') as stdin:
                subprocess.run(f'java -cp {dependencies};. {self.execName}', stdin=stdin, text=True)



preConfiguredFile = r'C:\Users\jorda\Documents\School\TA-Tools\grading.settings'
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

if dependencies == '':
    dependencies = None

os.chdir(topLevel)
sections = os.listdir(topLevel)
for section in sections:
    if(section == 'None'):
        continue
    print(f'Section {section}')
    os.chdir(section)

    studentFolders = os.listdir()
    for dir in studentFolders:
        if os.path.isdir(dir):
            print(dir)
            os.chdir(dir)
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

            print(javaFile.fileName)
            repeat = 'y'
            while 'y' in repeat:
                if len(inputFiles) > 0:
                    if len(inputFiles) == 1:
                        inputFile = inputFiles[0]
                    else:
                        for i, inputFile in enumerate(inputFiles):
                            print(i, inputFile, sep=': ')
                        
                        inputFileIndex = input("Enter the index of the input file you would like to use: ")
                        inputFile = inputFiles[int(inputFileIndex)]
                    
                    javaFile.run(dependencies=dependencies, inputSource=inputFile)
                else:
                    javaFile.run(dependencies=dependencies)
                
                repeat = input("Would you like to run this program again? (y/n): ")

        os.chdir('..')
    os.chdir('..')
