import os
from skimage import io, transform
import torch
import torchvision
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

import numpy as np
from PIL import Image
import glob
import cv2

from data_loader import RescaleT
from data_loader import ToTensor
from data_loader import ToTensorLab
from data_loader import SalObjDataset

from model import U2NET # full size version 173.6 MB
from model import U2NETP # small version u2net 4.7 MB

# normalize the predicted SOD probability map
def normalize(d):
    ma = torch.max(d)
    mi = torch.min(d)

    dn = (d-mi)/(ma-mi)

    return dn

def main():

    model_name='u2net'  # u2netp
    model_dir = os.path.join(os.getcwd(), 'saved_models', model_name, model_name + '.pth')

    if(model_name=='u2net'):
        print("...load U2NET---173.6 MB")
        net = U2NET(3,1)
    elif(model_name=='u2netp'):
        print("...load U2NEP---4.7 MB")
        net = U2NETP(3,1)
    net.load_state_dict(torch.load(model_dir))
    if torch.cuda.is_available():
        net.cuda()
    net.eval()

    cap = cv2.VideoCapture(0)

    import time

    while True:
        ret, frame = cap.read()
        if ret:
            t0 = time.time()
            img = cv2.resize(frame, (320, 320))
            img = img.transpose((2, 0, 1))
            img = img[None,...] / 255.
            inputs_test = torch.from_numpy(img)
            inputs_test = inputs_test.type(torch.FloatTensor)

            if torch.cuda.is_available():
                inputs_test = Variable(inputs_test.cuda())
            else:
                inputs_test = Variable(inputs_test)

            d1,d2,d3,d4,d5,d6,d7= net(inputs_test)

            pred = d1[:,0,:,:]
            predict = normalize(pred)
            predict = predict.squeeze()
            predict_np = predict.cpu().data.numpy()

            h, w = frame.shape[:2]
            pred_resized = cv2.resize(predict_np, (w, h))

            img = (frame.astype(np.float32) *  np.dstack((pred_resized, pred_resized, pred_resized))).astype(np.uint8)

            cv2.imshow("out", img)
            cv2.waitKey(1)

            del d1,d2,d3,d4,d5,d6,d7

if __name__ == "__main__":
    main()
