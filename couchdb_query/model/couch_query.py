from couchdb import Server
from couchdb.design import ViewDefinition
from couchdb.mapping import Document, TextField, BooleanField, IntegerField, DateField
from couchdb.http import HTTPError
from datetime import date, datetime, time
import sys
import inspect
from json import dumps
# adding Folder_2 to the system path
# sys.path.insert(0, '/home/vietph/workspace/couchdb_crud/couchdb_query/doc')
sys.path.insert(0, '/home/tainp/workspace/couchdb_crud/couchdb_query/doc')
from staff import Staff
def func_info():
  callerframerecord = inspect.stack()[1]    # 0 represents this line
                                            # 1 represents line at caller
  frame = callerframerecord[0]
  info = inspect.getframeinfo(frame)
  file_name = 'File "' + info.filename + '"'
  func_name = 'in ' + info.function
  line = 'line ' + str(info.lineno)
  return file_name, func_name, line

class CouchQuery:
    def __init__(self, db):
        self.db = db
        
    def createView(self, design_name, view_name, map_func, reduce_func=None):
        view = ViewDefinition(design_name, view_name, map_fun=map_func, reduce_fun=reduce_func)
        res = view.sync(self.db) 
        return view.get_doc(self.db)
    
    def insert_one(self, dict_data, **kwargs):
        try:
            if(dict_data != None):
                return db.save(dict_data)
            else:
                return db.save(kwargs)
        except HTTPError as err:
            f_info = func_info()
            print('HTTPError: ', f_info[0], f_info[1], f_info[2], err)
    
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

    def update_one(self, doc_object):
        doc_object.save(self.db)

    def update_many(self, doc_object_list):
        for doc_object in doc_object_list:
            doc_object.save(self.db)
    
class StaffModel(CouchQuery):
    def __init__(self, db):
        super().__init__(db)    

        
import random 
if __name__ == '__main__': 
    # couch = Server("http://admin:admin@172.21.100.174:5984")
    couch = Server("http://admin:admin@localhost:5984")
    try:
        db = couch.create('staff')
    except HTTPError as err:
        print(err)
        db = couch['staff']

    

    data = {'staff_code': 277457, 'full_name': 'NPTttaaiiii', 'mail_code': 'tainp', 
    'cellphone': '098881888', 'unit': 'TQDT', 'department': 'DK', 
    'sex': 'male', 'title': 'system programing', 
    'note': 'pro', 'should_roll_up': True, 'active': True}
    # staff_model = StaffModel(db)
    # doc_view = staff_model.createView('docs', 'by_name', '''function(doc) {
    #         emit(doc.full_name, doc._id);
    #     }''')
    # print(doc_view)
    # for row in db.view('docs/by_name', wrapper=None, include_docs=True, key='NPT'):
    #     print(row.key, row.value, row.doc)
    # data = staff_model.insert_one(data)
    # print(data[0], data[1])
    staff1 = Staff.create(data)
    # staff.full_name = 'TAIII'
    staff1.date_of_birth = date(1998, 10, 2)
    staff1.save(db)
    # staff_model = StaffModel(db)
    # staff = Staff(id='293e39d00fe0a9f1d5385a6488728c87')
    # staff.load(db)
    # staff.full_name = "TAIAJAJgggggDDDDD"
    # staff_model.update_many([staff1, staff])
    # staff = Staff.load_by_id(db, id='293e39d00fe0a9f1d5385a6488728c87')
    # print(staff.full_name)
    # staff.full_name = "NPTaii"
    # staff.save()
    # staff = StaffModel(db)
    # staff.load_attr(id='293e39d00fe0a9f1d5385a6488728c87')
    # staff.full_name = "Tai Nguyen Phu"
    # staff.save()
    # st = staff.update_by_attr(db, id='293e39d00fe0a9f1d5385a64887253dc', full_name='Nguyen Tai')
    # print(st.full_name)
    # for row in db.view('filter/count_documents'):
    #     print(row.value)
    # staff_query.insert(staff_code=277457, full_name='NPT', mail_code='tainp',
    #                 cellphone='098881888', unit='TQDT', department='DK',
    #                 date_of_birth='02-10-1998', sex='male',
    #                 title='system programing', note='pro', 
    #                 should_roll_up=True, active=True)
# name = 'ABCDEFGHKIJMNLPQSTUVRW'
# list_doc = []
# batch_size = 128
# for code in range(101000, 105000):
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
