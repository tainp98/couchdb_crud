from couchdb.mapping import Document, TextField, IntegerField
from couchdb.http import HTTPError
from datetime import date, datetime, time
import sys, os
dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(dir, '..')))
from helper import func_info
from helper import json_serial, date_to_str, datetime_to_str, str_to_date, str_to_datetime
class Camera(Document):
    _id = TextField()
    ip = TextField()
    mac = TextField()
    description = TextField()
    floor = IntegerField()
    nvr = TextField()
    def __init__(self, dict_data=None, _id=None, ip=None, mac=None, 
                 description=None, floor=None, nvr=None):
        super().__init__()
        if(dict_data != None):
            if(dict_data.get('floor') != None):
                if(isinstance(dict_data['floor'], int) == False):
                    f_info = func_info()
                    raise Exception(f_info[0]+' '+f_info[1]+' '+f_info[2]+" Error floor data type")
            self._id = dict_data.get('_id')
            self.ip = dict_data.get('ip')
            self.mac = dict_data.get('mac')
            self.description = dict_data.get('description')
            self.floor = dict_data.get('floor')
            self.nvr = dict_data.get('nvr')
        else:
            if(floor != None):
                if(isinstance(floor, int) == False):
                    f_info = func_info()
                    raise Exception(f_info[0]+' '+f_info[1]+' '+f_info[2]+" Error floor data type")
            self._id = _id
            self.ip = ip
            self.mac = mac
            self.description = description
            self.floor = floor
            self.nvr = nvr

    def save(self, db):
        cam = {}
        if(self._id != None):
            try:
                cam = db[self._id]
            except HTTPError as err:
                f_info = func_info()
                print('HTTPError: ', f_info[0], f_info[1], f_info[2], err)
                cam['_id'] = self._id

        cam['ip'] = self.ip
        cam['mac'] = self.mac
        cam['description'] = self.description
        cam['floor'] = self.floor
        cam['nvr'] = self.nvr
        try:
            return db.update([cam])
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
            cam = db[self._id]
            self.ip = cam['ip']
            self.mac = cam['mac']
            self.description = cam['description']
            self.floor = cam['floor']
            self.nvr = cam['nvr']
        except HTTPError as err:
            f_info = func_info()
            print('HTTPError: ', f_info[0], f_info[1], f_info[2], err)
    
    @classmethod
    def load_by_id(cls, db, id):
        try:
            cam = db[id]
            return cls(cam)
        except HTTPError as err:
            f_info = func_info()
            print('HTTPError: ', f_info[0], f_info[1], f_info[2], err)

    def _to_dict(self):
        json_obj = {}
        if(self._id != None):
            json_obj['_id'] = self._id
        json_obj['ip'] = self.ip
        json_obj['mac'] = self.mac
        json_obj['description'] = self.description
        json_obj['floor'] = self.floor
        json_obj['nvr'] = self.nvr
        return json_obj
if __name__ == '__main__':
    cam = Camera({'ip': '172.21.104.100', 'mac': '1C:C3:16:29:F6:B1', 'description': 'TT.KCVL', 
                    'floor': 4, 'nvr':'172.21.100.10'})
    print(cam._id, cam.ip, cam.mac, cam.description, cam.floor, cam.nvr)