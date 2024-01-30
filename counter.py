# coding:utf-8
import cv2
from utils.sort import *
from PyQt5.QtCore import  QThread, pyqtSignal
import predict
from config import *
from motor_movement import Serial_Motor_Control
import time 

class CounterThread(QThread):
    sin_counterResult = pyqtSignal(np.ndarray)
    sin_runningFlag = pyqtSignal(int)
    sin_videoPath = pyqtSignal(int)
    sin_countArea = pyqtSignal(dict)
    sin_done = pyqtSignal(int)

    def __init__(self, model,class_names, device):
        super(CounterThread,self).__init__()  
        self.model = model
        self.class_names = class_names
        self.device = device
        self.permission = names
        self.colorDict = color_dict
        self.cutflag = {"NO_1": False,
                    "NO_2": False,
                    "NO_3": False}
        # create instance of SORT
        self.mot_tracker = Sort(max_age=10, min_hits=2)
        self.countArea = {}
        self.running_flag = 0
        self.history = {}  #save history
        self.AreaBound = {}
        self.painting = {}
        self.Motors = Serial_Motor_Control()
        
        for item in Area_name:
            vars(self)[f"countArea['{item}']"] = None

        self.sin_runningFlag.connect(self.update_flag)
        self.sin_videoPath.connect(self.update_videoPath)
        self.sin_countArea.connect(self.update_countAreas)

        self.save_dir = "results"
        if not os.path.exists(self.save_dir): os.makedirs(self.save_dir)

    def run(self):
        cap = cv2.VideoCapture(self.videoPath)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        print("webcam fps: {}".format(fps))
        codec = cv2.VideoWriter_fourcc(*"MJPG")
        out = cv2.VideoWriter(os.path.join(self.save_dir,"output.avi"), codec, fps/25, (width, height), True)
        frame_count = 0
        for item in Area_name:
            if len(vars(self)[f"countArea['{item}']"]) > 2:
                CountArea = np.array(vars(self)[f"countArea['{item}']"])
                self.AreaBound[item] = [min(CountArea[:, 0]), min(CountArea[:, 1]), max(CountArea[:, 0]), max(CountArea[:, 1])]
                self.painting[item] = np.zeros((self.AreaBound[item][3] - self.AreaBound[item][1], self.AreaBound[item][2] - self.AreaBound[item][0]), dtype=np.uint8)
                CountArea_mini = CountArea - self.AreaBound[item][0:2]
                cv2.fillConvexPoly(self.painting[item], CountArea_mini, (1,))
        while True:
            if self.running_flag:
                ret, frame = cap.read()
                if frame_count % 25 == 0:
                    if ret:
                        # Let's clear the output serial buffer during each iteration to avoid 
                        # stacking up commands should this script run faster than the Arduino can handle.
                        self.Motors.flush_buffer()
                        a1 = time.time()
                        frame_v= self.counter(frame)
                        self.sin_counterResult.emit(frame_v)
                        out.write(frame_v)
                        a2 = time.time()
                        print(f"fps: {1 / (a2 - a1):.2f}")
                        #time.sleep(0.1)
                    else:
                        break
                frame_count += 1
                    
            else:
                break

        KalmanBoxTracker.count = 0
        cap.release()
        out.release()

        if self.running_flag:
            self.sin_done.emit(1)

    def update_flag(self,flag):
        self.running_flag = flag

    def update_videoPath(self, videoPath):
        print("Update videoPath!")
        self.videoPath = videoPath

    def update_countAreas(self, Areas):
        print("Update countAreas!")
        for item in Area_name:
            vars(self)[f"countArea['{item}']"] = Areas[f"{item}"]


    def counter(self, frame):
        
        objects = predict.yolo_prediction(self.model,self.device,frame,self.class_names) # detect all in frame
        objects = filter(lambda x: x[0] in self.permission, objects) # compare object name and permission name : filter
        objects = filter(lambda x: x[1] > 0.3,objects) # compare accracy: filter
        objects = list(objects)
        #filter out repeat bbox
        objects = filter_out_repeat(objects)

        detections = []
        for item in objects:
            detections.append([int(item[2][0] - item[2][2] / 2),
                               int(item[2][1] - item[2][3] / 2),
                               int(item[2][0] + item[2][2] / 2),
                               int(item[2][1] + item[2][3] / 2),
                               item[1]])
        track_bbs_ids = self.mot_tracker.update(np.array(detections))

        # painting lain_area
        for item in Area_name:
            if len(vars(self)[f"countArea['{item}']"]) >1:
                for i in range(len(vars(self)[f"countArea['{item}']"])):
                    cv2.line(frame, tuple(vars(self)[f"countArea['{item}']"][i]), tuple(vars(self)[f"countArea['{item}']"][(i + 1) % (len(vars(self)[f"countArea['{item}']"]))]), (100, 100, 10), 1)
                cv2.putText(frame, item, tuple(vars(self)[f"countArea['{item}']"][0]), cv2.FONT_HERSHEY_DUPLEX , 0.7, (155, 10, 200), thickness=1)

        if len(track_bbs_ids) > 0:
            for bb in track_bbs_ids:    #add all bbox to history
                id = int(bb[-1])
                objectName, point = get_objName_points(bb, objects)
                if id not in self.history.keys():  #add new id
                    self.history[id] = {}
                    self.history[id]["no_update_count"] = 0
                    self.history[id]["his"] = []
                    self.history[id]["his"].append(objectName)
                else:
                    self.history[id]["no_update_count"] = 0
                    self.history[id]["his"].append(objectName)

        cut_flag = False
        InArea = {"NO_1": False,
                    "NO_2": False,
                    "NO_3": False}
        for i, item in enumerate(track_bbs_ids):
            bb = list(map(lambda x: int(x), item))
            id = bb[-1]
            x1, y1, x2, y2 = bb[:4]
            his = self.history[id]["his"]

            result = {}
            for i in set(his):
                result[i] = his.count(i)
            res = sorted(result.items(), key=lambda d: d[1], reverse=True)
            objectName = res[0][0]
            boxColor = self.colorDict[objectName]
            for item in Area_name:
                if len(vars(self)[f"countArea['{item}']"]) > 2:
                    IsPointInArea = pointInCountArea(self.painting[item], self.AreaBound[item], [int((x1+x2)/2), int((y1+y2)/2)])
                    if IsPointInArea:
                        InArea[item] = True
                        if not self.cutflag[item]:
                            self.cutflag[item] = True
                            cut_flag = True
                        # cut_flag = True
                        cv2.rectangle(frame, (x1, y1), (x2, y2), boxColor, thickness=1)
                        cv2.putText(frame, objectName, (x1 - 1, y1 - 3), cv2.FONT_HERSHEY_DUPLEX , 0.5,
                                    boxColor,
                                    thickness=1)
        if len(track_bbs_ids) == 0:
            cv2.putText(frame, "STOP, replace the sugar cane in 10s!", (70, 70), cv2.FONT_HERSHEY_DUPLEX , 0.9,
                    (0, 0, 255),
                    thickness=2)
            self.Motors.stop()
            self.Motors.checkhome()
            time.sleep(10)
        else:
            if cut_flag:
                cv2.putText(frame, "CUT, wait for 3s", (70, 70), cv2.FONT_HERSHEY_DUPLEX , 0.9,
                        (0, 0, 255),
                        thickness=2)
                self.Motors.pause()
                self.Motors.cut()
                time.sleep(2)
            else:
                cv2.putText(frame, "MOVE", (70, 70), cv2.FONT_HERSHEY_DUPLEX , 0.9,
                        (0, 255, 0),
                        thickness=2)     
                self.Motors.move()

        for item in Area_name:
            if not InArea[item]:
                self.cutflag[item] = False
                
        removed_id_list = []
        for id in self.history.keys():    #extract id after tracking
            self.history[id]["no_update_count"] += 1
            if  self.history[id]["no_update_count"] > 5:  # if object no tracking over 5 times
                removed_id_list.append(id)

        for id in removed_id_list:
            _ = self.history.pop(id)

        return frame


