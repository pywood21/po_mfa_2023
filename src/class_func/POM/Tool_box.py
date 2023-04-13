#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import cv2


# In[ ]:


def create_folder(path, folder_name):
    folder_path=os.path.join(path, folder_name)
    
    if os.path.exists(folder_path)==False:
        os.makedirs(folder_path)


# In[ ]:


def find_target(image_path, extension=".tif"):
    image_path_list=[]
    for root, dirs, files in os.walk(os.path.join(image_path)):
        if (len(files)>0):
            files=[i for i in files if extension in i]
            image_path_extract=[os.path.join(root, files[i]) for i in range(len(files))]
            image_path_list.append(image_path_extract)
        else:
            pass
    
    return image_path_list

def load_im(im_path):
    im=cv2.imread(im_path)
    im=cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    
    return im

def binarize_im(im, inv=True):
    if inv==True:
        _, im_b = cv2.threshold(im, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)
    else:
        _, im_b = cv2.threshold(im, 0, 255, cv2.THRESH_OTSU)
    
    return im_b

def resize_im(im, scaling, interpolation=cv2.INTER_NEAREST):
    im_resize = cv2.resize(im, dsize=None, fx=scaling, fy=scaling, interpolation=interpolation)
    
    return im_resize

