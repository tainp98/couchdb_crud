import sys, os
from tokenize import group
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
    from camera_model import CameraModel
    import pandas as pd
    couch = CouchDBServer('172.21.100.174', 5984, 'admin', 'admin')
    print(couch.status())
    db = couch.create_db('detection')
        
    detection_model = DetectionModel(db)
    staff_model = StaffModel(couch.create_db('staff'))
    camera_model = CameraModel(couch.create_db('camera'))
    
    start_time = time.time()
    count_doc = detection_model.view_query('detection_design', 'count_documents')
    print(count_doc)
    end_time = (time.time() - start_time)*1000.0
    print("query_count_doc time = %s milli" % (end_time)) 

    all_staffid_reduce = staff_model.view_query('staff_design', 'all_staffid', group_level=1)
    all_staffid = []
    for staffid in all_staffid_reduce:
        all_staffid.append(staffid['value'])
    start_time = time.time()
    
    
    """Detect The appearance of a staff in a period of time"""
    start_time = time.time()
    minmax_byday = detection_model.view_query('staff_id', 'bytime', 
                                              startkey=['8f16853e2aa2f548148b120e73dd2a30', '2022-07-22 00:01:00'],
                                              endkey=['8f16853e2aa2f548148b120e73dd2a30', '2022-07-22 23:59:00'])
    # 8f16853e2aa2f548148b120e73e64a21
    # 8f16853e2aa2f548148b120e73dd2a30
    print(len(minmax_byday))
    end_time = (time.time() - start_time)*1000.0
    print("detect_by_staffid time = %s milli" % (end_time))
    person_trace = []
    for data in minmax_byday:
        staff = staff_model.doc_by_id(data['key'][0])
        camera = camera_model.doc_by_id(data['value']['camera_id'])
        person_trace.append({'full_name':staff['full_name'], 'mail_code':staff['mail_code'], 'ip':camera['ip'],
                             'floor':camera['floor'], 'cellphone':staff['cellphone'], 'unit':staff['unit'], 
                             'department':staff['department'],'appearance':data['value']['time'],
                             'score':data['value']['score']})
    df = pd.DataFrame(person_trace)
    print(df)
    df.to_csv('person_'+staff_model.doc_by_id('8f16853e2aa2f548148b120e73dd2a30')['mail_code']+'_'+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'.csv', index=False)
    
    """Report checkin time and checkout time of all staff in a day"""
    
    report_list = []
    start_time = time.time()
    for staff_id in all_staffid:
        # minmax_byday = detection_model.view_query('detection_design', 'minmaxtime_byday', group_level=1, 
        #                                           startkey=[staff_id, datetime.now().strftime('%Y-%m-%d')+' 00:01:00'],
        #                                           endkey=[staff_id, datetime.now().strftime('%Y-%m-%d')+' 23:59:00'])
        minmax_byday = detection_model.view_query('detection_design', 'minmaxtime_byday', group_level=1, 
                                                  startkey=[staff_id, '2022-07-22'+' 00:01:00'],
                                                  endkey=[staff_id, '2022-07-22'+' 23:59:00'])
        if(len(minmax_byday) == 0): continue
        # print(minmax_byday)
        staff = staff_model.doc_by_id(staff_id) 
        report_list.append({'full_name':staff['full_name'], 'mail_code':staff['mail_code'], 
                            'staff_code':staff['staff_code'], 'cellphone':staff['cellphone'],
                             'unit':staff['unit'], 'department':staff['department'], 
                             'checkin':minmax_byday[0]['value']['time'][0], 'checkout':minmax_byday[0]['value']['time'][1]})
    end_time = (time.time() - start_time)*1000.0
    print("detect_by_staffid time = %s milli" % (end_time))
    df = pd.DataFrame(report_list)
    print(df)
    # df.to_csv('report_'+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'.csv', index=False)