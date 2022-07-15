from couchdb import Server
from couchdb.design import ViewDefinition
from couchdb.mapping import Document, TextField, BooleanField, IntegerField, DateField
from datetime import date, datetime, time
class Staff(Document):
    id = IntegerField()
    staff_code = TextField()
    full_name = TextField()
    mail_code = TextField()
    cellphone = TextField()
    unit = TextField()
    department = TextField()
    date_of_birth = TextField()
    sex = TextField()
    title = TextField()
    note = TextField()
    should_roll_up = BooleanField()
    active = BooleanField()
    def __init__(self, **kwargs):
        super().__init__()
        if(kwargs.get('id') != None):
            self.id = kwargs['id']
        if(kwargs.get('staff_code') != None):
            self.staff_code = kwargs['staff_code']
        if(kwargs.get('full_name') != None):
            self.full_name = kwargs['full_name']
        if(kwargs.get('mail_code') != None):
            self.mail_code = kwargs['mail_code']
        if(kwargs.get('cellphone') != None):
            self.cellphone = kwargs['cellphone']
        if(kwargs.get('unit') != None):
            self.unit = kwargs['unit']
        if(kwargs.get('department') != None):
            self.department = kwargs['department']
        if(kwargs.get('date_of_birth') != None):
            self.date_of_birth = kwargs['date_of_birth']
        if(kwargs.get('sex') != None):
            self.sex = kwargs['sex']
        if(kwargs.get('title') != None):
            self.title = kwargs['title']
        if(kwargs.get('note') != None):
            self.note = kwargs['note']
        if(kwargs.get('should_roll_up') != None):
            self.should_roll_up = kwargs['should_roll_up']
        if(kwargs.get('active') != None):
            self.active = kwargs['active']
    @classmethod
    def create(cls, dict_data):
        id, staff_code, full_name, mail_code = None, None, None, None
        cellphone, unit, department, date_of_birth = None, None, None, None
        sex, title, note, should_roll_up, active = None, None, None, None, None
        if(dict_data.get('id') != None):
            id = dict_data['id']
        if(dict_data.get('staff_code') != None):
            staff_code = dict_data['staff_code']
        if(dict_data.get('full_name') != None):
            full_name = dict_data['full_name']
        if(dict_data.get('mail_code') != None):
            mail_code = dict_data['mail_code']
        if(dict_data.get('cellphone') != None):
            cellphone = dict_data['cellphone']
        if(dict_data.get('unit') != None):
            unit = dict_data['unit']
        if(dict_data.get('department') != None):
            department = dict_data['department']
        if(dict_data.get('date_of_birth') != None):
            date_of_birth = dict_data['date_of_birth']
        if(dict_data.get('sex') != None):
            sex = dict_data['sex']
        if(dict_data.get('title') != None):
            title = dict_data['title']
        if(dict_data.get('note') != None):
            note = dict_data['note']
        if(dict_data.get('should_roll_up') != None):
            should_roll_up = dict_data['should_roll_up']
        if(dict_data.get('active') != None):
            active = dict_data['active']
        return cls(id=id, staff_code=staff_code, full_name=full_name, mail_code=mail_code,
                   cellphone=cellphone, unit=unit, department=department, date_of_birth = date_of_birth,
                   sex=sex, title=title, note=note, should_roll_up=should_roll_up, active=active)
# staff = Staff.create({'staff_code': 277457, 'full_name': 'NPT', 'mail_code': 'tainp', 'cellphone': '098881888', 'unit': 'TQDT', 'department': 'DK', 'date_of_birth':'02-10-1998', 'sex': 'male', 'title': 'system programing', 'note': 'pro', 'should_roll_up': True, 'active': True})
# print(staff.date_of_birth)