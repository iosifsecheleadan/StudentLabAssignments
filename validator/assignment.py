from error.custom import ValidationError

class ValidatorAssignment:
    def validate(self, assignment):
        try:
            assignment.setDeadline(self.valiDate(assignment.getDeadline()))
            if int(assignment.getID())<0:
                raise ValidationError
        except ValueError or IndexError:
            raise ValidationError

    def valiDate(self, date):
        date = date.split('.')
        if len(date)!=3: raise ValidationError
        try:
            date[0]=int(date[0])
            date[1]=int(date[1])
            date[2]=int(date[2])
        except ValueError:
            raise ValidationError

        # basic
        if date[0]<0 or date[0]>31 or date[1]<0 or date[1]>12 or date[2]<2015: raise ValidationError
        # 30 day month
        if (date[1] in [4,6,9,11]) and date[0]>30: raise ValidationError
        # february
        if date[1] == 2 and ((date[2] % 4 == 0 and date[0] > 29) or (date[2] % 4 != 0 and date[0] > 28)): raise ValidationError

        return str(date[0]) + "." + str(date[1]) + "." + str(date[2])

