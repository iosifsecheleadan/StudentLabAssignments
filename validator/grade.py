from error.custom import ValidationError

class ValidatorGrade:
    def validate(self, grade, studentList, asssignmentList):
        try:
            if grade.getGrade() != 'not assigned' and (int(grade.getGrade()) < 0 or int(grade.getGrade() > 10)): raise ValidationError
            if int(grade.getStudentID())<0 or int(grade.getAssignmentID())<0: raise ValidationError
        except ValueError:
            raise ValidationError

