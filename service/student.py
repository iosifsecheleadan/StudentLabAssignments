from error.custom import ServiceError
from model.student import Student

import unittest

import random

class ServiceStudent:
    def __init__(self, repoStud, validStud) -> None:
        self.__repository = repoStud
        self.__validator = validStud
        self.__randomFirstName = ['Alexia', 'Emily', 'Linnaea', 'Ovidiu', 'Philander',
                                 'Nicole', 'Royal', 'Tammara', 'Iob', 'Kori',
                                 'Marion', 'Raphael', 'David', 'Irene', 'Petronel',
                                 'Joandra', 'Mathilda', 'Farran', 'Githa', 'Sheridan',
                                 'Katee', 'Moira', 'Caleigh', 'Shaye', 'Lucian',
                                 'Haylee', 'Stevie', 'Mehitabel', 'Ross', 'Ellisson',
                                 'Fay', 'Moss', 'Norm', 'Ridley', 'Clarke',
                                 'Derick', 'Wenda', 'Kassia', 'Nannie', 'Alyssia',
                                 'Rey', 'Adriana', 'Jeri', 'Graham', 'Greer',
                                 'Galen', 'Tina', 'Maeleth', 'Brenden', 'Linton', 'Allahu']
        self.__randomSecondName = ['Nelson', 'Lewin', 'Derrick', 'Senior', 'Leonard',
                                  'Hancock', 'Cojocaru', 'Crewe', 'Low', 'Bean',
                                  'Stacey', 'David', 'Raphael', 'Goodwin', 'Nielson',
                                  'Simpkin', 'Spears', 'Harlow', 'Thurstan', 'Toller',
                                  'Sommer', 'Steele', 'Polley', 'Vincent', 'Perkins',
                                  'Sanford', 'Reeves', 'Sydney', 'Ellisson', 'Ross',
                                  'Moss', 'Fay', 'Henson', 'Clarke', 'Ridley',
                                  'Morse', 'Paget', 'Dodge', 'Poindexter', 'Rey',
                                  'Wilkins', 'Gardener', 'Paddon', 'Graham', 'Thornton',
                                  'Carter', 'Shearer', 'Miller', 'Chadwick', 'Bloodworth', 'Akbar']

    def getRepository(self):
        return self.__repository

    def getValidator(self):
        return self.__validator

    def append(self, student):
        self.__repository.appendToList(student)

    def remove(self, student):
        self.__repository.removeFromList(student)

    def removeAll(self):
        self.__repository.erase()

    def verify(self, student):
        if self.__repository.verifyID(student.getID()) == True:
            raise ServiceError("student with ID " + str(student.getID()) + " already exists")

    def check(self, student):
        if self.__repository.verifyID(student.getID()) == False:
            raise ServiceError("student with ID " + str(student.getID()) + " doesn't exist")

    def update(self, student, newStudent):
        if student.getID() == newStudent.getID():
            self.__repository.replace(student, newStudent)
        else : raise ServiceError("ID" + str(student.getID()) + " doesn't match ID " + str(newStudent.getID()))

    def getRandomStudent(self):
        #ID = random.randint(10000, 99999)
        ID = random.randint(74180,74190)
        group = random.randint(100, 999)
        name = str(random.choice(self.__randomFirstName) + " " + random.choice(self.__randomSecondName))
        return Student(ID, group, name)

    def addRandomStudent(self, number):
        while number > 0:
            student = self.getRandomStudent()
            try:
                self.verify(student)
                self.__repository.appendToList(student)
                number -= 1
            except ServiceError:
                pass




