# -*- coding: utf-8 -*-
"""
ROMS_Technical Task - Yohanes de Britto Hertyasta Prathama (Aki)
"""

import cv2
import json
import matplotlib.pyplot as plt
from dataclasses import dataclass

# Parameters
MODEL_FPATH = './models/ssd_mobilenet_v2_coco_2018_03_29/frozen_inference_graph.pb'
ARCH_FPATH = './models/ssd_mobilenet_v2_coco_2018_03_29/ssd_mobilenet_v2_coco_2018_03_29.pbtxt'
COCO_LABELS_FPATH = './coco_labels.json' # model is trained on MSCOCO dataset (80 classes)
CONF_THRESH = 0.55 # object detection confidence
IOU_THRESH = 0.7 #NMS confidence

# load coco labels/classes
with open(COCO_LABELS_FPATH , 'r') as f:
    coco_class_names = json.load(f)
    
@dataclass
class ModelConfig:
    scalefactor: float = 1.0
    size: tuple = (224, 224)
    mean: tuple = (0, 0, 0)
    swapRB: bool = False
    crop: bool = False
    ddepth: int = cv2.CV_32F

configs = vars(ModelConfig(size=(300, 300), swapRB=True))

for x in range(100):
    # Load image and prepare a blob which is going to be input to the model
    stringX = str(x+1)
    if x < 9:
        stringX = "000" + stringX
    elif 9 <= x < 99:
        stringX = "00" + stringX
    else:
        stringX = "0" + stringX
        
    IMG_FPATH = "./imagesJAAD/video_" + stringX + ".jpg" # or laptops.jpg
    IMG_ANNOT_FPATH = "./imagesJAAD_annot/video_" + stringX + "_annot.jpg" # or laptops.jpg
    img = cv2.imread(IMG_FPATH)
    if img is None:
        raise Exception(f'Image not found with the path provided: {IMG_FPATH}')
    
    img_height, img_width = img.shape[:2]
    blob = cv2.dnn.blobFromImage(img,
                                 scalefactor=configs['scalefactor'],
                                 size=configs['size'],
                                 mean=configs['mean'],
                                 swapRB=configs['swapRB'],
                                 crop=configs['crop'],
                                 ddepth=configs['ddepth'])
    
    # Load model
    net = cv2.dnn.readNetFromTensorflow(MODEL_FPATH, ARCH_FPATH)
    
    # Specify target device
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    
    # Run inference
    net.setInput(blob)
    detections = net.forward()
    
    def show_img(img):
        dpi = 80
        height, width, _ = img.shape
        figsize = width / float(dpi), height / float(dpi)
        
        fig = plt.figure(figsize=figsize)
        plt.axis('off')
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.show()
    
    class_names = []
    confidences = []
    boxes = []
    # iterate over each detection and plot a BB on the image
    for detect in detections[0, 0, :, :]:
        conf = detect[2]
        # show the BB only of certain confidence threshold
        if conf > CONF_THRESH:
            class_id = int(detect[1])
            class_name = coco_class_names[str(class_id)]
            left = detect[3]*img_width
            top = detect[4]*img_height
            right = detect[5]*img_width
            bottom = detect[6]*img_height
            boxes.append([left,top,right,bottom])
            class_names.append(class_name)
            confidences.append(conf)
            
    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONF_THRESH, IOU_THRESH)
    for i in indices:
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        cv2.rectangle(img, (int(left), int(top)), (int(width), int(height)), (23, 230, 210), thickness=2)
        cv2.putText(img, class_names[i], (int(left), int(top)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
        
    show_img(img)
    cv2.imwrite(IMG_ANNOT_FPATH, img)