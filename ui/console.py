from model.student import Student
from model.assignment import Assignment
from model.grade import Grade

from error.custom import ServiceError, ConsoleError, ListError, ValidationError

import random
import operator
from repository.list import List

class Console:
    def __init__(self, servStud, servAssig, servGrade, prop) -> None:
        self.__prop = prop
        self.__servGrade = servGrade
        self.__servAssig = servAssig
        self.__servStud = servStud
        self.__undoList = List()
        self.__undoIndex = -1
        self.__commands = {"add": self.__add,
                           "print": self.__print,
                           "random": self.__random,
                           "remove": self.__remove,
                           "update": self.__update,
                           "assign": self.__assign,
                           "commands": self.__commands,
                           "statistics": self.__statistics,
                           "save" : self.__save,
                           "undo": self.__undo,
                           "redo": self.__redo}

    def run(self):
        try:
            properties = self.__prop.getSettings()
        except ValueError as errorMessage:
            print(errorMessage)
        self.__servStud.getRepository().setList(properties['students'])
        self.__servAssig.getRepository().setList(properties['assignments'])
        self.__servGrade.getRepository().setList(properties['grades'])
        print('type "commands" for help')
        while True:
            userInput = input("Enter command: ")
            userSplit = userInput.split()
            if userSplit[0] in self.__commands:
                try:
                    self.__commands[userSplit[0]](userSplit)
                except ConsoleError:
                    print("wrong input you idiot")
                except ValueError:
                    print("wrong input you idiot")
                except ValidationError:
                    print("not a valid item")
                except ServiceError as serviceErrorMessage:
                    print(serviceErrorMessage)
                except ListError as listErrorMessage:
                    print(listErrorMessage)
                except Exception:
                    print("you really managed to fuck it up \n not even I know what the hell you did")
            elif userInput == "exit":
                return
            else:
                print("wrong input you idiot")

    def __save(self, nothing):
        properties = {'students': self.__servStud.getRepository().getList(),
                      'assignments': self.__servAssig.getRepository().getList(),
                      'grades': self.__servGrade.getRepository().getList()}
        self.__prop.setSettings(properties)
        print("All data has benn saved. ")

    # UNDO REDO

    def __undo(self, nothing):
        if self.__undoIndex == -1:
            print("that's all the undos you get for today mister")
        else:
            function = self.__undoList.getList()[self.__undoIndex][0]
            update = [self.__servStud.update, self.__servAssig.update, self.__servGrade.update]
            if function in update:
                argument1 = self.__undoList.getList()[self.__undoIndex][1]
                argument2 = self.__undoList.getList()[self.__undoIndex][2]
                # call undo
                function(argument1, argument2)
            else:
                argument = self.__undoList.getList()[self.__undoIndex][1]
                # call undo
                function(argument)
            self.__undoIndex -= 1
            print('undone')

    def __redo(self, nothing):
        if self.__undoIndex == len(self.__undoList.getList())-1:
            print("that's all the redos you get for today mister")
        else:
            self.__undoIndex += 1
            function = self.__undoList.getList()[self.__undoIndex][0]
            reverse = {self.__servStud.append : self.__servStud.remove, self.__servAssig.append : self.__servAssig.remove, self.__servGrade.append : self.__servGrade.remove,
                       self.__servStud.remove : self.__servStud.append, self.__servAssig.remove : self.__servAssig.append, self.__servGrade.remove : self.__servGrade.append}
            update = [self.__servStud.update, self.__servAssig.update, self.__servGrade.update]
            if function in reverse:
                function = reverse[function]
                argument = self.__undoList.getList()[self.__undoIndex][1]
                # call redo
                function(argument)
            elif function in update:
                argument1 = self.__undoList.getList()[self.__undoIndex][2]
                argumet2 = self.__undoList.getList()[self.__undoIndex][1]
                # call redo
                function(argument1, argumet2)
            print('redone')

    def __print(self, userSplit):
        if len(userSplit)!=2: raise ConsoleError
        elif userSplit[1]=="student":
            print(self.__servStud.getRepository())
        elif userSplit[1]=="assignment":
            print(self.__servAssig.getRepository())
        elif userSplit[1]=="grade":
            print(self.__servGrade.getRepository())
        else: raise ConsoleError

    def __add(self, userSplit):
        if len(userSplit)!=2: raise ConsoleError
        elif userSplit[1] == "student" :
            # add student
            student = self.userStudent()
            self.__servStud.verify(student)
            self.__servStud.append(student)
            print(str(student) + " added")
            # prepare undo add student
            self.__undoList.removeFromIndex(self.__undoIndex)
            self.__undoList.appendToList((self.__servStud.remove, student))
            self.__undoIndex += 1
        elif userSplit[1] == "assignment":
            # add assignment
            assignment = self.userAssignment()
            self.__servAssig.verify(assignment)
            self.__servAssig.append(assignment)
            print(str(assignment) + " added")
            # prepare undo add assignment
            self.__undoList.removeFromIndex(self.__undoIndex)
            self.__undoList.appendToList((self.__servAssig.remove, assignment))
            self.__undoIndex += 1
        elif userSplit[1] == "grade":
            # add grade
            grade = self.userGrade()
            self.__servGrade.verifyGrade(grade)
            self.__servGrade.append(grade)
            print(str(grade) + " added")
            # prepare undo add grade
            self.__undoList.removeFromIndex(self.__undoIndex)
            self.__undoList.appendToList((self.__servGrade.remove, grade))
            self.__undoIndex += 1
        else: raise ConsoleError

    def __remove(self, userSplit):
        if len(userSplit) != 2: raise ConsoleError
        elif userSplit[1] == "student":
            # remove student
            student = self.userStudent()
            self.__servStud.check(student)
            self.__servStud.remove(student)
            self.__servGrade.removeStudents(student.getID())
            print(str(student) + " removed")
            # prepare undo remove student
            self.__undoList.removeFromIndex(self.__undoIndex)
            self.__undoList.appendToList((self.__servStud.append, student))
            self.__undoIndex += 1
        elif userSplit[1] == "assignment":
            # remove assignment
            assignment = self.userAssignment()
            self.__servAssig.check(assignment)
            self.__servAssig.remove(assignment)
            self.__servGrade.removeAssignments(assignment.getID())
            print(str(assignment) + " removed")
            # prepare undo remove assignment
            self.__undoList.removeFromIndex(self.__undoIndex)
            self.__undoList.appendToList((self.__servAssig.append, assignment))
            self.__undoIndex += 1
        elif userSplit[1] == "grade":
            # remove grade
            grade = self.userGrade()
            self.__servGrade.checkGrade(grade)
            self.__servGrade.remove(grade)
            print(str(grade) + " removed")
            # prepare undo remove grade
            self.__undoList.removeFromIndex(self.__undoIndex)
            self.__undoList.appendToList((self.__servGrade.append, grade))
            self.__undoIndex += 1
        elif userSplit[1] == "all":
            self.__servStud.removeAll()
            self.__servAssig.removeAll()
            self.__servGrade.removeAll()
            self.__undoList.erase()
            print("All items removed.")
        else: raise ConsoleError
        # undo

    def __update(self, userSplit):
        if len(userSplit)!=2 : raise ConsoleError
        elif userSplit[1] == "student":
            # update student
            student = self.userStudent()
            self.__servStud.check(student)
            newStudent = self.userStudent()
            self.__servStud.update(student, newStudent)
            print(str(student) + " replaced with " + str(newStudent))
            # prepare undo update student
            self.__undoList.removeFromIndex(self.__undoIndex)
            self.__undoList.appendToList((self.__servStud.update, newStudent, student))
            self.__undoIndex += 1
        elif userSplit[1] == "assignment":
            # update assignment
            assignment = self.userAssignment()
            self.__servAssig.check(assignment)
            newAssignment = self.userAssignment()
            self.__servAssig.update(assignment, newAssignment)
            print(str(assignment) + " replaced with " + str(newAssignment))
            # prepare undo update assignment
            self.__undoList.removeFromIndex(self.__undoIndex)
            self.__undoList.appendToList((self.__servAssig.update, newAssignment, assignment))
            self.__undoIndex += 1
        elif userSplit[1] == "grade":
            # update grade
            grade = self.userGrade()
            self.__servGrade.checkGrade(grade)
            newGrade = self.userGrade()
            self.__servGrade.update(grade, newGrade)
            print(str(grade) + " replaced with " + str(newGrade))
            # prepare undo update grade
            self.__undoList.removeFromIndex(self.__undoIndex)
            self.__undoList.appendToList((self.__servGrade.update, newGrade, grade))
            self.__undoIndex += 1
        else: raise ConsoleError
        # undo

    def __assign(self, userSplit):
        if len(userSplit)!=2: raise ConsoleError
        assignment = self.userAssignment()
        self.__servAssig.check(assignment)
        self.__servGrade.assign(int(userSplit[1]), assignment.getID())
        # undo. this one's complicated

    def __random(self, userSplit):
        if len(userSplit) != 3: raise ConsoleError
        elif userSplit[1] == "student":
            self.__servStud.addRandomStudent(int(userSplit[2]))
            print(userSplit[2] + " random students added")
        elif userSplit[1] == "assignment":
            self.__servAssig.addRandomAssignment(int(userSplit[2]))
            print(userSplit[2] + " random assignments added")
        elif userSplit[1] == "grade":
            self.__servGrade.addRandomGrade(int(userSplit[2]))
            print(userSplit[2] + " random grades added")
        else: raise ConsoleError
        # undo

    def __statistics(self, userSplit):
        userInput = ' '.join(userSplit[1:])
        if userInput == 'students with assignment':
            assignment = self.inputAssignment()
            studentsWithAssignment = self.__servGrade.studentsWithAssignment(assignment)
            # sort studentsWithAssignment alphabetically. Somehow...
            #studentsWithAssignment.shellSort(lambda item1, item2: item1.getName()<item2.getName())
            print(studentsWithAssignment)
        elif userInput == 'late students':
            lateStudents = self. __servGrade.lateStudents()
            print(lateStudents)
        elif userInput == 'best students':
            bestStudents = self.__servGrade.bestStudents()
            # sort bestStudents by average grade. Somehow...
            #bestStudents.shellSort(lambda item1, item2: self.__servGrade.getAverageStudentGrade(item1) > self.__servGrade.getAverageStudentGrade(item2))
            print(bestStudents)
        elif userInput == 'assignments with grades':
            assignmentsWithGrades = self.__servGrade.assignmentsWithGrades()
            # sort assignmentsWithGrades by average grade (descending). Somehow...
            #assignmentsWithGrades.shellSort(lambda item1, item2: self.__servGrade.getAverageAssignmentGrade(item1) < self.__servGrade.getAverageAssignmentGrade(item2))
            print(assignmentsWithGrades)
        else: print('wrong input you idiot')

    def inputStudent(self):
        student = input("Give student (ID, group, name): ")
        student = student.split(None, 2)
        if len(student) != 3: raise ConsoleError
        return Student(student[0], student[1], student[2])

    def inputAssignment(self):
        assignment = input("Give assignment (ID, deadline, description): ")
        assignment = assignment.split(None, 2)
        if len(assignment)!=3: raise ConsoleError
        return Assignment(assignment[0], assignment[1], assignment[2])

    def inputGrade(self):
        grade = input("Give grade (student ID, assignment ID, grade): ")
        grade = grade.split(None, 2)
        if len(grade)!=3: raise ConsoleError
        return Grade(grade[0],grade[1],grade[2])

    def userStudent(self):
        student = self.inputStudent()
        self.__servStud.getValidator().validate(student)
        print(str(student) + " read")
        return student

    def userAssignment(self):
        assignment = self.inputAssignment()
        self.__servAssig.getValidator().validate(assignment)
        print(str(assignment) + " read")
        return assignment

    def userGrade(self):
        grade = self.inputGrade()
        self.__servGrade.getValidator().validate(grade, self.__servAssig.getRepository(), self.__servStud.getRepository())
        print(str(grade) + " read")
        return grade


    def __commands(self, userSplit):
        print('''You already have 10 random students, assignments and grades in your program. 
Commands: 
"add <student>/<assignment>/<grade>" :                  enter a new student/assignment/grade
"remove <student>/<assignment>/<grade/all>" :           remove an existing student/assignment/grade ("all" deletes everything including undos and redos)
"update <student>/<assignment>/<grade>" :               update an existing student/assignment/grade
"random <student>/<assignment>/<grade> <integer>" :     adds as many students/assignments/grades as given integer 
                                                            *NOTE: only recommended to add as many grades as students and assignments*
"print <student>/<assignment>/<grade>" :                prints all your students/assignments/grades
"assign <integer>" :                                    assigns an existing assignment to all students of a group
"statistics" :                                          prints out different statistics about students, assignments and grades
''')

# add reverse to undo list

