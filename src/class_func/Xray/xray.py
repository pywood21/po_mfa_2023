from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import cv2
from tqdm import tqdm
import pandas as pd

def polar_projection(img):
    value = np.sqrt(((img.shape[0]/2.0)**2.0)+((img.shape[1]/2.0)**2.0))
    polar_image = cv2.linearPolar(img,(img.shape[1]/2, img.shape[0]/2), value, cv2.WARP_FILL_OUTLIERS)
    polar = polar_image.astype(np.uint16)
    return polar
    
def spherical_projection(img , f=1480) :
    ### 1480 was decided from the judges on the linearity in polar diagram
    ### This process done by try and error.
    rows, cols = img.shape # 0 vertical direction 1 horizontal
    #cols = img.shape[1] #horizontal direction
    center_x = int(cols / 2) # horizontal center
    center_y = int(rows / 2) # vertical center
    phi_max=math.atan(rows/(2*f))
    rows_p=int(f*phi_max)
    sphere = np.zeros((rows_p*2,cols))
    center_w=int(cols/2)  # horizontal center x
    center_v= rows_p   # vertical center y

    for  y in tqdm(range(rows_p*2)):
        #phi = math.atan((y- center_v)/ f)
        dy, point_y =math.modf( f*math.tan((y-center_v)/f)+ center_y)  # this function takes integer and 
        for x in range(cols):
            point_x = x    
            #print(point_x,point_y,dy)           
            if point_x >= cols or point_x < 0 or point_y >= rows or point_y < 0:
                pass
            else:
                sphere[y, x] =(img[int(point_y), point_x] *(1-dy)+img[int(point_y)+1, point_x] *dy)  # 
    return sphere