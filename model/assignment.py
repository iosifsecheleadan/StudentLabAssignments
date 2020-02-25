import unittest

import random

class Assignment:
    def __init__(self, ID, deadline, description) -> None:
        self.__ID = int(ID)
        self.__deadline = str(deadline)
        self.__description = str(description)

    def __eq__(self, other) -> bool:
        return self.__ID == other.__ID

    def __str__(self) -> str:
        return "Assignment " + str(self.__description) + " with ID " + str(self.__ID) + " has deadline " + str(self.__deadline)


    def getID(self):
        return self.__ID

    def getDeadline(self):
        return self.__deadline

    def getDescription(self):
        return self.__description


    def setDeadline(self, deadline):
        self.__deadline = deadline

    def setDescription(self, description):
        self.__description = description


class testAssignmentModel(unittest.TestCase):
    def test(self):
        self.testGet()
        self.testSet()
        self.testStrEqu()

    def testGet(self):
        test = Assignment(13, '25.1.2112', 'any friggin description')
        self.assertEqual(test.getID(), 13)
        self.assertEqual(test.getDeadline(), '25.1.2112')
        self.assertEqual(test.getDescription(), 'any friggin description')

    def testSet(self):
        test = Assignment(13, '25.1.2112', 'any friggin description')
        self.assertEqual(test.getDeadline(), '25.1.2112')
        self.assertEqual(test.getDescription(), 'any friggin description')
        test.setDeadline('5.11.2021')
        test.setDescription('not quite ' + test.getDescription())
        self.assertEqual(test.getDeadline(), '5.11.2021')
        self.assertEqual(test.getDescription(), 'not quite any friggin description')

    def testStrEqu(self):
        list = []
        number = random.randint(1,9)
        while number > 0:
            date = str(random.randint(1,27)) + '.'
            month = str(random.randint(1,12)) + '.'
            year = str(random.randint(2019, 2025))
            list.append(Assignment(3, str(date+month+year), 'description'))
            number -= 1
        for test in list:
            for item in list:
                self.assertEqual(test, item)
            self.assertEqual(str(test), "Assignment description with ID 3 has deadline " + str(test.getDeadline()))



