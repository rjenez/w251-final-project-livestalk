# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
This is taken from and heavily modified version of detect.py from yolov5
GPL license is above as required and the documentation is below

This code is modified to act as a library call so that we can send one image
at a time and have the results returned to the caller.

Run inference on image, producing detected image.
"""

import argparse
import os
import sys
from pathlib import Path

import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn

import sys
sys.path.insert(0, ".")

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

#from models.common import DetectMultiBackend
from models.experimental import attempt_load
from utils.datasets import LoadImages, LoadStreams
from utils.general import apply_classifier, check_img_size, check_imshow, check_requirements, check_suffix, colorstr, \
    increment_path, non_max_suppression, print_args, save_one_box, scale_coords, set_logging, \
    strip_optimizer, xyxy2xywh
from utils.plots import Annotator, colors
from utils.torch_utils import load_classifier, select_device, time_sync

from utils.augmentations import letterbox

class identify:
    def __init__(
            self,
            weights=ROOT / 'yolov5s.pt',  # model.pt path(s)
            device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
            dnn=False,  # use OpenCV DNN for ONNX inference
            half=False,  # use FP16 half-precision inference
            imgsz=640,  # inference size (pixels)
            **args
    ):
        # Load model
        device = select_device(device)
        #model = DetectMultiBackend(weights, device=device, dnn=dnn)

        half &= device.type != 'cpu'  # half precision only supported on CUDA

        # Load model
        w = str(weights[0] if isinstance(weights, list) else weights)
        classify, suffix, suffixes = False, Path(w).suffix.lower(), ['.pt', '.onnx', '.tflite', '.pb', '']
        check_suffix(w, suffixes)  # check weights have acceptable suffix
        pt, onnx, tflite, pb, saved_model = (suffix == x for x in suffixes)  # backend booleans
        stride, names = 64, [f'class{i}' for i in range(1000)]  # assign defaults

        modelc=None

        # always pt
        if pt:
            model = torch.jit.load(w) if 'torchscript' in w else attempt_load(weights, map_location=device)
            stride = int(model.stride.max())  # model stride
            names = model.module.names if hasattr(model, 'module') else model.names  # get class names
            if half:
                model.half()  # to FP16
            if classify:  # second-stage classifier
                modelc = load_classifier(name='resnet50', n=2)  # initialize
                modelc.load_state_dict(torch.load('resnet50.pt', map_location=device)['model']).to(device).eval()

        self.pt = pt
        imgsz = check_img_size(imgsz, s=stride)  # check image size

        # Half
        half &= pt and device.type != 'cpu'  # half precision only supported by PyTorch on CUDA
        if pt:
            model.model.half() if half else model.model.float()

        # Run inference
        if pt and device.type != 'cpu':
            model(torch.zeros(1, 3, *imgsz).to(device).type_as(next(model.parameters())))  # run once
            
        self.model = model
        self.modelc = modelc
        self.classify = classify
        self.device = device
        self.stride = stride
        self.imgsz = imgsz
        self.names = names
        self.half = half
        self.pt = pt
    

    @torch.no_grad()
    def detect(self,
               im0s,# image to detect from
               imgsz=640,  # inference size (pixels)
               conf_thres=0.25,  # confidence threshold
               iou_thres=0.45,  # NMS IOU threshold
               max_det=1000,  # maximum detections per image
               classes=None,  # filter by class: --class 0, or --class 0 2 3
               agnostic_nms=False,  # class-agnostic NMS
               augment=False,  # augmented inference
               visualize=False,  # visualize features
               update=False,  # update all models
               line_thickness=1,  # bounding box thickness (pixels)
               hide_labels=False,  # hide labels
               hide_conf=False,  # hide confidences
               save_conf=False, # save the confidence level
               view_img=False,  # show results
               **args
    ):
        model= self.model
        modelc = self.modelc
        device = self.device
        stride = self.stride
        names = self.names
        classify = self.classify
        pt = self.pt
        half = self.half

        nparr = np.fromstring(im0s, np.uint8)
        im0s = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        #
        labels = [] #labels for image

        dt, seen = [0.0, 0.0, 0.0], 0
        # resize the image
        im = letterbox(im0s, imgsz, stride=self.stride, auto=True)[0]

        # Convert
        im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        im = np.ascontiguousarray(im)

        t1 = time_sync()
        im = torch.from_numpy(im).to(device)
        im = im.half() if half else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        t2 = time_sync()
        dt[0] += t2 - t1
                
        # Inference
        #visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
        pred = model(im, augment=augment, visualize=visualize)[0]
        
        t3 = time_sync()
        dt[1] += t3 - t2

        # NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        dt[2] += time_sync() - t3

        # Second-stage classifier (optional)
        if classify:
            pred = apply_classifier(pred, self.modelc, im, im0s)

        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1
            im0 = im0s.copy()
            s = ''

            s += '%gx%g ' % im.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            # imc = im0.copy() if save_crop else im0  # for save_crop
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))
            if len(det) == 0:
                continue
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

            # Print results
            for c in det[:, -1].unique():
                n = (det[:, -1] == c).sum()  # detections per class
                s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

            # Write results
            for *xyxy, conf, cls in reversed(det):
                xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                labels.append(('%g ' * len(line)).rstrip() % line)

                c = int(cls)  # integer class
                label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                annotator.box_label(xyxy, label, color=colors(c, True))

        # get final annotated image
        im0 = annotator.result()
        if view_img:
            cv2.imshow("image", im0)
            cv2.waitKey(1000)  # 1 millisecond

        im0 = cv2.imencode('.jpg', im0)[1].tostring()
        return im0,labels


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'yolov5s.pt', help='model path(s)')
    parser.add_argument('--source', type=str, default=ROOT / 'data/images', help='file/dir/URL/glob, 0 for webcam')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_false', help='show results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default=ROOT / 'runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    # print_args(FILE.stem, opt)
    return opt

from PIL import Image

def main(opt):
    id = identify(**vars(opt)) # weights=opt.weights, device=opt.device,dnn=opt.dnn,half=opt.half,imgsz=opt.imgsz)
    print(opt.weights)

    dataset = LoadImages(opt.source, img_size=id.imgsz, stride=id.stride, auto=id.pt)
    for path, img, im0s, vid_cap in dataset:
        im0s = cv2.imencode('.jpg', im0s)[1].tostring()
        image,labels = id.detect(im0s,**vars(opt))
        print(labels)

if __name__ == "__main__":
    opt = parse_opt()
    main(opt)


