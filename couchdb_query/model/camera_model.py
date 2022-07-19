import sys, os
dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(dir, '.')))
sys.path.insert(0, os.path.abspath(os.path.join(dir, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(dir, '../doc')))
from couch_query import CouchQuery
from helper import func_info
from camera import Camera

class CameraModel(CouchQuery):
    def __init__(self, db):
        super().__init__(db)
        
    def update_cameras(self, cameras):
        if(isinstance(cameras, list) == False):
            f_info = func_info()
            print('[Error]: ', f_info[0], f_info[1], f_info[2], 
                  ' wrong data type: cameras is list type instead of ', type(cameras)) 
            return False
        for camera in cameras:
            if(isinstance(camera, Camera) == False):
                f_info = func_info()
                print('[Error]: ', f_info[0], f_info[1], f_info[2], 
                    ' wrong data type: camera is Camera type instead of ', type(camera))
                continue
            camera.save(self.db)
            
    def cameras_by_id(self, ids):
        if(isinstance(ids, list) == False):
            f_info = func_info()
            print('Error: ', f_info[0], f_info[1], f_info[2], ' wrong data type: ids is dict type instead of ', type(ids)) 
            return []
        list_camera = []
        for id in ids:
            camera = Camera.load_by_id(self.db, id)
            if(camera != None):
                list_camera.append(camera)
        return list_camera
            
        
if __name__ == '__main__':
    from couchdb import Server
    from couchdb.design import ViewDefinition
    from couchdb.http import HTTPError, ResourceNotFound
    from datetime import date, datetime
    couch = Server("http://admin:admin@172.21.100.174:5984")
    # couch = Server("http://admin:admin@localhost:5984")
    try:
        db = couch.create('camera')
    except HTTPError as err:
        print(err)
        db = couch['camera']
        
    camera_model = CameraModel(db)
    data_demo1 = {'ip':'172.21.100.100', 'mac': '1C:C3:16:29:F6:B1', 'description': 'TT.KCVL', 'floor': 4, 'nvr':'172.21.100.10'}
    
    data_demo2 = {'ip':'172.21.100.101', 'mac': '1C:C3:16:29:F6:D3', 'description': 'TT.KCVL', 'floor': 5, 'nvr':'172.21.100.10'}
    
    camera1 = Camera(data_demo1)
    camera2 = Camera(data_demo2)
    print(camera1.ip, camera2.ip)
    # print(camera1.save(db))
    # print(camera2.save(db))
    
    # data = staff_model.view_query('filter', 'by_staff_code', include_docs=True, key='12')
    data = camera_model.cameras_by_id(['8f16853e2aa2f548148b120e73bec972', '8f16853e2aa2f548148b120e73bed0a0'])
    print(len(data))
    for camera in data:
        print(camera.ip)
    
    # staff_model.update_staffs([staff1, staff2])