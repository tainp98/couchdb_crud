import socketio
import psycopg2 as pg
import json
import logging
import logging.config
import threading
import queue
import time
from datetime import date, datetime
import sys, os
dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(dir, '.')))
# sys.path.insert(0, os.path.abspath(os.path.join(dir, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(dir, './doc')))
sys.path.insert(0, os.path.abspath(os.path.join(dir, './model')))
from couchdb_server import CouchDBServer
from staff_model import StaffModel
from camera_model import CameraModel
from detection_model import DetectionModel
from staff import Staff
from detection import Detection
from helper import datetime_to_str
QUEUE = queue.Queue(1024)

NUM_PROCESS_PACKET = 0
NUM_RECEIVED_PACKET = 0
detect_list = []

logger = logging.getLogger()
sio = socketio.Client()
connection = pg.connect(
    "host=172.21.100.254 port=5432 dbname=faceiddb user=datdaica password=postgres"
)
cur = connection.cursor()
cur.execute("SELECT ip FROM camera;")
rows = cur.fetchall()
ips = [row[0] for row in rows]
ips += ["172.21.104.127"]
connection.close()

"""Create CouchDB Database"""
couch_server = CouchDBServer('172.21.100.174', '5984', 'admin', 'admin')
print(couch_server.status())
staff_db = couch_server.create_db('staff')
staff_model = StaffModel(staff_db)

camera_db = couch_server.create_db('camera')
camera_model = CameraModel(camera_db)

detection_db = couch_server.create_db('detection')
detection_model = DetectionModel(detection_db)

received_start_time = time.time()
@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')
    
@sio.on("new detection")
def on_new_detection(data):
    """receive new detection"""
    add_detection_to_queue(data)
    

def handle_detection(data: dict) -> None:
    """handle new detection"""
    start_time = time.time()
    global detect_list
    global NUM_PROCESS_PACKET
    NUM_PROCESS_PACKET += 1
    cam_doc = camera_model.view_query('camera_design', 'by_ip', key=data['ip'])
    staff_doc = staff_model.view_query('staff_design', 'by_staffcode', key=data['staffCode'])
    search_time = (time.time()-start_time)*1000.0
    # cam_doc = camera_model.mango_query(selector={'ip':detection_data['ip']}, fields=['_id'])
    # staff_doc = staff_model.mango_query(selector={'staff_code':detection_data['staffCode']}, fields=['_id'])
    # print(len(cam_doc), len(staff_doc), cam_doc, staff_doc)
    start_time = time.time()
    for cam in cam_doc:
        for staff in staff_doc:
            detect = {'camera_id':cam['value'], 'staff_id':staff['value'], 
                      'detection_time':datetime_to_str(datetime.fromtimestamp(data['detectionTime'] / 1000.0)),
                'detection_path':data['detectionPath'], 'track_id':data['trackID'],
                'landmark':[1.0, 1.1, 1.2, 1.3], 'feature':[1.33333333 for i in range(512)], 
                'milvus_score':data['confidence']}
            # detection_obj = Detection(detect)
            # detection_obj.save(detection_model.db)
            detect_list.append(detect)
            if(len(detect_list) == 128):
                detection_model.update_docs(detect_list)
                detect_list.clear()
            # detection_model.update_doc(detect)
    update_time = (time.time() - start_time)*1000.0
    print('---------- NUM_PROCESS_PACKET = ', NUM_PROCESS_PACKET, ', Search Time = %s millis, Update Time = %s millis' % (search_time, update_time))


def add_detection_to_queue(data: dict) -> None:
    """add detection to queue for async processing"""
    try:
        global received_start_time
        QUEUE.put(data, timeout=1)
        global NUM_RECEIVED_PACKET
        NUM_RECEIVED_PACKET += 1
        # print('---------- NUM_RECEIVED_PACKET = ', NUM_RECEIVED_PACKET, ', New Dection Event Comming Time = %s seconds' % (time.time() - received_start_time))
        received_start_time = time.time()
    except queue.Full:
        logger.error("------------------------- queue is full, put timeout after 1s")
        
def keepalive():
    """send a message periodictly to the stdout to show that the application is still working"""
    this_logger = logging.getLogger('keepalive')
    while True:
        this_logger.info("queue_size = %d, packet received = %d", QUEUE.qsize(), NUM_RECEIVED_PACKET)
        time.sleep(30)

def worker():
    """the data processing thread"""
    while True:
        data = QUEUE.get()
        handle_detection(data=data)
        QUEUE.task_done()

def start():
    """to be call from main"""
    threading.Thread(target=worker).start()
    threading.Thread(target=keepalive).start()

if __name__ == '__main__':
    sio.connect('http://172.21.100.254:8080')
    s = json.dumps({"msgType": "intro", "type": "client", "role": "dev"})
    sio.emit("intro message", s)

    # have to subscribe
    for ip in ips:
        s = json.dumps({"ip": ip, "msgType": "subscribe"})
        sio.emit("subscribe", s)
    logger.info("subscribe to %s", ips)
    start()

    # sio.wait()
