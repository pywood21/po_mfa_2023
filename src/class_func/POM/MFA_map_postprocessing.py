#!/usr/bin/env python
# coding: utf-8

# 2022/01/08
# 
# This code contains class fucntions for postprocessing of MFA and azimuthal angle map.
# Azimuthal angle map can be drawn as a vector-field like map.


#import libraries
import numpy as np
import numpy.ma as ma
import math
import cv2
from tqdm import tqdm
from skimage.filters import threshold_otsu


#Below class contains two functions.
#The former is for calculating difference of azimuthal angle and rotation angle of CCD camera.
#This function finely works in softwood specimens.
#If CCD camera is optimally set, it is no need to use this function.
#The latter is for drawing vector-filed like map.


class azimuthal_map_drawing:
    def __init__(self, azimuth_im):
        self.azimuth_im=azimuth_im #set azimuthal angle map beforehand
        
    
    def get_mean_rotation_angle(self, azimuth_target, azimuth_interval,  
                                rho=1, theta=np.pi/360, threshold=255, minLineLength=100, maxLineGap=5):
        
        #cellwall selection by azimuthal angle region you set
        angle_select_map=np.where(np.logical_and(self.azimuth_im > azimuth_target-azimuth_interval, 
                                    self.azimuth_im < azimuth_target+azimuth_interval), 255, 0)
                                  
        #cellwall detected by hough line detection (implemented by opencv2 library)
        #please optimize hyperparameters depending on your image (especially, resolution)
        lines = cv2.HoughLinesP(np.uint8(angle_select_map), rho=rho, theta=theta, threshold=threshold, 
                                minLineLength=minLineLength, maxLineGap=maxLineGap)
        
        #get their mean values
        #get line inclination angle defined by image dimension
        angle_lines=[np.arctan2(lines[i][0][3]-lines[i][0][1], lines[i][0][2]-lines[i][0][0])*180/np.pi for i in range(len(lines))]
        angle_lines=list(map(lambda x: x if x > 0 else 180+x, angle_lines))
        
        #get mean angle
        angle_lines_mean=np.asarray(angle_lines).mean()
        
        #get the angle difference between azimuth angle on azimuth map and angle defined by x & y-directions on image
        rotation_angle=angle_lines_mean-azimuth_target
                                  
        return rotation_angle

                                  
    def draw_azimuth_vector_map(self, rotation_angle, stride, step, radius, line_thickness, color, *bg_map):
        
        #set bachground
        #if you have a background image, you can selectively get azimuthal angle info from original image
        if len(bg_map)>0:
            #binarization                          
            threshold = threshold_otsu(bg_map[0])
            bg_binary=np.where(bg_map[0]<threshold, 255, 0) #255: lumen, 0: cellwall
            bg_binary=np.uint8(bg_binary)

            bg_mask=np.where(bg_binary==0, 0, 1)
            target_im=ma.masked_array(self.azimuth_im, mask=bg_mask)
        
        #if yo dont have, all azimuthal angle info containig bg region is reflected.
        else:
            target_im=self.azimuth_im
        
                     
        #draw azimuthal angle map visualized as like vector field 
        height, width=self.azimuth_im.shape
        result_map=np.zeros((height, width))

        for i in tqdm(range(height//stride)):
            for j in range(width//stride):
                #get mean angle widthin kernel
                mean_angle=target_im[i*stride:(i+1)*stride, j*stride:(j+1)*stride].mean()


                #draw mean angle as a inclined bar on original image
                if mean_angle is ma.masked:
                    continue
                else:
                    #get the coordinates of the center of patch in original image
                    center_coord=[(i*stride+(i+1)*stride)//2, (j*stride+(j+1)*stride)//2]
                    
                    #get the coordinates of the center within patch
                    center=stride//2+1
                                  
                    #convert unit from degree to radian
                    mean_radian=math.radians(mean_angle)
                    rotation_radian=math.radians(rotation_angle)
                    target_radian=mean_radian+rotation_radian

                    #create temp map
                    #vector field is drawn on this map temporally
                    temp_map=np.zeros((stride, stride))
                    
                    #set visualization condition
                    if color==0: #In this case, each vector has mean azimuthal angle as color.
                        temp_map=cv2.line(temp_map, (center, center), 
                                      (center+np.int(radius*np.cos(target_radian)), center+np.int(radius*np.sin(target_radian))), 
                                      color=mean_angle, thickness=line_thickness, lineType=cv2.LINE_AA)
                    else: #In this case, each vector has constant value as color, 255.
                        temp_map=cv2.line(temp_map, (center, center), 
                                      (center+np.int(radius*np.cos(target_radian)), center+np.int(radius*np.sin(target_radian))), 
                                      color=color, thickness=line_thickness, lineType=cv2.LINE_AA)


                    #temporary result is reflected on the final result map
                    result_map[center_coord[0]-stride//2:center_coord[0]+stride//2+1, 
                               center_coord[1]-stride//2:center_coord[1]+stride//2+1]=temp_map

        return result_map
                                  

