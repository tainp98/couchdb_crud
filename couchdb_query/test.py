import pandas as pd 
import numpy as np
from datetime import date, datetime
import time
import calendar
import sys, os
dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(dir, '.')))
sys.path.insert(0, os.path.abspath(os.path.join(dir, './model')))
sys.path.insert(0, os.path.abspath(os.path.join(dir, './doc')))
from couchdb_server import CouchDBServer
from staff_model import StaffModel
from camera_model import CameraModel
from detection_model import DetectionModel
from staff import Staff
from detection import Detection
from helper import date_to_str, datetime_to_str, str_to_date, str_to_datetime
df = pd.read_csv('/home/tainp/Downloads/staff.csv', dtype={"cellphone": str})
staff = df.where(pd.notnull(df), None)
camera = pd.read_csv('/home/tainp/Downloads/camera.csv', dtype={"floor": int})
# camera = df2.dropna(subset=['floor'])
# camera.to_csv('/home/vietph/Downloads/camera.csv', index=False)
# camera = df2.where(pd.notnull(df), None)

couch_server = CouchDBServer('localhost', '5984', 'admin', 'admin')
print(couch_server.status())
staff_db = couch_server.create_db('staff')
staff_model = StaffModel(staff_db)

camera_db = couch_server.create_db('camera')
camera_model = CameraModel(camera_db)

cams = camera_model.cameras_by_id(['e483790a629fb04842e11390762e94ac'])
for cam in cams:
    print(cam.floor, type(cam.floor))

detection_data = {'msgType':'new_detection', 'ip':'172.21.105.105',
                    'detectionPath':'http://172.21.100.240:9999/analysis/1658229497728_333_0.635322.jpg',
                    'detectionTime':1658229497576, 'staffCode':'240837',
                    'confidence':0.6353216171264648, 'trackID':0, 'fullName':'Luong Van Tan'}
print(detection_data['detectionTime'], type(detection_data['detectionTime']))
print(detection_data['confidence'], type(detection_data['confidence']))
date = datetime.fromtimestamp(detection_data['detectionTime'] / 1000.0)
date_str = datetime_to_str(date)
print(date, type(date), date.strftime('%s'), calendar.timegm(date.timetuple()))
print(date_str, int(time.time()*1000))
date_obj = str_to_datetime(date_str)
print(date_obj, type(date_obj))
print(date_str > '2023-06-19 18:18:18')

detection_model = DetectionModel(couch_server.create_db('detection'))
cam_doc = camera_model.mango_query(selector={'ip':detection_data['ip']}, fields=['_id'])
staff_doc = staff_model.mango_query(selector={'staff_code':detection_data['staffCode']}, fields=['_id'])
for cam in cam_doc:
    for staff in staff_doc:
        detect = {'camera_id':cam['_id'], 'staff_id':staff['_id'], 'detection_time':date,
                'detection_path':detection_data['detectionPath'], 'track_id':detection_data['trackID'],
                'landmark':[1.0, 1.0, 1.1], 'feature':[1.1 for i in range(512)],
                'milvus_score':detection_data['confidence']}
        detection_obj = Detection(detect)
        print(detection_obj.staff_id, detection_obj.camera_id, type(detection_obj.feature[0]))
        detection_obj.save(detection_model.db)
detect_obj = detection_model.detections_by_id(['e483790a629fb04842e1139076317f80'])
print(detect_obj[0]._id, detect_obj[0].feature[0], type(detect_obj[0].feature[0]))

# staff_model.update_doc({'staff_code': '122502', 'full_name': 'Nguyễn Văn Tuyển', 'mail_code': 'tuyennv8', 'cellphone': '0972893298', 'unit': 'Khối phòng ban quản lý, hỗ trợ - Viện HKVT', 'department': 'Phòng Công nghệ thông tin', 'date_of_birth': '1988-07-31', 'sex': 'Nam', 'title': 'Kỹ sư nghiên cứu ATTT', 'note': 'quitted', 'should_roll_up': None, 'active': False})
# for index, row in staff.iterrows():
#     data = {'staff_code':row['staff_code'], 'full_name':row['full_name'], 'mail_code':row['mail_code'],
#             'cellphone':row['cellphone'], 'unit':row['unit'], 'department':row['department'],
#             'date_of_birth':row['date_of_birth'], 'sex':row['sex'], 'title':row['title'],
#             'note':row['note'], 'should_roll_up':row['should_diemdanh'], 'active':row['activate']}
#     print(data)
#     staff_model.update_doc(data)
    
# for index, row in camera.iterrows():
#     if(pd.isna(row['nvr']) ==  True):
#         nvr = None
#     else:
#         nvr = row['nvr']
#     data = {'ip':row['ip'], 'mac':row['mac'], 'description':row['description'],
#             'floor':row['floor'], 'nvr':nvr}
#     print(data)
#     camera_model.update_doc(data)