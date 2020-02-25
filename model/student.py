import unittest

import random

class Student:
    def __init__(self, ID, group, name) -> None:
        self.__ID = int(ID)
        self.__group = int(group)
        self.__name = str(name)

    def __eq__(self, other) -> bool:
        return self.__ID == other.__ID

    def __str__(self) -> str:
        return "Student " + str(self.__name) + " with ID " + str(self.__ID) +  " in group " + str(self.__group)


    def getID(self):
        return self.__ID

    def getGroup(self):
        return self.__group

    def getName(self):
        return self.__name


    def setGroup (self, group):
        self.__group = group

    def setName(self, name):
        self.__name = name

class testStudentModule(unittest.TestCase):
    def test(self):
        self.testGet()
        self.testSet()
        self.testStrEqu()

    def testGet(self):
        test = Student(2621, 917, 'sechelea')
        self.assertEqual(test.getID(), 2621)
        self.assertEqual(test.getGroup(), 917)
        self.assertEqual(test.getName(), 'sechelea')

    def testSet(self):
        test = Student(2621, 917, 'sechelea')
        self.assertEqual(test.getGroup(), 917)
        self.assertEqual(test.getName(), 'sechelea')
        test.setGroup(45)
        test.setName('iosif')
        self.assertEqual(test.getGroup(), 45)
        self.assertEqual(test.getName(), 'iosif')

    def testStrEqu(self):
        list = []
        number = random.randint(1,9)
        while number > 0:
            group = random.randint(100,999)
            list.append(Student(317, group, 'idiot'))
        for test in list:
            for item in list:
                self.assertEqual(test, item)
            self.assertEqual(str(test), "Student idiot with ID 317 in group " + str(test.getGroup()))



