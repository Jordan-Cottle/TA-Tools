import info
from random import choice
from openpyxl import Workbook

''' info.py requirements
    info.studentList
    - A dictionary containing all student's names
    - The structure of the dictionary is important
        * There are only two top level keys, "Male" and "Female"
        * The values associated with each key is a list containing each student's name
        * Each student's name is a list or tuple with two elements. Index 0 is thei first name, index 1 is their last name
    - place all Male students in the list located under the "Male" key
    - place all Female students in the list located under the "Female" key

    Example:

    studentList = {
        "Male": [
            ("Joe", "Smith"),
            ("John", "Doe")
        ],

        "Female": [
            ("Jane", "Doe"),
            ("Sarha", "Ward")
        ]
    }
'''


def makeTeams(students):
    teams = []
    while len(students) > 1:
        a = choice(students)
        students.remove(a)
        b = choice(students)
        students.remove(b)

        teams.append((a, b))

    return teams


def addToTeam(teams, student):
    oldTeam = choice(teams)
    newTeam = (*oldTeam, student)

    teams.remove(oldTeam)
    teams.append(newTeam)


students = info.studentList

males = students['Male']
females = students['Female']

maleTeams = makeTeams(males)
femaleTeams = makeTeams(females)

malesRemaining = len(males)
femalesRemaining = len(females)
remaining = malesRemaining + femalesRemaining

# handle extra students
if remaining == 1:  # odd number in class

    # Add extra male/female into existing male/female team (a single team of 3)
    if malesRemaining == 1:
        print("Creating male team of 3")
        addToTeam(maleTeams, males[0])
    elif femalesRemaining == 1:
        print('Creating female team of 3')
        addToTeam(femaleTeams, females[0])

elif remaining == 2:  # odd number of both males and females
    print('Creating mixed team')
    femaleTeams.append((males[0], females[0]))

teams = maleTeams + femaleTeams


workbook = Workbook()

sheet = workbook.active

col = 'A'
row = 1
for team in teams:
    # pull names out of tuple structure
    firstNameA = team[0][0]
    lastNameA = team[0][1]

    firstNameB = team[1][0]
    lastNameB = team[1][1]

    # combine names together
    teamNames = f'{firstNameA} {lastNameA} & {firstNameB} {lastNameB}'

    # set names into cell
    sheet[f'{col}{row}'].value = teamNames

    row += 1
    print(teamNames)

workbook.save('teams.xlsx')
