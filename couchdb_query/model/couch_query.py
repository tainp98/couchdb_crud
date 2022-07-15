from couchdb import Server
from couchdb.design import ViewDefinition
from couchdb.mapping import Document, TextField, IntegerField
from couchdb.http import HTTPError
from datetime import date, datetime, time
import sys
# adding Folder_2 to the system path
sys.path.insert(0, '/home/vietph/workspace/couchdb_crud/couchdb_query/doc')
from staff import Staff
class CouchQuery:
    def __init__(self, db):
        self.db = db
        
    def insert(self, dict_data = None, **kwargs):
        print('couch insert')
        if(dict_data != None):
            db.save(dict_data)
        else:
            db.save(kwargs)
    def read(self):
        pass
    def update(self):
        pass
    def delete(self):
        pass
    
class StaffQuery(CouchQuery):
    def __init__(self, db):
        super().__init__(db)
        
    def insert_many(self, list_doc, batch_size = 128):
        number_iter = len(list_doc) // 128
        # number_mod = len(list_doc) % 128
        for i in range(number_iter):
            try:
                db.update(list_doc[i*batch_size:(i+1)*batch_size])
            except TypeError as err:
                print(err)
                return False
        try:
            db.update(list_doc[number_iter*batch_size:])
        except TypeError as err:
            print(err)
            return False
        return True
        
import random 
if __name__ == '__main__': 
    couch = Server("http://admin:admin@172.21.100.174:5984")
    try:
        db = couch.create('staff')
    except HTTPError:
        print('http error')
        db = couch['staff']
    else:
        db = couch.create('staff')
    staff_query = StaffQuery(db)
    for row in db.view('filter/count_documents'):
        print(row.value)
    # staff_query.insert(staff_code=277457, full_name='NPT', mail_code='tainp',
    #                 cellphone='098881888', unit='TQDT', department='DK',
    #                 date_of_birth='02-10-1998', sex='male',
    #                 title='system programing', note='pro', 
    #                 should_roll_up=True, active=True)
# name = 'ABCDEFGHKIJMNLPQSTUVRW'
# list_doc = []
# batch_size = 128
# for code in range(201000, 205000):
#     full_name = name[random.randrange(0, 22)] + name[random.randrange(0, 22)] +\
#                 name[random.randrange(0, 22)] + name[random.randrange(0, 22)] +\
#                     name[random.randrange(0, 22)]
#     mail_code = full_name + '@vtx'
#     list_doc.append({'staff_code': code, 'full_name': full_name, 
#                      'mail_code': mail_code, 'cellphone': '098881888', 
#                      'unit': 'TQDT', 'department': 'DK', 'date_of_birth':'02-10-1998', 
#                      'sex': 'male', 'title': 'system programing', 'note': 'pro', 
#                      'should_roll_up': True, 'active': True})
#     if(len(list_doc) == batch_size):
#         print(len(list_doc))
#         staff_query.insert_many(list_doc)
#         list_doc.clear()
