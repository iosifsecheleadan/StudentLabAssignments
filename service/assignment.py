from error.custom import ServiceError

from model.assignment import Assignment

import random

class ServiceAssignment:
    def __init__(self, repoAssig, validAssig) -> None:
        self.__repository = repoAssig
        self.__validator = validAssig
        self.__preDescription = ["Basics", "Fundamental", "Beginners", "Minimalistic", "Inferior", "Simple",
                                 "Advanced", "Complex", "Superior", "Serious", "Supreme", "Sophisticated",
                                 "Structural", "Computational"]
        self.__Description = ["Programming", "Computers", "Algorithmics", "Data Bases", "Circuits",
                              "Geometry", "Algebra", "Mathematics", "Analysis", "Calculus", "Vectors"]

    def getRepository(self):
        return self.__repository

    def getValidator(self):
        return self.__validator

    def append(self, assignment):
        self.__repository.appendToList(assignment)

    def remove(self, assignment):
        self.__repository.removeFromList(assignment)

    def removeAll(self):
        self.__repository.erase()

    def update(self, assignment, newAssignment):
        if assignment.getID() == newAssignment.getID():
            self.__repository.replace(assignment, newAssignment)
        else : raise ServiceError("ID" + str(assignment.getID()) + " doesn't match ID " + str(newAssignment.getID()))

    def verify(self, assignment):
        if self.__repository.verifyID(assignment.getID()) == True:
            raise ServiceError("assignment with ID " + str(assignment.getID()) + " already exists")

    def check(self, assignment):
        if self.__repository.verifyID(assignment.getID()) == False:
            raise ServiceError("assignment with ID " + str(assignment.getID()) + " doesn't exist")

    def getRandomDate(self):
        year = random.randint(2017, 2020)
        month = random.randint(1, 12)
        if month == 2 and year % 4 == 0:
            day = random.randint(1, 29)
        elif month == 2:
            day = random.randint(1, 28)
        elif month in [4, 6, 9, 11]:
            day = random.randint(1, 30)
        else:
            day = random.randint(1, 31)
        return str(day) + "." + str(month) + "." + str(year)

    def getRandomAssignment(self):
        #ID = random.randint(10000,99999)
        ID = random.randint(47030,47040)
        date = self.getRandomDate()
        description = str(random.choice(self.__preDescription) + " " + random.choice(self.__Description))
        return Assignment(ID, date, description)

    def addRandomAssignment(self, number):
        while number>0:
            assignment = self.getRandomAssignment()
            try:
                self.verify(assignment)
                self.__repository.appendToList(assignment)
                number -= 1
            except ServiceError:
                pass


