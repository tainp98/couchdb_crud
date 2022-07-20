import sys, os
dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(dir, '.')))
sys.path.insert(0, os.path.abspath(os.path.join(dir, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(dir, '../doc')))
from couch_query import CouchQuery
from couchdb_server import CouchDBServer
from helper import datetime_to_str, func_info
from detection import Detection

class DetectionModel(CouchQuery):
    def __init__(self, db):
        super().__init__(db)
        
    def update_detections(self, detections):
        if(isinstance(detections, list) == False):
            f_info = func_info()
            print('[Error]: ', f_info[0], f_info[1], f_info[2], 
                  ' wrong data type: staffs is list type instead of ', type(detections)) 
            return False
        for detection in detections:
            if(isinstance(detection, Detection) == False):
                f_info = func_info()
                print('[Error]: ', f_info[0], f_info[1], f_info[2], 
                    ' wrong data type: detection is Detection type instead of ', type(detection))
                continue
            detection.save(self.db)
            
    def detections_by_id(self, ids):
        if(isinstance(ids, list) == False):
            f_info = func_info()
            print('Error: ', f_info[0], f_info[1], f_info[2], ' wrong data type: ids is dict type instead of ', type(ids)) 
            return []
        list_detection = []
        for id in ids:
            detection = Detection.load_by_id(self.db, id)
            if(detection != None):
                list_detection.append(detection)
        return list_detection
            
        
if __name__ == '__main__':
    from couchdb import Server
    from couchdb.design import ViewDefinition
    from couchdb.http import HTTPError, ResourceNotFound, Unauthorized
    from datetime import date, datetime
    import time
    from staff_model import StaffModel
    import pandas as pd
    couch = CouchDBServer('172.21.100.174', 5984, 'admin', 'admin')
    print(couch.status())
    db = couch.create_db('detection')
        
    detection_model = DetectionModel(db)
    staff_model = StaffModel(couch.create_db('staff'))
    data_demo1 = {'detection_time': datetime.now(), 'staff_id': '277457', 'feature': [1.0, 2.2, 3.33]}
    
    data_demo2 = {'detection_time': datetime.now(), 'staff_id': '277457', 'feature': [2.0, 3.2, 4.33]}
    
    detection1 = Detection(data_demo1)
    detection2 = Detection(data_demo2)
    
    start_time = time.time()
    count_doc = detection_model.view_query('detection_design', 'count_documents')
    print(count_doc)
    end_time = (time.time() - start_time)*1000.0
    print("query_count_doc time = %s milli" % (end_time)) 
    
    staff_doc = staff_model.doc_by_id('8f16853e2aa2f548148b120e73de157e')
    print(staff_doc)
    start_time = time.time()
    detect_by_staffid = detection_model.view_query('detection_design', 'by_staffid', include_docs=False, key='8f16853e2aa2f548148b120e73de157e') #, key='8f16853e2aa2f548148b120e73dc20a9'
    # print(detect_by_staffid)
    # for doc in detect_by_staffid:
    #     print(doc['value'])
     
    
    start_time = time.time()
    minmax_time = detection_model.view_query('staff_id', 'minmaxtime', include_docs=False, group_level=1)
    print(len(minmax_time))
    end_time = (time.time() - start_time)*1000.0
    print("detect_by_staffid time = %s milli" % (end_time))
    staff_list = []
    for min_max in minmax_time:
        staff_doc = staff_model.doc_by_id(min_max['key'])
        staff_info_in_day = {}
        staff_info_in_day['staff_id'] = staff_doc['_id']
        staff_info_in_day['staff_code'] = staff_doc['staff_code']
        staff_info_in_day['full_name'] = staff_doc['full_name']
        staff_info_in_day['department'] = staff_doc['department']
        staff_info_in_day['checkin_time'] = min_max['value'][0]
        staff_info_in_day['checkout_time'] = min_max['value'][1]
        # print(staff_info_in_day)
        staff_list.append(staff_info_in_day)
    
    df = pd.DataFrame(staff_list)
    print(df)
    df.to_csv('report_'+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'.csv', index=False)
    
    
    
    # print(detection1.feature, detection2.feature)
    # print(detection1.save(db))
    # print(detection2.save(db))
    
    # data = staff_model.view_query('filter', 'by_staff_code', include_docs=True, key='12')
    # data = detection_model.detections_by_id(['8f16853e2aa2f548148b120e73bedf3d', '8f16853e2aa2f548148b120e73bee75f'])
    # print(len(data))
    # for detection in data:
    #     print(detection.feature)