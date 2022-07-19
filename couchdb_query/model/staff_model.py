import sys, os
dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(dir, '.')))
sys.path.insert(0, os.path.abspath(os.path.join(dir, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(dir, '../doc')))
from couch_query import CouchQuery
from helper import func_info
from staff import Staff

class StaffModel(CouchQuery):
    def __init__(self, db):
        super().__init__(db)
        
    def update_staffs(self, staffs):
        if(isinstance(staffs, list) == False):
            f_info = func_info()
            print('[Error]: ', f_info[0], f_info[1], f_info[2], 
                  ' wrong data type: staffs is list type instead of ', type(staffs)) 
            return False
        for staff in staffs:
            if(isinstance(staff, Staff) == False):
                f_info = func_info()
                print('[Error]: ', f_info[0], f_info[1], f_info[2], 
                    ' wrong data type: staff is Staff type instead of ', type(staff))
                continue
            staff.save(self.db)
            
    def staffs_by_id(self, ids):
        if(isinstance(ids, list) == False):
            f_info = func_info()
            print('Error: ', f_info[0], f_info[1], f_info[2], ' wrong data type: ids is dict type instead of ', type(ids)) 
            return []
        list_staff = []
        for id in ids:
            staff = Staff.load_by_id(self.db, id)
            if(staff != None):
                list_staff.append(staff)
        return list_staff
            
        
if __name__ == '__main__':
    from couchdb import Server
    from couchdb.design import ViewDefinition
    from couchdb.http import HTTPError, ResourceNotFound
    from datetime import date, datetime
    couch = Server("http://admin:admin@172.21.100.174:5984")
    # couch = Server("http://admin:admin@localhost:5984")
    try:
        db = couch.create('staff')
    except HTTPError as err:
        print(err)
        db = couch['staff']
        
    staff_model = StaffModel(db)
    data_demo1 = {'_id':10, 'staff_code': 12, 'full_name': 'NPT', 'mail_code': 'tainp', 'cellphone': '098881888', 'unit': 'TQDT', 'department': 'DK', 
                        'date_of_birth':date(1998, 10, 2), 'sex': 'male', 'title': 'system programing', 'note': 'pro', 'should_roll_up': True, 'active': True}
    
    data_demo2 = {'staff_code': 13, 'full_name': 'NPT', 'mail_code': 'tainp', 'cellphone': '098881888', 'unit': 'TQDT', 'department': 'DK', 
                        'date_of_birth':date(1998, 10, 2), 'sex': 'male', 'title': 'system programing', 'note': 'pro', 'should_roll_up': True, 'active': True}
    
    staff1 = Staff(data_demo1)
    staff2 = Staff(data_demo2)
    print(staff1.staff_code, staff2.staff_code)
    print(staff1.save(db))
    # print(staff2.save(db))
    
    # data = staff_model.view_query('filter', 'by_staff_code', include_docs=True, key='12')
    data = staff_model.staffs_by_id(['8f16853e2aa2f548148b120e73be83aa', '8f16853e2aa2f548148b120e73be9230'])
    print(len(data))
    for staff in data:
        print(staff.staff_code)
    
    # staff_model.update_staffs([staff1, staff2])