#!/usr/bin/env python
# coding: utf-8

# In[1]:
#These functions are for image segmentation by using classical algorithm, watershed segmentation and image pre and postprocessing.

import numpy as np
import os, sys
import copy
import cv2
import mahotas as mh
from skimage.measure import label
from tqdm import tqdm
from skimage.morphology import opening, closing
from skimage.morphology import disk
from skimage.filters import threshold_otsu, threshold_triangle, threshold_yen, threshold_mean, threshold_minimum, threshold_li, threshold_isodata
import itertools


# In[ ]:


class watershed_preprocessing:
    
    @staticmethod
    def labels_selection_by_area(image, area):
        #labeling by connected components
        _, labels, stats, _ = cv2.connectedComponentsWithStats(np.uint8(image))
        
        #extract labels to be omitted
        label_drop=[i for i in range(len(stats)) if stats[i][4]<area]
        
        return labels, label_drop
    
    @staticmethod
    def labels_selection_by_area_and_aspect_ratio(image, area_1, area_2, aspect_ratio):
        #labeling by connected components
        _, labels, stats, _ = cv2.connectedComponentsWithStats(image)

        #extract labels to be omitted
        label_drop_1=[i for i in range(len(stats)) if stats[i][4]<area_1 and stats[i][3]/stats[i][2]<aspect_ratio]
        label_drop_2=[i for i in range(len(stats)) if stats[i][4]<area_2]
        label_drop=list(set(list(itertools.chain(label_drop_1, label_drop_2))))
        
        return labels, label_drop
    
    @staticmethod
    def labels_selection_by_area_or_aspect_ratio(image, area, aspect_ratio):
        #labeling by connected components
        _, labels, stats, _ = cv2.connectedComponentsWithStats(image)

        #some componnents are droped by restriction on area and aspect ratio
        label_drop_1=[i for i in range(len(stats)) if stats[i][4]<area]
        label_drop_2=[i for i in range(len(stats)) if stats[i][3]/stats[i][2]>aspect_ratio]
        label_drop=list(set(list(itertools.chain(label_drop_1, label_drop_2))))
        
        return labels, label_drop
        
    
    def omit_by_area(self, image, area, inversion="True"):
        #define image dimension
        height, width=image.shape
        
        if inversion=="True":
            #positive negative inversion
            image=cv2.bitwise_not(image)
        
        labels, label_drop=watershed_preprocessing.labels_selection_by_area(image, area)
        labels=labels.flatten()
        
        #pixels assigned to label_drop_lumen are set to 0 
        for i in tqdm(range(len(label_drop))):
            label_drop_ind=np.where(labels==label_drop[i])
            labels[label_drop_ind]=0
        
        labels=labels.reshape(height, width)
        labels=np.where(labels>0, 255, 0)
        
        return labels
    
    
    def omit_by_area_aspect_ratio(self, image, area_1, area_2, aspect_ratio, inversion="True"):
        #define image dimension
        height, width=image.shape
        
        if inversion=="True":
            #positive negative inversion
            image=cv2.bitwise_not(np.uint8(image))

        labels, label_drop=watershed_preprocessing.labels_selection_by_area_and_aspect_ratio(image, area_1, area_2, aspect_ratio)
        labels=labels.flatten()
        
        for i in tqdm(range(len(label_drop))):
            label_drop_ind=np.where(labels==label_drop[i])
            labels[label_drop_ind]=0
        
        labels=labels.reshape(height, width)
        labels=np.where(labels>0, 255, 0)
  
        return labels
    
    
    def ray_extraction(self, image, kernel, iterations, area, aspect_ratio):
        #small regions coming from intermediate layer are omitted by morphological operator 
        height, width=image.shape
        
        kernel = np.ones(kernel ,np.uint8)
        erosion = cv2.erode(np.uint8(image), kernel, iterations = iterations)
        
        labels, label_drop=watershed_preprocessing.labels_selection_by_area_or_aspect_ratio(erosion, area, aspect_ratio)
        labels=labels.flatten()
        
        for i in tqdm(range(len(label_drop))):
            label_drop_ind=np.where(labels==label_drop[i])
            labels[label_drop_ind]=0
        
        label_map=np.where(labels.reshape(height, width)>0, 255, 0)
        gradient = cv2.morphologyEx(np.uint8(label_map), cv2.MORPH_GRADIENT, kernel)
        ray_region=np.where(label_map-gradient>200, 255, 0)
        
        return ray_region
    
    

class watershed:
    
    @staticmethod   
    def watershed_segmentation(image):
        
        locmax=mh.regmax(image)
        seeds, nr_nuclei = mh.label(locmax)

        #distans transformation
        T = mh.thresholding.otsu(np.uint8(image))
        dist = mh.distance(np.uint8(image) > T)
        dist = dist.max() - dist
        dist -= dist.min()
        dist = dist/float(dist.ptp()) * 255
        dist = dist.astype(np.uint8)
        
        nuclei, lines = mh.cwatershed(dist, seeds, return_lines=True)
        
        return nuclei, lines

    
class watershed_postprocessing:
    
    @staticmethod
    def boundary_overlay(original_image, boundary_image, kernel):
        im_dim=len(original_image.shape)
        
        if im_dim==2:
            height, width=original_image.shape
        if im_dim==3:
            height, width, channel=original_image.shape
        
        #blur boundary lines for good visualization
        blur = cv2.GaussianBlur(boundary_image, kernel, 0)
        blur = np.where(blur[:,:]>0, 255, 0)
        
        if im_dim==2:
            im_copy=np.zeros((height, width))
            im_copy[:,:]=original_image
            im_copy[np.where(blur[:,:]==255)]=[255, 0, 0]
            
            return im_copy
        
        if im_dim==3:
            im_copy=np.zeros((height, width, channel), np.uint8)
            im_copy[:,:, :]=original_image
            im_copy[np.where(blur[:,:]==255)]=[255, 0, 0]
            
            return im_copy
        
        else:
            print("Image dimension is invalid")
            
    @staticmethod
    def save_overlay_im(boundary_image, original_image, save_path, save_name):
        
        if len(boundary_image.shape)>2:
            print("Image dimension is invalid")
            return boundary_image
        
        else:
            boundary_image_tr=np.zeros((boundary_image.shape[0], boundary_image.shape[1], 4), np.uint8)
            boundary_image_tr[:,:,2]=boundary_image
            boundary_image_tr[:,:,3] = np.where(np.all(boundary_image_tr == 0, axis=-1), 0, 255) 

            #set save path
            if os.path.exists(save_path)==False:
                os.makedirs(save_path)

            cv2.imwrite(os.path.join(save_path, 'boundary_for_mannual_correction_'+str(save_name)+'.png'), boundary_image_tr)
            cv2.imwrite(os.path.join(save_path, 'ground_im_for_manual_correction_'+str(save_name)+'.png'), original_image)
        