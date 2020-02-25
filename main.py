from ui.console import Console

from repository.list import List

from validator.grade import ValidatorGrade
from validator.assignment import ValidatorAssignment
from validator.student import ValidatorStudent

from service.grade import ServiceGrade
from service.assignment import ServiceAssignment
from service.student import ServiceStudent

from settings.properties import Properties

prop = Properties()

repoAssig = List()
validAssig = ValidatorAssignment()
servAssig = ServiceAssignment(repoAssig, validAssig)

repoStud = List()
validStud = ValidatorStudent()
servStud = ServiceStudent(repoStud, validStud)

repoGrade = List()
validGrade = ValidatorGrade()
servGrade = ServiceGrade(repoGrade, repoStud, repoAssig, validGrade)

console = Console(servStud, servAssig, servGrade, prop)

console.run()

