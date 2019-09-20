from random import choice
from openpyxl import Workbook, load_workbook

# TODO: Check for same teams in past
# TODO: Read names and past teams from spreadsheet

''' 
This script requires a students.xlsx file to be created with all of the student's names and genders

The first column should include each student's first name
The second column should include each student's last name
The last column should include each students gender, marked with M for male or F for female

The first row of the spreadsheet can include a header or be blank.
The script begins reading from the second row.
'''
class Student:
    def __init__(self, firstName, lastName, gender):
        self.firstName = firstName
        self.lastName = lastName
        self.gender = gender
    
    def __str__(self):
        return f'{self.firstName} {self.lastName}'
    

class Team:
    def __init__(self, *students):
        self.members = list(students)
    
    def addMember(self, student):
        self.members.append(student)

    def __str__(self):
        return ' & '.join((str(member) for member in self.members))
    

def makeTeams(students):
    teams = []
    while len(students) > 1:
        a = choice(students)
        students.remove(a)
        b = choice(students)
        students.remove(b)

        teams.append(Team(a, b))

    return teams


studentWorkbook = load_workbook('students.xlsx', read_only=True)
studentWorksheet = studentWorkbook.active

males = []
females = []
# skip header on row 1
for i in range(2, studentWorksheet.max_row + 1):
    firstName = studentWorksheet[f'A{i}'].value
    lastName = studentWorksheet[f'B{i}'].value
    gender = studentWorksheet[f'C{i}'].value

    student = Student(firstName, lastName, gender)

    if student.gender.lower() == 'm':
        males.append(student)
    else:
        females.append(student)

maleTeams = makeTeams(males)
femaleTeams = makeTeams(females)

malesRemaining = len(males)
femalesRemaining = len(females)
remaining = malesRemaining + femalesRemaining

# handle extra students
if remaining == 1:  # odd number in class

    # Add extra male/female into existing male/female team (a single team of 3)
    if malesRemaining == 1:
        print('Creating male team of 3')
        choice(maleTeams).addMember(males[0])
    elif femalesRemaining == 1:
        print('Creating female team of 3')
        print(females[0])
        choice(femaleTeams).addMember(females[0])

elif remaining == 2:  # odd number of both males and females
    print('Creating mixed team')
    femaleTeams.append(Team(males[0], females[0]))

teams = maleTeams + femaleTeams

workbook = Workbook()

sheet = workbook.active

col = 'A'
row = 1
for team in teams:

    # set names into cell
    sheet[f'{col}{row}'].value = str(team)

    row += 1

workbook.save('teams.xlsx')
