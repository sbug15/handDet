# -*- coding: utf-8 -*-

import os
from os import getcwd
from PIL import Image
import random

if not os.path.exists("bbox_posGt"):
    os.makedirs("bbox_posGt")

if not os.path.exists("yolo_posGt"):
    os.makedirs("yolo_posGt")

inputPrefix = getcwd()
inputPath = inputPrefix + "/posGt/"
outputPath = inputPrefix + "/bbox_posGt/"
yoloOutputPath = inputPrefix + "/yolo_posGt/"
imgInputPath =  inputPrefix + "/pos/"


def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

classes = ["hand"]
cls = "hand"
if cls not in classes:
    exit(0)
cls_id = classes.index(cls)
list_file = open('%s/%s_list.txt'%(inputPrefix, cls), 'w')
train_txt = open('train.txt', 'w')
test_txt = open('text.txt', 'w')

def processStr(_str):
    elem = _str.split(" ")
    return " ".join(elem[1:5])

txt_name_list = []
for (dirpath, dirnames, filenames) in sorted(os.walk("posGt/")):
    txt_name_list.extend(filenames)

random.seed(4)
random.shuffle(txt_name_list)
train_samples = int(len(txt_name_list) * 0.9)

for txt_name in txt_name_list[:train_samples]:
    img_path = imgInputPath + txt_name.split(".")[0] + ".png"    
    train_txt.write(img_path + "\n")

train_txt.close()

for txt_name in txt_name_list[train_samples:]:
    img_path = imgInputPath + txt_name.split(".")[0] + ".png"    
    test_txt.write(img_path + "\n")

test_txt.close()

for txt_name in txt_name_list:
    txt_path = inputPath + txt_name
    txt_file = open(txt_path, "r")
    lines = txt_file.read().splitlines()

    txt_outpath = outputPath + txt_name
    txt_outfile = open(txt_outpath, "w")

    yolo_txt_outputpath = yoloOutputPath + txt_name    
    yolo_txt_outfile = open(yolo_txt_outputpath, "w")
    
    img_path = imgInputPath + txt_name.split(".")[0] + ".png"
    list_file.write(img_path + "\n")
    
    txt_outfile.write('0')
    for line in lines[1:]:
        elems = line.split(" ")
        txt_outfile.write('\n')
        txt_outfile.write(" ".join(elems[1:5]))

        xmin = elems[1]
        xmax = elems[1] + elems[3]
        ymin = elems[2]
        ymax = elems[2] + elems[4]
        b = (float(xmin), float(xmax), float(ymin), float(ymax))
        im = Image.open(img_path)
        w= int(im.size[0])
        h= int(im.size[1])
        bb = convert((w,h), b)
        print " ".join([str(a) for a in bb])
        yolo_txt_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    yolo_txt_outfile.close()
    txt_outfile.close()


list_file.close()    
