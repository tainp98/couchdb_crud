import sys, os
dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(dir, '.')))
sys.path.insert(0, os.path.abspath(os.path.join(dir, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(dir, '../doc')))
from couch_query import CouchQuery
from couchdb_server import CouchDBServer
from helper import func_info
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
    couch = CouchDBServer('172.21.100.174', 5984, 'admin', 'admin')
    print(couch.status())
    db = couch.create_db('detection')
        
    detection_model = DetectionModel(db)
    data_demo1 = {'detection_time': datetime.now(), 'staff_id': '277457', 'feature': [1.0, 2.2, 3.33]}
    
    data_demo2 = {'detection_time': datetime.now(), 'staff_id': '277457', 'feature': [2.0, 3.2, 4.33]}
    
    detection1 = Detection(data_demo1)
    detection2 = Detection(data_demo2)
    # print(detection1.feature, detection2.feature)
    # print(detection1.save(db))
    # print(detection2.save(db))
    
    # data = staff_model.view_query('filter', 'by_staff_code', include_docs=True, key='12')
    data = detection_model.detections_by_id(['8f16853e2aa2f548148b120e73bedf3d', '8f16853e2aa2f548148b120e73bee75f'])
    print(len(data))
    for detection in data:
        print(detection.feature)