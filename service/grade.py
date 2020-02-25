from error.custom import ServiceError

from model.grade import Grade

from repository.list import List

import random
import datetime

class ServiceGrade:
    def __init__(self, repoGrade, repoStud, repoAssig, validGrade) -> None:
        self.__repositoryGrade = repoGrade
        self.__repositoryStudent = repoStud
        self.__repositoryAssignment = repoAssig
        self.__validator = validGrade

    def getRepository(self):
        return self.__repositoryGrade

    def getRepositoryStudent(self):
        return self.__repositoryStudent

    def getRepositoryAssignment(self):
        return self.__repositoryAssignment

    def getValidator(self):
        return self.__validator

    def append(self, grade):
        self.__repositoryGrade.appendToList(grade)

    def remove(self, grade):
        self.__repositoryGrade.removeFromList(grade)

    def removeAll(self):
        self.__repositoryGrade.erase()

    def removeStudentByID(self, ID):
        self.__repositoryGrade.removeStudentByID(ID)

    def removeAssignmentByID(self, ID):
        self.__repositoryAssignment.removeStudentByID(ID)

    def update(self, grade, newGrade):
        if grade.getID() == newGrade.getID():
            self.__repositoryGrade.replace(grade, newGrade)
        else : raise ServiceError("ID" + str(grade.getID()) + " doesn't match ID " + str(newGrade.getID()))

    def verifyGrade(self, grade):
        if self.__repositoryStudent.verifyID(grade.getStudentID()) == False:
            raise ServiceError("student with ID " + str(grade.getStudentID()) + " doesn't exist")
        if self.__repositoryAssignment.verifyID(grade.getAssignmentID()) == False:
            raise ServiceError("assignment with ID " + str(grade.getAssignmentID()) + " doesn't exit")
        if self.__repositoryGrade.verifyID(grade.getID()) == True:
            raise ServiceError("grade with student ID " + str(grade.getStudentID()) + " and assignment ID " + str(grade.getAssignmentID()) + " already exists")

    def checkGrade(self, grade):
        if self.__repositoryGrade.verifyID(grade.getID()) == False:
            raise ServiceError("grade with student ID " + str(grade.getStudentID()) + " and assignment ID " + str(grade.getAssignmentID()) + " doesn't exist")

    def checkGradeBool(self, grade):
        return self.__repositoryGrade.verifyID(grade.getID())

    def assign(self, group, assignmentID):
        for student in self.__repositoryStudent.getList():
            if student.getGroup() == group:
                grade = Grade(student.getID(), assignmentID, "not assigned")
                if self.checkGradeBool(grade)==False:
                    self.__repositoryGrade.appendToList(grade)
                    print(str(grade) + " added")

    # STATISTICS

    def studentsWithAssignment(self, assignment):
        assignmentID = assignment.getID()
        studentList = List()
        for grade in self.__repositoryGrade.getList():
            if grade.getAssignmentID() == assignmentID:
                student = self.__repositoryStudent.itemWithID(grade.getStudentID())
                studentList.appendToList(student)
        return studentList

    def lateStudents(self):
        studentList = List()
        now = datetime.datetime.now()
        for grade in self.__repositoryGrade.getList():
            if grade.getGrade() == 'not assigned':
                date = self.__repositoryAssignment.itemWithID(grade.getAssignmentID()).getDeadline()
                actualDate = str(now.day) + '.' + str(now.month) + '.' + str(now.year)
                if self.isDateSmaller(date, actualDate) == True:
                    student = self.__repositoryStudent.itemWithID(grade.getStudentID())
                    if student not in studentList.getList():
                        studentList.appendToList(student)
        return studentList

    def bestStudents(self):
        studentList = List()
        for grade in self.__repositoryGrade.getList():
            if grade.getGrade() != 'not assigned':
                studentID = grade.getStudentID()
                student = self.__repositoryStudent.itemWithID(studentID)
                if student not in studentList.getList():
                    studentList.appendToList(student)
        return studentList

    def assignmentsWithGrades(self):
        assignmentList = List()
        for grade in self.__repositoryGrade.getList():
            if grade.getGrade() != 'not assigned':
                assignmentID = grade.getAssignmentID()
                assignment = self.__repositoryAssignment.itemWithID(assignmentID)
                if assignment not in assignmentList.getList():
                    assignmentList.appendToList(assignment)
        return  assignmentList

    # RANDOM FUNCTIONS

    def getRandomGrade(self):
        studentNumber = random.randint(0,len(self.__repositoryStudent.getList())-1)
        studentID = self.__repositoryStudent.getItemOnPosition(studentNumber).getID()

        assignmentNumber = random.randint(0,len(self.__repositoryAssignment.getList())-1)
        assignmentID = self.__repositoryAssignment.getItemOnPosition(assignmentNumber).getID()

        grade = random.randint(1,14)
        if grade > 10: grade = "not assigned"
        return Grade(studentID,assignmentID,grade)

    def addRandomGrade(self, number):
        maxGrades = len(self.__repositoryAssignment.getList())*len(self.__repositoryStudent.getList())
        if number > maxGrades:
            print("Can only add " + str(maxGrades) + " grades. It will take long, possibly forever, to add that many grades.")
            number = maxGrades/2
            print("Adding " + str(number) + " grades")

        while number>0:
            grade = self.getRandomGrade()
            try:
                self.verifyGrade(grade)
                self.__repositoryGrade.appendToList(grade)
                number -= 1
            except ServiceError:
                pass


    def isDateSmaller(self, date1, date2):
        date1 = date1.split('.')
        date2 = date2.split('.')
        if date1[2]<date2[2]:
            return True
        elif date1[2]==date2[2] and date1[1]<date2[1]:
            return True
        elif date1[2]==date2[2] and date1[1]==date2[1] and date1[0]<date2[0]:
            return True
        else: return False

    def getAverageStudentGrade(self, student):
        studentID = student.getID()
        average = 0
        number = 0
        for grade in self.__repositoryGrade.getList():
            if grade.getStudentID() == studentID and grade.getGrade()!='not assigned':
                average += grade.getGrade()
                number += 1
        if number == 0 : return 0
        return float(average/number)

    def getAverageAssignmentGrade(self, assignment):
        assignmentID = assignment.getID()
        average = 0
        number = 0
        for grade in self.__repositoryGrade.getList():
            if grade.getAssignmentID() == assignment and grade.getGrade()!='not assigned':
                average += grade.getGrade()
                number += 1
        if number == 0 : return 0
        return float(average/number)


