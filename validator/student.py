from error.custom import ValidationError

class ValidatorStudent:
    def validate(self, student):
        try:
            if int(student.getID()) < 0:
                raise ValidationError
        except ValueError:
            raise ValidationError


