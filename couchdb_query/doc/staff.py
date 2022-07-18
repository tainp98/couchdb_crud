from couchdb import Server
from couchdb.design import ViewDefinition
from couchdb.mapping import Document, TextField, BooleanField, IntegerField, DateField, DateTimeField
from couchdb.http import HTTPError
from datetime import date, datetime, time
import sys, os
dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(dir, '..')))
from helper import func_info
from helper import json_serial, date_to_str, datetime_to_str, str_to_date, str_to_datetime
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
    def __init__(self, dict_data=None, _id=None, staff_code=None, full_name=None, mail_code=None,
                 cellphone=None, unit=None, department=None, date_of_birth=None,
                 sex=None, title=None, note=None, should_roll_up=None, active=None):
        super().__init__()
        if(dict_data != None):
            if(dict_data.get('date_of_birth') != None):
                if(isinstance(dict_data['date_of_birth'], date) == False):
                    f_info = func_info()
                    raise Exception(f_info[0]+' '+f_info[1]+' '+f_info[2]+" Error date_of_birth data type")
            self._id = dict_data.get('_id')
            self.staff_code = dict_data.get('staff_code')
            self.full_name = dict_data.get('full_name')
            self.mail_code = dict_data.get('mail_code')
            self.cellphone = dict_data.get('cellphone')
            self.unit = dict_data.get('unit')
            self.department = dict_data.get('department')
            self.date_of_birth = dict_data.get('date_of_birth')
            self.sex = dict_data.get('sex')
            self.title = dict_data.get('title')
            self.note = dict_data.get('note')
            self.should_roll_up = dict_data.get('should_roll_up')
            self.active = dict_data.get('active')
        else:
            if(date_of_birth != None):
                f_info = func_info()
                raise Exception(f_info[0]+' '+f_info[1]+' '+f_info[2]+" Error date_of_birth data type")
            self._id = _id
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
        staff['date_of_birth'] = date_to_str(self.date_of_birth)
        staff['sex'] = self.sex
        staff['title'] = self.title
        staff['note'] = self.note
        staff['should_roll_up'] = self.should_roll_up
        staff['active'] = self.active
        try:
            return db.update([staff])
        except HTTPError as err:
            f_info = func_info()
            print('HTTPError: ', f_info[0], f_info[1], f_info[2], err)
            return []
        except TypeError as err:
            f_info = func_info()
            print('TypeError: ', f_info[0], f_info[1], f_info[2], err)
            return []

    def load(self, db):
        try:
            staff = db[self._id]
            self.staff_code = staff['staff_code']
            self.full_name = staff['full_name']
            self.mail_code = staff['mail_code']
            self.cellphone = staff['cellphone']
            self.unit = staff['unit']
            self.department = staff['department']
            self.date_of_birth = str_to_date(staff['date_of_birth'])
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
            if(staff['date_of_birth'] != None):
                staff['date_of_birth'] = str_to_date(staff['date_of_birth'])
            return cls(staff)
        except HTTPError as err:
            f_info = func_info()
            print('HTTPError: ', f_info[0], f_info[1], f_info[2], err)

    def _to_json(self):
        json_obj = {}
        if(self._id != None):
            json_obj['_id'] = self._id
        json_obj['staff_code'] = self.staff_code
        json_obj['full_name'] = self.full_name
        json_obj['mail_code'] = self.mail_code
        json_obj['cellphone'] = self.cellphone
        json_obj['unit'] = self.unit
        json_obj['department'] = self.department
        if(self.date_of_birth != None):
            json_obj['date_of_birth'] = date_to_str(self.date_of_birth)
        json_obj['sex'] = self.sex
        json_obj['title'] = self.title
        json_obj['note'] = self.note
        json_obj['should_roll_up'] = self.should_roll_up
        json_obj['active'] = self.active
        return json_obj
if __name__ == '__main__':
    staff = Staff({'staff_code': 277457, 'full_name': 'NPT', 'mail_code': 'tainp', 'cellphone': '098881888', 'unit': 'TQDT', 'department': 'DK', 
                        'date_of_birth':date(1998, 10, 2), 'sex': 'male', 'title': 'system programing', 'note': 'pro', 'should_roll_up': True, 'active': True})
    print(staff._id, type(staff.date_of_birth))