def filter_out_repeat(objects):
    objects = sorted(objects,key=lambda x: x[1])
    l = len(objects)
    new_objects = []
    if l > 1:
        for i in range(l-1):
            flag = 0
            for j in range(i+1,l):
                x_i, y_i, w_i, h_i = objects[i][2]
                x_j, y_j, w_j, h_j = objects[j][2]
                box1 = [int(x_i - w_i / 2), int(y_i - h_i / 2), int(x_i + w_i / 2), int(y_i + h_i / 2)]
                box2 = [int(x_j - w_j / 2), int(y_j - h_j / 2), int(x_j + w_j / 2), int(y_j + h_j / 2)]
                if cal_iou(box1,box2) >= 0.7:
                    flag = 1
                    break
            #if no repeat
            if not flag:
                new_objects.append(objects[i])
        #add the last one
        new_objects.append(objects[-1])
    else:
        return objects

    return list(tuple(new_objects))


def cal_iou(box1,box2):
    x1 = max(box1[0],box2[0])
    y1 = max(box1[1],box2[1])
    x2 = min(box1[2],box2[2])
    y2 = min(box1[3],box2[3])
    i = max(0,(x2-x1))*max(0,(y2-y1))
    u = (box1[2]-box1[0])*(box1[3]-box1[1]) + (box2[2]-box2[0])*(box2[3]-box2[1]) -  i
    iou = float(i)/float(u)
    return iou

def get_objName_points(item,objects):
    iou_list = []
    for i,object in enumerate(objects):
        x, y, w, h = object[2]
        x1, y1, x2, y2 = int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)
        iou_list.append(cal_iou(item[:4],[x1,y1,x2,y2]))
    max_index = iou_list.index(max(iou_list))
    x, y, w, h = objects[max_index][2]
    return objects[max_index][0], (x, y)

def pointInCountArea(painting, AreaBound, point):
    h,w = painting.shape[:2]
    point = np.array(point)
    point = point - AreaBound[:2]
    if point[0] < 0 or point[1] < 0 or point[0] >= w or point[1] >= h:
        return 0
    else:
        return painting[point[1],point[0]]






