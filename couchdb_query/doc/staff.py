from couchdb import Server
from couchdb.design import ViewDefinition
from couchdb.mapping import Document, TextField, BooleanField, IntegerField, DateField, DateTimeField
from couchdb.http import HTTPError
from datetime import date, datetime, time
import sys, os
dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(dir, '..')))
from helper import func_info
from helper import json_serial
class Staff(Document):
    _id = TextField()
    staff_code = TextField()
    full_name = TextField()
    mail_code = TextField()
    cellphone = TextField()
    unit = TextField()
    department = TextField()
    date_of_birth = DateField()
    sex = TextField()
    title = TextField()
    note = TextField()
    should_roll_up = BooleanField()
    active = BooleanField()
    def __init__(self, id=None, staff_code=None, full_name=None, mail_code=None,
                 cellphone=None, unit=None, department=None, date_of_birth=None,
                 sex=None, title=None, note=None, should_roll_up=None, active=None):
        super().__init__()
        self._id = id
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

    def save(self, db):
        staff = {}
        if(self._id != None):
            try:
                staff = db[self._id]
            except HTTPError as err:
                f_info = func_info()
                print('HTTPError: ', f_info[0], f_info[1], f_info[2], err)

        staff['staff_code'] = self.staff_code
        staff['full_name'] = self.full_name
        staff['mail_code'] = self.mail_code
        staff['cellphone'] = self.cellphone
        staff['unit'] = self.unit
        staff['department'] = self.department
        staff['date_of_birth'] = json_serial(self.date_of_birth)
        staff['sex'] = self.sex
        staff['title'] = self.title
        staff['note'] = self.note
        staff['should_roll_up'] = self.should_roll_up
        staff['active'] = self.active
        try:
            db.update([staff])
        except HTTPError as err:
            f_info = func_info()
            print('HTTPError: ', f_info[0], f_info[1], f_info[2], err)
            return False
        except TypeError as err:
            f_info = func_info()
            print('TypeError: ', f_info[0], f_info[1], f_info[2], err)
        else:
            return True

    def load(self, db):
        try:
            staff = db[self._id]
            self.staff_code = staff['staff_code']
            self.full_name = staff['full_name']
            self.mail_code = staff['mail_code']
            self.cellphone = staff['cellphone']
            self.unit = staff['unit']
            self.department = staff['department']
            self.date_of_birth = staff['date_of_birth']
            self.sex = staff['sex']
            self.title = staff['title']
            self.note = staff['note']
            self.should_roll_up = staff['should_roll_up']
            self.active = staff['active']
        except HTTPError as err:
            f_info = func_info()
            print('HTTPError: ', f_info[0], f_info[1], f_info[2], err)
    
    @classmethod
    def load_by_id(cls, db, id):
        try:
            staff = db[id]
            return Staff.create(staff)
        except HTTPError as err:
            f_info = func_info()
            print('HTTPError: ', f_info[0], f_info[1], f_info[2], err)
# staff = Staff.create({'staff_code': 277457, 'full_name': 'NPT', 'mail_code': 'tainp', 'cellphone': '098881888', 'unit': 'TQDT', 'department': 'DK', 'date_of_birth':'02-10-1998', 'sex': 'male', 'title': 'system programing', 'note': 'pro', 'should_roll_up': True, 'active': True})
# print(staff.date_of_birth)