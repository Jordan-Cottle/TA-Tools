from info import studentList

section003 = []
section009 = []
for student in sorted(list(studentList)):
    section = int(input(f"Which section is {student} in?"))
    if section == 3:
        section003.append(student)
    elif section == 9:
        section009.append(student)
    else:
        print(f'{student} is not your student')

print(f'Section 003: {section003}', f'Section 009: {section009}', sep='\n')
