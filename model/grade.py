import unittest

import random

class Grade:
    def __init__(self, studentID, assignmentID, grade) -> None:
        self.__ID = (int(studentID), int(assignmentID))
        if grade == "not assigned": self.__grade = str(grade)
        else: self.__grade = int(grade)
        self.__studentID = int(studentID)
        self.__assignmentID = int(assignmentID)


    def __eq__(self, other) -> bool:
        return self.__ID == other.__ID

    def __str__(self) -> str:
        return "Student " + str(self.__studentID) + " in assignment " + str(self.__assignmentID) + " has grade " + str(self.__grade)


    def getID(self):
        return self.__ID

    def getGrade(self):
        return self.__grade

    def getStudentID(self):
        return self.__studentID

    def getAssignmentID(self):
        return self.__assignmentID


    def setGrade(self, grade):
        self.__grade = grade

class testGradeModel(unittest.TestCase):
    def test(self):
        self.testGet()
        self.testSet()
        self.testStrEqu()

    def testGet(self):
        test = Grade(13, 47, 9)
        self.assertEqual(test.getStudentID(), 13)
        self.assertEqual(test.getAssignmentID(), 47)
        self.assertEqual(test.getID(), (13, 47))
        self.assertEqual(test.getGrade(), 9)

    def testSet(self):
        test = Grade(13, 47, 9)
        self.assertEqual(test.getGrade(), 9)
        test.setGrade('not assigned')
        self.assertEqual(test.getGrade(), 'not assigned')

    def testStrEqu(self):
        list = []
        number = random.randint(1,9)
        while number > 0:
            grade = random.randint(1,10)
            list.append(Grade(13, 7, grade))
            number -= 0
        for test in list:
            for item in list:
                self.assertEqual(test, item)
            self.assertEqual(str(test), "Student 13 in assignment 7 has grade " + str(test.getGrade()))



