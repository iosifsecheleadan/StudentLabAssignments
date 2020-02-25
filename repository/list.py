import unittest

import random

from error.custom import ListError

class BreakIteration(Exception):
    pass

class List:
    def __init__(self) -> None:
        self.__list = []
        self.__len = len(self.__list)
        self.__index = 0

    def __str__(self) -> str:
        number = 0
        for item in self.__list:
            print(item)
            number += 1
        return "there are " + str(number) + " items in this list"

    def __eq__(self, other):
        return self.getList() == other.getList()

    # idkreally
    def __setitem__(self, key, value):
        self.swap(key, value)

    def __delitem__(self, key):
        self.__list[key:]=self.__list[key+1:]

    def __next__(self):
        if self.__index<self.__len:
            item = self.__list[self.__index]
        else: BreakIteration()
        self.__index += 1
        return item

    def __iter__(self):
        return self
    # idkreally

    def setList(self, list): #done
        self.__list = list

    def getList(self): #done
        return self.__list

    def getItemOnPosition(self, index): #done
        if index > len(self.getList())-1:
            raise ListError('Index out of range')
        return self.__list[index]

    def appendToList(self, item): #done
        self.__list.append(item)

    def removeFromList(self, item): #done
        self.__list.remove(item)

    def interchange(self, index1, index2): #done
        temp = self.__list[index1]
        self.__list[index1] = self.__list[index2]
        self.__list[index2] = temp

    def swap(self, index, item): #done
        self.__list[index]=item

    def insert(self, index, item): #done
        self.__list[index+1:]=self.__list[index:]
        self.__list[index] = item

    def erase(self): #done
        self.__list = []

    def removeFromIndex(self, index): #done
        self.__list[index+1:] = []

    def getIndex(self, item): #done
        for index in range(0, len(self.__list)):
            if self.__list[index]==item:
                return index
        raise ListError ("item with index " + str(index) + " doesn't exist")

    def replace(self, oldItem, newItem): #done
        ''' Replaces oldItem with newItem in list. '''
        for item in self.__list:
            if item == oldItem:
                index = self.getIndex(item)
                self.swap(index, newItem)
                return
        raise ListError(oldItem + " doesn't exist")

    def itemWithID(self, ID):
        ''' Returns the item with the given ID. '''
        for item in self.__list:
            if item.getID() == ID:
                return item
        raise ListError("item with ID " + str(ID) + " doesn't exist")

    def verifyID(self, ID):
        ''' Returns True if the ID exists and False otherwise. '''
        for item in self.__list:
            if item.getID() == ID:
                return True
        return False

    def removeStudentByID(self, ID):
        ''' Removes all students from the gradeList with given student ID '''
        for index in range(0, len(self.__list)):
            item = self.getItemOnPosition(index)
            if item.getStudentID() == ID:
                self.removeFromList(item)
            else: index += 1

    def removeAssignmentByID(self, ID):
        ''' Removes all assignments from the gradeList with given student ID '''
        for index in range(0, len(self.__list)):
            item = self.getItemOnPosition(index)
            if item.getAssignmentID() == ID:
                self.removeFromList(item)
            else: index += 1

    def shellSort(self, function): #done
        ratio = len(self.__list)//2
        ordered = False
        while ratio and not ordered:
            ordered = True
            index = 0
            while index + ratio < len(self.__list):
                saveIndex = index
                while True:
                    if not function(list[index], list[index + ratio]):
                        ordered = False
                        self.interchange(index, index + ratio)
                        if index - ratio < 0: break
                        else : index -= ratio
                    else: break
                index = saveIndex + 1
            ratio //= 2


class listRepository(unittest.TestCase):
    def test(self):
        self.testGet()
        self.testSet()
        self.testStrEqu()
        self.testRemove()
        self.testShellSort()

    def testGet(self):
        list = List()
        self.assertEqual(list.getList(), [])
        list.appendToList(0)
        list.appendToList(1)
        list.appendToList(2)
        self.assertEqual((list.getList()), [0,1,2])
        self.assertEqual(list.getItemOnPosition(2), 2)

    def testSet(self):
        list = List()
        list.setList([0,1,2,3,4,5])
        self.assertEqual(list.getList(), [0,1,2,3,4,5])
        list.swap(4,5)
        list.swap(5,4)
        self.assertEqual(list.getList(), [0,1,2,3,5,4])
        list.interchange(4,5)
        self.assertEqual(list.getList(), [0,1,2,3,4,5])
        list.appendToList(7)
        list.insert(13,6)
        self.assertEqual(list.getList(), [0,1,2,3,4,5,13,7])
        list.replace(13,6)
        self.assertEqual(list.getList(), [0,1,2,3,4,5,6,7])

    def testStrEqu(self):
        list = List()
        self.assertEqual(str(list), 'there are 0 items in this list')
        self.assertEqual(list, list)

    def testRemove(self):
        list = List()
        list.setList([0,1,2,3,4,5])
        list.removeFromList(5)
        self.assertEqual(list.getList(), [0,1,2,3,4])
        list.removeFromIndex(3)
        self.assertEqual(list.getList(), [0,1,2])
        list.erase()
        self.assertEqual(list.getList(), [])

    def testShellSort(self):
        list = List()
        list.setList([0,5,2,7,3,4,8,9,6,1])
        self.assertEqual(list.shellSort(lambda a,b: a<b), [0,1,2,3,4,5,6,7,8,9])
        self.assertEqual(list.shellSort(lambda a,b: a>b), [9,8,7,6,5,4,3,2,1,0])












