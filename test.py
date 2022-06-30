import sys,os
cur_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cur_path)
print("test cur_pathm = ", cur_path)
import cv2
import time

import torch
from model.detector import Detector
import utils.utils

class instancePrediction():
    def __init__(self):
        
        self.cfg, self.model, self.device, self.LABEL_NAMES = self.init_load()

    def init_load(self):
        cfg = utils.utils.load_datafile("data/coco.data")
        device = torch.device("cpu")
        model = Detector(cfg["classes"], cfg["anchor_num"], True).to(device)
        model.load_state_dict(torch.load("modelzoo/coco2017-0.241078ap-model.pth", map_location=device))
        #sets the module in eval node
        model.eval()

        #加载label names
        LABEL_NAMES = []
        with open(cfg["names"], 'r') as f:
            for line in f.readlines():
                LABEL_NAMES.append(line.strip())

        return cfg, model, device, LABEL_NAMES

    def load_img(self, img_file_path):
        #数据预处理
        ori_img = cv2.imread(img_file_path)
        res_img = cv2.resize(ori_img, (self.cfg["width"], self.cfg["height"]), interpolation = cv2.INTER_LINEAR) 
        img = res_img.reshape(1, self.cfg["height"], self.cfg["width"], 3)
        img = torch.from_numpy(img.transpose(0,3, 1, 2))
        img = img.to(self.device).float() / 255.0
        return ori_img, img

    def predict(self, img_file_path):
        ori_img, img = self.load_img(img_file_path)

        #模型推理
        start = time.perf_counter()
        preds = self.model(img)
        end = time.perf_counter()
        pred_time = (end - start) * 1000.
        #print("forward time:%fms"%pred_time)

        #特征图后处理
        output = utils.utils.handel_preds(preds, self.cfg, self.device)
        output_boxes = utils.utils.non_max_suppression(output, conf_thres = 0.3, iou_thres = 0.4, classes = 0)

        
        h, w, _ = ori_img.shape
        scale_h, scale_w = h / self.cfg["height"], w / self.cfg["width"]
        
        pos_list = []
        
        #绘制预测框
        for box in output_boxes[0]:
            box = box.tolist()
        
            obj_score = box[4]
            category = self.LABEL_NAMES[int(box[5])]

            x1, y1 = int(box[0] * scale_w), int(box[1] * scale_h)
            x2, y2 = int(box[2] * scale_w), int(box[3] * scale_h)

            x_ = int((x1+x2)/2)
            y_ = int((y1+y2)/2)

            pos_list.append((x_, y_))

            cv2.rectangle(ori_img, (x1, y1), (x2, y2), (255, 255, 0), 2)
            cv2.putText(ori_img, '%.2f' % obj_score, (x1, y1 - 5), 0, 0.7, (0, 255, 0), 2)	
            cv2.putText(ori_img, category, (x1, y1 - 25), 0, 0.7, (0, 255, 0), 2)
            cv2.circle(ori_img,(x_, y_), 4, (255, 255, 0), 2)

        #cv2.imwrite(img_file_path[:-4]+"_test_result"+img_file_path[-4:], ori_img)

        end = time.perf_counter()
        pred_time = (end - start) * 1000.
        #print("total time:%fms"%pred_time)

        return pos_list


if __name__ == '__main__':
    instance_prediction = instancePrediction()

    #img_file_path = "/img/test_2.png"
    img_file_path = os.path.join(cur_path, "img/test_2.png")
    instance_prediction.predict(img_file_path)

    
    
    
    
    

