from couchdb import Server
from couchdb.design import ViewDefinition
from couchdb.mapping import Document, TextField, BooleanField, IntegerField, DateTimeField

class Staff(Document):
    id = IntegerField
    staff_code = TextField
    full_name = TextField
    mail_code = TextField
    cellphone = TextField
    unit = TextField
    department = TextField
    date_of_birth = DateTimeField
    sex = TextField
    title = TextField
    note = TextField
    should_roll_up = BooleanField
    active = BooleanField
    def __init__(self, id, staff_code, full_name, mail_code, 
                 cellphone, unit, department, date_of_birth, 
                 sex, title, note, should_roll_up, active):
        super().__init__()
        self.id = id
        self.staff_code = staff_code
        self.full_name = full_name
        self.mail_code = mail_code
        self.cellphone = cellphone
        self.unit = unit
        self.department = department
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.title = title
        self.note = note
        self.should_roll_up = should_roll_up
        self.active = active
staff = Staff(1, 2,3,1,1,1,1,1,1,1,1,1,1)
print(staff.id, staff.staff_code, staff.full_name)
print(sorted(staff.items()))