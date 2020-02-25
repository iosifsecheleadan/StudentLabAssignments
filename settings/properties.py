from repository.list import List

import time

from model.student import Student
from model.assignment import Assignment
from model.grade import Grade

from validator.student import ValidatorStudent
from validator.assignment import ValidatorAssignment
from validator.grade import ValidatorGrade

class Properties:
    def __init__(self) -> None:
        self.__directory = "/home/sechelea/Documents/programming/projects/python/assignement5-9.StudentLabAssignments/settings/properties.txt"
        self.__type = self.__getType()
        self.__repos = {'inMemory' : [self.__getInMemory, self.__setInMemory],
                        'textFile': [self.__getTextFile, self.__setTextFile],
                        'binaryFile' : [self.__getBinaryFile, self.__setBinaryFile]}

    def __getType(self):
        f = open(self.__directory, "r")
        firstLine = f.readline()
        f.close()
        return firstLine.split('"')[1]


    def getSettings(self):
        if self.__type in self.__repos:
            return self.__repos[self.__type][0]()
        raise ValueError('check the properties text file in "settings>properties"')

    def __getInMemory(self):
        return {'students' : [], 'assignments' : [], 'grades' : []}

    def __getTextFile(self):
        f = open(self.__directory, "r")
        f.readline()
        students = self.__getStudentsTextFile(f.readline())
        assignments = self.__getAssignmentsTextFile(f.readline())
        grades = self.__getGradesTextFile(f.readline(), students, assignments)
        f.close()
        return {'students': students.getList(), 'assignments': assignments.getList(), 'grades': grades.getList()}

    def __getStudentsTextFile(self, line):
        line = line.split('"')
        valid = ValidatorStudent()
        index = 1
        students = List()
        while index < len(line):
            student = line[index].split(', ')
            if len(student)==3:
                student = Student (student[0], student[1], student[2])
                valid.validate(student)
                print(str(student) + ' read', end=' ')
                if students.verifyID(student.getID()) == True:
                    print('\nstudent with ID ' + str(student.getID()) + ' already exists')
                else:
                    students.appendToList(student)
                    print('and added')
            elif len(student)==0: print("student not valid")
            index += 2
            self.buffer()
        print(str(int(len(line)/2)) + " students recovered")
        return students

    def __getAssignmentsTextFile(self, line):
        valid = ValidatorAssignment()
        index = 1
        assignments = List()
        line = line.split('"')
        while index < len(line):
            assignment = line[index].split(', ')
            if len(assignment)==3:
                assignment = Assignment(assignment[0], assignment[1], assignment[2])
                valid.validate(assignment)
                print(str(assignment) + ' read', end=' ')
                if assignments.verifyID(assignment.getID()) == True:
                    print('\nassignment with ID ' + str(assignment.getID()) + ' already exists')
                else:
                    assignments.appendToList(assignment)
                    print('and added')
            elif len(assignment)==0: print("assignment not valid")
            index += 2
            self.buffer()
        print(str(int(len(line)/2)) + " assignments recovered")
        return assignments

    def __getGradesTextFile(self, line, studList, assigList):
        line = line.split('"')
        valid = ValidatorGrade()
        index = 1
        grades = List()
        while index < len(line):
            grade = line[index].split(', ')
            if len(grade)==3:
                grade = Grade(grade[0], grade[1], grade[2])
                valid.validate(grade, studList, assigList)
                print(str(grade) + ' read', end=' ')
                if studList.verifyID(grade.getStudentID()) == False:
                    print('\nstudent with ID ' + str(grade.getStudentID()) + ' does not exist')
                elif assigList.verifyID(grade.getAssignmentID()) == False:
                    print('\nassignment with ID ' + str(grade.getAssignmentID()) + ' does not exist')
                elif grades.verifyID(grade.getID()) == True:
                    print('\ngrade with ID ' + str(grade.getID()) + ' already exists')
                else:
                    grades.appendToList(grade)
                    print('and added')
            elif len(grade)==0: print("grade not valid")
            index += 2
            self.buffer()
        print(str(int(len(line)/2)) + " grades recovered")
        return grades

    def __getBinaryFile(self):
        pass


    def setSettings(self, settings):
        if self.__type in self.__repos:
            self.__repos[self.__type][1](settings)
        else: raise ValueError('check the properties text file in "settings>properties"')

    def __setInMemory(self, nothing):
        print('Using "inMemory" settings you cannot save your progress. Everything used in one session is only valid for that one session.')

    def __setTextFile(self, settings):
        f = open(self.__directory, "w")
        f.write('repository = "textFile" \nstudents = ')
        f.close()

        f = open(self.__directory, "a")
        for item in settings['students']:
            f.write('"' + str(item.getID()) + ', ' + str(item.getGroup()) + ', ' + str(item.getName()) + '", ')
        f.write('\nassignments = ')
        for item in settings['assignments']:
            f.write('"' + str(item.getID()) + ', ' + str(item.getDeadline()) + ', ' + str(item.getDescription()) + '", ')
        f.write('\ngrades = ')
        for item in settings['grades']:
            f.write('"' + str(item.getStudentID()) + ', ' + str(item.getAssignmentID()) + ', ' + str(item.getGrade()) + '", ')
        f.write('''

# DO NOT MODIFY THE LINES OR THEIR ORDER IN ANY WAY
# repository can be "inMemory"/"textFile"/"binaryFile"
# students have "ID, group, name", etc
# assignments have "ID, deadline, description", etc
# grades have "studentID, assignmentID, grade", etc''')
        f.close()

    def __setBinaryFile(self):
        pass

    def buffer(self):
        time.sleep(0.25)





