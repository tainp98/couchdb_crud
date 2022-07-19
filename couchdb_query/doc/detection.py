from couchdb.mapping import Document, TextField, BooleanField, DateTimeField, IntegerField, FloatField, ListField
from couchdb.http import HTTPError
from datetime import date, datetime, time
import sys, os
dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(dir, '..')))
from helper import func_info
from helper import datetime_to_str, str_to_datetime
class Detection(Document):
    _id = TextField()
    camera_id = TextField()
    staff_id = TextField()
    detection_time = DateTimeField()
    detection_path = TextField()
    track_id = IntegerField()
    bbox_x1 = FloatField()
    bbox_y1 = FloatField()
    bbox_w = FloatField()
    bbox_h = FloatField()
    landmark = ListField(FloatField)
    feature = ListField(FloatField)
    milvus_score = FloatField()
    blurry_score = FloatField()
    t_detection_time = DateTimeField()
    t_recognized_time = DateTimeField()
    has_mask = BooleanField()
    pose_yaw = FloatField()
    pose_pitch = FloatField()
    pose_roll = FloatField()
    def __init__(self, dict_data=None, _id=None, camera_id=None, staff_id=None, detection_time=None,
                 detection_path=None, track_id=None, bbox_x1=None, bbox_y1=None, bbox_w=None,
                 bbox_h=None, landmark=None, feature=None, milvus_score=None, blurry_score=None,
                 t_detection_time=None, t_recognized_time=None, has_mask=None, pose_yaw=None,
                 pose_pitch=None, pose_roll=None):
        super().__init__()
        if(dict_data != None):
            if(dict_data.get('detection_time') != None):
                if(isinstance(dict_data['detection_time'], datetime) == False):
                    f_info = func_info()
                    raise Exception(f_info[0]+' '+f_info[1]+' '+f_info[2]+" Error detection_time data type")
            if(dict_data.get('t_detection_time') != None):
                if(isinstance(dict_data['t_detection_time'], datetime) == False):
                    f_info = func_info()
                    raise Exception(f_info[0]+' '+f_info[1]+' '+f_info[2]+" Error t_detection_time data type")
            if(dict_data.get('t_recognized_time') != None):
                if(isinstance(dict_data['t_recognized_time'], datetime) == False):
                    f_info = func_info()
                    raise Exception(f_info[0]+' '+f_info[1]+' '+f_info[2]+" Error t_recognized_time data type")
            if(dict_data.get('landmark') != None):
                if(isinstance(dict_data['landmark'], list) == False):
                    f_info = func_info()
                    raise Exception(f_info[0]+' '+f_info[1]+' '+f_info[2]+" Error landmark data type")
            if(dict_data.get('feature') != None):
                if(isinstance(dict_data['feature'], list) == False):
                    f_info = func_info()
                    raise Exception(f_info[0]+' '+f_info[1]+' '+f_info[2]+" Error feature data type")
            self._id = dict_data.get('_id')
            self.camera_id = dict_data.get('camera_id')
            self.staff_id = dict_data.get('staff_id')
            self.detection_time = dict_data.get('detection_time')
            self.detection_path = dict_data.get('detection_path')
            self.track_id = dict_data.get('track_id')
            self.bbox_x1 = dict_data.get('bbox_x1')
            self.bbox_y1 = dict_data.get('bbox_y1')
            self.bbox_w = dict_data.get('bbox_w')
            self.bbox_h = dict_data.get('bbox_h')
            self.landmark = dict_data.get('landmark')
            self.feature = dict_data.get('feature')
            self.milvus_score = dict_data.get('milvus_score') 
            self.blurry_score = dict_data.get('blurry_score')
            self.t_detection_time = dict_data.get('t_detection_time')
            self.t_recognized_time = dict_data.get('t_recognized_time')
            self.has_mask = dict_data.get('has_mask')
            self.pose_yaw = dict_data.get('pose_yaw')
            self.pose_pitch = dict_data.get('pose_pitch')
            self.pose_roll = dict_data.get('pose_roll')
        else:
            if(detection_time != None):
                if(isinstance(detection_time, datetime) == False):
                    f_info = func_info()
                    raise Exception(f_info[0]+' '+f_info[1]+' '+f_info[2]+" Error detection_time data type")
            if(t_detection_time != None):
                if(isinstance(t_detection_time, datetime) == False):
                    f_info = func_info()
                    raise Exception(f_info[0]+' '+f_info[1]+' '+f_info[2]+" Error t_detection_time data type")
            if(t_recognized_time != None):
                if(isinstance(t_recognized_time, datetime) == False):
                    f_info = func_info()
                    raise Exception(f_info[0]+' '+f_info[1]+' '+f_info[2]+" Error t_recognized_time data type")
            if(landmark != None):
                if(isinstance(landmark, list) == False):
                    f_info = func_info()
                    raise Exception(f_info[0]+' '+f_info[1]+' '+f_info[2]+" Error landmark data type")
            if(feature != None):
                if(isinstance(feature, list) == False):
                    f_info = func_info()
                    raise Exception(f_info[0]+' '+f_info[1]+' '+f_info[2]+" Error feature data type")
            self._id = _id
            self.camera_id = camera_id
            self.staff_id = staff_id
            self.detection_time = detection_time
            self.detection_path = detection_path
            self.track_id = track_id
            self.bbox_x1 = bbox_x1
            self.bbox_y1 = bbox_y1
            self.bbox_w = bbox_w
            self.bbox_h = bbox_h
            self.landmark = landmark
            self.feature = feature
            self.milvus_score = milvus_score   
            self.blurry_score = blurry_score
            self.t_detection_time = t_detection_time
            self.t_recognized_time = t_recognized_time
            self.has_mask = has_mask
            self.pose_yaw = pose_yaw
            self.pose_pitch = pose_pitch
            self.pose_roll = pose_roll

    def save(self, db):
        detection = {}
        if(self._id != None):
            try:
                detection = db[self._id]
            except HTTPError as err:
                f_info = func_info()
                print('HTTPError: ', f_info[0], f_info[1], f_info[2], err)
                detection['_id'] = self._id

        detection['camera_id'] = self.camera_id
        detection['staff_id'] = self.staff_id
        detection['detection_time'] = datetime_to_str(self.detection_time)
        detection['detection_path'] = self.detection_path
        detection['track_id'] = self.track_id
        detection['bbox_x1'] = self.bbox_x1
        detection['bbox_y1'] = self.bbox_y1
        detection['bbox_w'] = self.bbox_w
        detection['bbox_h'] = self.bbox_h
        detection['landmark'] = self.landmark
        detection['feature'] = self.feature
        detection['milvus_score'] = self.milvus_score
        detection['blurry_score'] = self.blurry_score
        detection['t_detection_time'] = datetime_to_str(self.t_detection_time)
        detection['t_recognized_time'] = datetime_to_str(self.t_recognized_time)
        detection['has_mask'] = self.has_mask
        detection['pose_yaw'] = self.pose_yaw
        detection['pose_pitch'] = self.pose_pitch
        detection['pose_roll'] = self.pose_roll
        try:
            return db.update([detection])
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
            detection = db[self._id]
            self.camera_id = detection['camera_id']
            self.staff_id = detection['staff_id']
            self.detection_time = str_to_datetime(detection['detection_time'])
            self.detection_path = detection['detection_path']
            self.track_id = detection['track_id']
            self.bbox_x1 = detection['bbox_x1']
            self.bbox_y1 = detection['bbox_y1']
            self.bbox_w = detection['bbox_w']
            self.bbox_h = detection['bbox_h']
            self.landmark = detection['landmark']
            self.feature = detection['feature']
            self.milvus_score = detection['milvus_score']
            
            self.blurry_score = detection['blurry_score']
            self.t_detection_time = str_to_datetime(detection['t_detection_time'])
            self.t_recognized_time = str_to_datetime(detection['t_recognized_time'])
            self.has_mask = detection['has_mask']
            self.pose_yaw = detection['pose_yaw']
            self.pose_pitch = detection['pose_pitch']
            self.pose_roll = detection['pose_roll']
        except HTTPError as err:
            f_info = func_info()
            print('HTTPError: ', f_info[0], f_info[1], f_info[2], err)
    
    @classmethod
    def load_by_id(cls, db, id):
        try:
            detection = db[id]
            if(detection['detection_time'] != None):
                detection['detection_time'] = str_to_datetime(detection['detection_time'])
            if(detection['t_detection_time'] != None):
                detection['t_detection_time'] = str_to_datetime(detection['t_detection_time'])
            if(detection['t_recognized_time'] != None):
                detection['t_recognized_time'] = str_to_datetime(detection['t_recognized_time'])
            return cls(detection)
        except HTTPError as err:
            f_info = func_info()
            print('HTTPError: ', f_info[0], f_info[1], f_info[2], err)

    def _to_dict(self):
        json_obj = {}
        if(self._id != None):
            json_obj['_id'] = self._id
        json_obj['camera_id'] = self.camera_id
        json_obj['staff_id'] = self.staff_id
        if(self.detection_time != None):
            json_obj['detection_time'] = datetime_to_str(self.detection_time)
        json_obj['detection_path'] = self.detection_path
        json_obj['track_id'] = self.track_id
        json_obj['bbox_x1'] = self.bbox_x1
        json_obj['bbox_y1'] = self.bbox_y1
        json_obj['bbox_w'] = self.bbox_w
        json_obj['bbox_h'] = self.bbox_h
        json_obj['landmark'] = self.landmark
        json_obj['feature'] = self.feature
        json_obj['milvus_score'] = self.milvus_score
        
        json_obj['blurry_score'] = self.blurry_score
        if(self.t_detection_time != None):
            json_obj['t_detection_time'] = datetime_to_str(self.t_detection_time)
        if(self.t_recognized_time != None):
            json_obj['t_recognized_time'] = datetime_to_str(self.t_recognized_time)
        json_obj['has_mask'] = self.has_mask
        json_obj['pose_yaw'] = self.pose_yaw
        json_obj['pose_pitch'] = self.pose_pitch
        json_obj['pose_roll'] = self.pose_roll
        return json_obj
if __name__ == '__main__':
    from couchdb import Server
    from couchdb.design import ViewDefinition
    from couchdb.http import HTTPError, ResourceNotFound
    from datetime import date, datetime
    couch = Server("http://admin:admin@172.21.100.174:5984")
    # couch = Server("http://admin:admin@localhost:5984")
    try:
        db = couch.create('detection')
    except HTTPError as err:
        print(err)
        db = couch['detection']
    # detection = Detection(staff_id='277457', detection_time=datetime.now(),
    #                       feature=[1.0, 2.2, 3.33])
    detection = Detection.load_by_id(db, '8f16853e2aa2f548148b120e73beb348')
    
    print(detection._id, detection.detection_time, type(detection.feature))
    # print(detection.save(db))