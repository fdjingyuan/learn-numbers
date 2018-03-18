#!/usr/bin/python
# -*- coding: utf-8 -*-
# Import the modules
import cv2
from sklearn.externals import joblib
from skimage.feature import hog
import numpy as np
import argparse as ap
import base64
import os
from collections import namedtuple
import uuid
import shutil

# Load the classifier
dirname = os.path.dirname(__file__)
clf_path = os.path.join(os.path.dirname(__file__), 'digits_cls.pkl')

Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')


def rect_overlap_rate(rect1, rect2):
    # rect: [宽起点，高起点，宽，高]
    ra = Rectangle(rect1[0], rect1[1], rect1[0] + rect1[2], rect1[1] + rect1[3])
    rb = Rectangle(rect2[0], rect2[1], rect2[0] + rect2[2], rect2[1] + rect2[3])
    dx = min(ra.xmax, rb.xmax) - max(ra.xmin, rb.xmin)
    dy = min(ra.ymax, rb.ymax) - max(ra.ymin, rb.ymin)
    if (dx >= 0) and (dy >= 0):
        i = dx * dy
    else:
        i = 0
    overa = float(i) / ((ra.ymax - ra.ymin) * (ra.xmax - ra.xmin))
    overb = float(i) / ((rb.ymax - rb.ymin) * (rb.xmax - rb.xmin))
    if overa > overb:
        return overa
    else:
        return overb


def convert_alpha(im):
    a = im[:, :, 3]
    new_im = np.zeros((im.shape[0], im.shape[1], 3), dtype=np.uint8)
    new_im[:, :, 0] = new_im[:, :, 1] = new_im[:, :, 2] = a
    new_im = 255 - new_im
    return new_im


def predict(base64_data):
    clf, pp = joblib.load(clf_path)

    byte = base64.b64decode(base64_data)
    tmp_image = str(uuid.uuid1()) + '.png'
    with open(tmp_image, 'wb') as f:
        f.write(byte)
    im = cv2.imread(tmp_image, cv2.IMREAD_UNCHANGED)
    os.remove(tmp_image)
    # npimg = np.fromstring(img, dtype=np.uint8)
    # im = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)

    im = convert_alpha(im)
    print(im.shape)
    print(im.sum())
    cv2.imwrite(os.path.join(dirname, 'im.jpg'), im)

    # padding
    white_im = np.zeros((600, 1200, 3), dtype=np.uint8)
    white_im.fill(255)
    new_w = int(im.shape[1] * float(300) / im.shape[0])
    im_resized = cv2.resize(im, (new_w, 300))
    white_im[150: 450, int(1200 / 2 - new_w // 2): int(1200 / 2 - new_w // 2 + new_w)] = im_resized
    im = white_im

    # Convert to grayscale and apply Gaussian filtering
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)
    cv2.imwrite(os.path.join(dirname, 'img/im_gray.jpg'), im_gray)

    # Threshold the image
    ret, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)
    # cv2.imwrite('img/im_th.jpg', im_gray)

    # Find contours in the image
    image, ctrs, _ = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # , hie

    tmp_image = image.copy()
    cv2.drawContours(tmp_image, ctrs, -1, (0, 0, 255), 3)
    # cv2.imwrite('img/tmp_image.jpg', tmp_image)

    # Get rectangles contains each contour
    rects = [cv2.boundingRect(ctr) for ctr in ctrs]
    rects = sorted(rects, key=lambda x: x[0])

    new_rects = []
    for rect in rects:
        ok = True
        for rect_already in new_rects:
            if rect_overlap_rate(rect, rect_already) >= 0.3:
                print(rect_overlap_rate(rect, rect_already))
                ok = False
                break
        if ok:
            new_rects.append(rect)
    rects = new_rects
    # For each rectangular region, calculate HOG features and predict
    # the digit using Linear SVM.
    res = 0
    for i, rect in enumerate(rects):
        # Draw the rectangles
        # rect: [宽起点，高起点，宽，高]
        cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3)
        # Make the rectangular region around the digit
        if rect[2] > rect[3]:
            max_leng = rect[2]
        else:
            max_leng = rect[3]
        leng = int(max_leng * 1.2)
        pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
        pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
        roi = im_th[pt1:pt1 + leng, pt2:pt2 + leng]
        cv2.imwrite(os.path.join(dirname, 'roi{}.jpg'.format(i)), roi)
        print(os.path.join(dirname, 'roi{}.jpg'.format(i)))
        # Resize the image
        roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
        roi = cv2.dilate(roi, (3, 3))
        # Calculate the HOG features
        roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
        roi_hog_fd = pp.transform(np.array([roi_hog_fd], 'float64'))
        nbr = clf.predict(roi_hog_fd)
        # print(int(nbr[0]))
        res = res * 10 + nbr
    # cv2.imwrite('im_rect.jpg', im)
    return res[0]
# cv2.namedWindow("Resulting Image with Rectangular ROIs", cv2.WINDOW_NORMAL)
# cv2.imshow("Resulting Image with Rectangular ROIs", im)
# cv2.waitKey()


if __name__ == '__main__':
    image_p = 'photo_1.jpg'
    with open(image_p, 'rb') as f:
        image_data = f.read()
        base64_data = base64.b64encode(image_data)
        print(predict(base64_data))
