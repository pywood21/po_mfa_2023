from __future__ import print_function
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os
import glob
import skimage.io as io
import skimage.transform as trans
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import random
import tensorflow as tf

def adjustData(img,mask):
    img = img
    mask[mask > 0.5] = 1
    mask[mask <= 0.5] = 0
    return (img,mask)

def geneNpy(image_path,mask_path):
    images = []
    masks = [] 
    for directory_path in glob.glob(image_path):
        for img_path in glob.glob(os.path.join(directory_path, "*.png")):
            img = Image.open(img_path).convert("L")
            #img = cv2.imread(img_path, -1)
            img = np.array(img)
            img = img/255
            img = np.reshape(img,img.shape + (1,))
            images.append(img)
    
    for directory_path in glob.glob(mask_path):
        for mask_path in glob.glob(os.path.join(directory_path, "*.png")):
            mask = Image.open(mask_path).convert("L")
            #mask = cv2.imread(mask_path, -1)
            mask = np.array(mask)
            mask = mask/255
            mask[mask > 0.5] = 1
            mask[mask <= 0.5] = 0
            mask = np.reshape(mask,mask.shape + (1,))
            masks.append(mask)
    
    images_Npy = np.asarray(images)
    masks_Npy = np.asarray(masks)    
    
    return images_Npy, masks_Npy

def trainGenerator(batch_size,image_path,mask_path, aug_dict):
    imgs, masks = geneNpy(image_path, mask_path)
    
    image_datagen = ImageDataGenerator(**aug_dict)
    mask_datagen = ImageDataGenerator(**aug_dict)
    
    seed = 1
    image_generator = image_datagen.flow(imgs, batch_size=batch_size, seed=seed)
    mask_generator = mask_datagen.flow(masks, batch_size=batch_size, seed=seed)
    
    train_generator = zip(image_generator, mask_generator)
    
    for (img,mask) in train_generator:
        img,mask = adjustData(img,mask)
        yield (img,mask)

        
def testGenerator_path(test_path, target_size = (512, 512)):
    #im_path=glob.glob(os.path.join(test_path, "*.png"))
    #selected_im_path=random.sample(im_path, num_image)
    
    for i in test_path:
        img = Image.open(os.path.join(i))
        img = np.array(img.convert('L'))
        img = img / 255
        img = trans.resize(img,target_size)
        img = np.reshape(img,img.shape+(1,))
        img = np.reshape(img,(1,)+img.shape)
        yield img
    
def testGenerator_im(test_image, target_size = (512, 512)):
    #im_path=glob.glob(os.path.join(test_path, "*.png"))
    #selected_im_path=random.sample(im_path, num_image)
    
    for img in test_image:
        #img = Image.open(os.path.join(i))
        #img = np.array(img.convert('L'))
        img = img / 255
        img = trans.resize(img,target_size)
        img = np.reshape(img,img.shape+(1,))
        img = np.reshape(img,(1,)+img.shape)
        yield img
    