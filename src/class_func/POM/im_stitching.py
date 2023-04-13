
import numpy as np
import copy
from module.Stitcher import Stitcher


def stitch_im_POC(reference_im_list, target_im_list, ref_padding=255, target_padding=0):
    #copy input
    reference_im_list_copy=copy.deepcopy(reference_im_list)
    target_im_list_copy=copy.deepcopy(target_im_list)
    
    #call class
    stitcher=Stitcher()
    
    #set count
    n=0
    while(True):
        if n==0:
            im_num=len(reference_im_list_copy)

            #set list for temporary result
            reference_result=[]
            target_result=[]

            while(True):
                #first image is poped put from list
                reference_image_1=reference_im_list_copy.pop(0)
                reference_image_2=reference_im_list_copy[0]
                target_image_1=target_im_list_copy.pop(0)
                target_image_2=target_im_list_copy[0]
                
                #check image dimension of your input
                target_image_dim=len(target_image_1.shape)

                #adjust image size of reference images
                reference_images=image_dimension_adj(reference_image_1, reference_image_2, padding=ref_padding, criterion="A")
                
                #adjust image size of target images depending on their dimension
                if target_image_dim==2:
                    target_images=image_dimension_adj(target_image_1, target_image_2, padding=target_padding, criterion="A")
                else:
                    target_images=image_dimension_adj_3D(target_image_1, target_image_2, padding=target_padding, criterion="A")
                
                #sttching by POC
                reference_image_stitch_temp, target_image_stitch_temp = stitcher.POC_reference_criterion(reference_images, target_images)
                
                #save result
                reference_result.append(reference_image_stitch_temp)
                target_result.append(target_image_stitch_temp)

                #if length of original image list becomes 1, break loop 
                list_len=len(reference_im_list_copy)

                if list_len==1:
                    break
            
            #add count
            n+=1
            
            #if your input corresopond to only 2 images, break loop 
            result_list_len=len(reference_result)
            if result_list_len==1:
                break
        
        #if your input is more than three images, following part will run.
        if n>0:
            #set count
            m=0

            while(True):
                #select target images to be stictched
                #first image is poped put from list
                reference_image_1=reference_result.pop(0)
                reference_image_2=reference_result[0]
                target_image_1=target_result.pop(0)
                target_image_2=target_result[0]
                
                #adjust image size of reference images
                reference_images=image_dimension_adj(reference_image_1, reference_image_2, padding=ref_padding, 
                                                           criterion="A")
                
                #adjust image size of target images depending on their dimension
                if target_image_dim==2:
                    target_images=image_dimension_adj(target_image_1, target_image_2, 
                                                        padding=target_padding, criterion="A")
                else:
                    target_images=image_dimension_adj_3D(target_image_1, target_image_2, 
                                                        padding=target_padding, criterion="A")
                    
                
                #sttching by POC
                reference_image_stitch_temp, target_image_stitch_temp=stitcher.POC_reference_criterion(reference_images, target_images)
               
                #obtained results are pushed into the list
                reference_result.append(reference_image_stitch_temp)
                target_result.append(target_image_stitch_temp)
                
                #add count
                m+=1
                
                #if image stitching is completed, break loop
                if m==(result_list_len-1):
                    reference_result=reference_result[1:]
                    target_result=target_result[1:]
                    break
            
            #add count
            n+=1
            
            #Finally, check stitching result and break loop
            result_list_len=len(reference_result)
            if result_list_len==1:
                break
    
    return reference_result[0], target_result[0]





def image_dimension_adj(imageA, imageB, padding, criterion="A", verbose=False, const=0):
    height_A, width_A=imageA.shape
    height_B, width_B=imageB.shape

    if verbose==True:
        print("criterion="+str(criterion))
    else:
        pass

    #when criterion is equal to 0, dimension of imageB is reset to that of imageA.
    #when criterion is equal to 1, dimension of imageA is reset to that of imageB.
    #when criterion is not defined, dimension of each images are adjusted to the longer height and width.
    if criterion=="A":
        imageA_=imageA
        imageB_=np.ones((height_A, width_A))*const

        if height_A>height_B:
            if width_A>width_B:
                imageB_[:height_B, :width_B]=imageB[:height_B, :width_B]
            if width_B>width_A:
                imageB_[:height_B, :width_A]=imageB[:height_B, :width_A]
                imageB_[height_B:]=padding
            else:
                imageB_[:height_B, :width_B]=imageB[:height_B, :width_B]
                imageB_[height_B:, width_B:]=padding
        if height_B>height_A:
            if width_A>width_B:
                imageB_[:height_A, :width_B]=imageB[:height_A, :width_B]
                imageB_[:, width_B:]=padding
            if width_B>width_A:
                imageB_[:height_A, :width_A]=imageB[:height_A, :width_A]
            else:
                imageB_[:height_A, :width_B]=imageB[:height_A, :width_B]
                imageB_[:, width_B:]=padding
        if height_A==height_B:
            if width_A>width_B:
                imageB_[:height_A, :width_B]=imageB[:height_A, :width_B]
                imageB_[:, width_B:]=padding
            if width_B>width_A:
                imageB_[:height_A, :width_A]=imageB[:height_A, :width_A]
            else:
                imageB_[:height_A, :width_B]=imageB[:height_A, :width_B]


    if criterion=="B":
        imageA_=np.ones((height_B, width_B))*const
        imageB_=imageB

        if height_A>height_B:
            if width_A>width_B:
                imageA_[:height_B, :width_B]=imageA[:height_B, :width_B]
            if width_B>width_A:
                imageA_[:height_B, :width_A]=imageA[:height_B, :width_A]
                imageA_[:, width_A:]=padding
            else:
                imageA_[:height_B, :width_B]=imageA[:height_B, :width_B]
        if height_B>height_A:
            if width_A>width_B:
                imageA_[:height_A, :width_B]=imageA[:height_A, :width_B]
                imageA_[height_A:]=padding
            if width_B>width_A:
                imageA_[:height_A, :width_A]=imageA[:height_A, :width_A]
                imageA_[height_A:, width_A:]=padding
            else:
                imageA_[:height_A, :width_B]=imageA[:height_A, :width_B]
                imageA_[height_A:]=padding
        if height_A==height_B:
            if width_A>width_B:
                imageA_[:height_A, :width_B]=imageA[:height_A, :width_B]
            if width_B>width_A:
                imageA_[:height_A, :width_A]=imageA[:height_A, :width_A]
                imageA_[height_A:, width_A:]=padding
            else:
                imageA_[:height_A, :width_B]=imageA[:height_A, :width_B]


    if criterion=="AB":
        #set list
        height_list=[height_A, height_B]
        width_list=[width_A, width_B]

        #max val is extracted
        height_maxind=np.argmax(height_list)
        width_maxind=np.argmax(width_list)
        height_minind=np.argmin(height_list)
        width_minind=np.argmin(width_list)

        if height_maxind==height_minind:
            if width_maxind==width_minind:
                imageA_=imageA
                imageB_=imageB
            else:
                imageA_=np.ones((height_list[height_maxind], width_list[width_maxind]))*const
                imageB_=np.ones((height_list[height_maxind], width_list[width_maxind]))*const
                imageA_[:height_A, :width_A]=imageA
                imageB_[:height_B, :width_B]=imageB
        else:
            imageA_=np.ones((height_list[height_maxind], width_list[width_maxind]))*const
            imageB_=np.ones((height_list[height_maxind], width_list[width_maxind]))*const
            imageA_[:height_A, :width_A]=imageA
            imageB_[:height_B, :width_B]=imageB


    height_A_, width_A_=imageA_.shape
    height_B_, width_B_=imageB_.shape

    #show results
    if verbose==True:
        print("imageA: height="+str(height_A)+", width="+str(width_A))
        print("imageB: height="+str(height_B)+", width="+str(width_B))
        print("After adjustment, imageA: height="+str(height_A_)+", width="+str(width_A_))
        print("After adjustment, imageB: height="+str(height_B_)+", width="+str(width_B_))
    else:
        pass

    return imageA_, imageB_


def image_dimension_adj_center(imageA, imageB, criterion="A", verbose=False, const=0):
    height_A, width_A=imageA.shape
    height_B, width_B=imageB.shape

    if verbose==True:
        print("criterion="+str(criterion))
    else:
        pass

    #when criterion is equal to 0, dimension of imageB is reset to that of imageA.
    #when criterion is equal to 1, dimension of imageA is reset to that of imageB.
    #when criterion is not defined, dimension of each images are adjusted to the longer height and width.
    if criterion=="A":
        imageA_=imageA
        imageB_=np.ones((height_A, width_A))*const
        
        center_h=np.int(height_A/2)

        if height_A>height_B:           
            if width_A>width_B:
                center_w=np.int(width_A/2)
                imageB_[center_h-np.int(height_B/2):center_h-np.int(height_B/2)+height_B, 
                        center_w-np.int(width_B/2):center_w-np.int(width_B/2)+width_B]=imageB[:height_B, :width_B]
                
            elif width_B>width_A:
                center_w=np.int(width_A/2)
                imageB_[center_h-np.int(height_B/2):center_h-np.int(height_B/2)+height_B, 
                        :width_A]=imageB[:height_B, :width_A]
                #imageB_[height_B:]=padding
                
            else:
                center_w=np.int(width_A/2)
                imageB_[center_h-np.int(height_B/2):center_h-np.int(height_B/2)+height_B, 
                        center_w-np.int(width_B/2):center_w-np.int(width_B/2)+width_B]=imageB[:height_B, :width_B]
                #imageB_[height_B:, width_B:]=padding
                
        elif height_B>height_A:
            if width_A>width_B:
                center_w=np.int(width_A/2)
                imageB_[:height_A, center_w-np.int(width_B/2):center_w-np.int(width_B/2)+width_B]=imageB[:height_A, :width_B]
                #imageB_[:, width_B:]=padding
                
            elif width_B>width_A:
                imageB_[:height_A, :width_A]=imageB[:height_A, :width_A]
                
            else:
                center_w=np.int(width_A/2)
                imageB_[:height_A, center_w-np.int(width_B/2):center_w-np.int(width_B/2)+width_B]=imageB[:height_A, :width_B]
                #imageB_[:, width_B:]=padding
                
        elif height_A==height_B:
            if width_A>width_B:
                center_w=np.int(width_A/2)
                imageB_[:height_A, center_w-np.int(width_B/2):center_w-np.int(width_B/2)+width_B]=imageB[:height_A, :width_B]
                #imageB_[:, width_B:]=padding
                
            elif width_B>width_A:
                imageB_[:height_A, :width_A]=imageB[:height_A, :width_A]
                
            else:
                center_w=np.int(width_A/2)
                imageB_[:height_A, center_w-np.int(width_B/2):center_w-np.int(width_B/2)+width_B]=imageB[:height_A, :width_B]


    elif criterion=="B":
        imageA_=np.ones((height_B, width_B))*const
        imageB_=imageB
        center_h=np.int(height_B/2)
        
        if height_A>height_B:
            if width_A>width_B:
                imageA_[:height_B, :width_B]=imageA[:height_B, :width_B]
                
            if width_B>width_A:
                center_w=np.int(width_B/2)
                imageA_[:height_B, center_w-np.int(width_A/2):center_w-np.int(width_A/2)+width_A]=imageA[:height_B, :width_A]
                #imageA_[:, width_A:]=padding
                
            else:
                imageA_[:height_B, :width_B]=imageA[:height_B, :width_B]
                
        if height_B>height_A:
            if width_A>width_B:
                imageA_[center_h-np.int(height_A/2):center_h-np.int(height_A/2)+height_A, :width_B]=imageA[:height_A, :width_B]
                #imageA_[height_A:]=padding
                
            if width_B>width_A:
                center_w=np.int(width_B/2)
                imageA_[center_h-np.int(height_A/2):center_h-np.int(height_A/2)+height_A, 
                        center_w-np.int(width_A/2):center_w-np.int(width_A/2)+width_A]=imageA[:height_A, :width_A]
                #imageA_[height_A:, width_A:]=padding
                
            else:
                imageA_[center_h-np.int(height_A/2):center_h-np.int(height_A/2)+height_A, :width_B]=imageA[:height_A, :width_B]
                #imageA_[height_A:]=padding
                
        if height_A==height_B:
            if width_A>width_B:
                imageA_[:height_A, :width_B]=imageA[:height_A, :width_B]
            if width_B>width_A:
                imageA_[:height_A, :width_A]=imageA[:height_A, :width_A]
                imageA_[height_A:, width_A:]=padding
            else:
                imageA_[:height_A, :width_B]=imageA[:height_A, :width_B]


    elif criterion=="AB":
        #set list
        height_list=[height_A, height_B]
        width_list=[width_A, width_B]

        #max val is extracted
        height_maxind=np.argmax(height_list)
        width_maxind=np.argmax(width_list)
        height_minind=np.argmin(height_list)
        width_minind=np.argmin(width_list)

        if height_maxind==height_minind:
            if width_maxind==width_minind:
                imageA_=imageA
                imageB_=imageB
            else:
                imageA_=np.random.randint(0, 255, (height_list[height_maxind], width_list[width_maxind]))
                imageB_=np.random.randint(0, 255, (height_list[height_maxind], width_list[width_maxind]))
                imageA_[:height_A, :width_A]=imageA
                imageB_[:height_B, :width_B]=imageB
        else:
            imageA_=np.random.randint(0, 255, (height_list[height_maxind], width_list[width_maxind]))
            imageB_=np.random.randint(0, 255, (height_list[height_maxind], width_list[width_maxind]))
            imageA_[:height_A, :width_A]=imageA
            imageB_[:height_B, :width_B]=imageB


    height_A_, width_A_=imageA_.shape
    height_B_, width_B_=imageB_.shape

    #show results
    if verbose==True:
        print("imageA: height="+str(height_A)+", width="+str(width_A))
        print("imageB: height="+str(height_B)+", width="+str(width_B))
        print("After adjustment, imageA: height="+str(height_A_)+", width="+str(width_A_))
        print("After adjustment, imageB: height="+str(height_B_)+", width="+str(width_B_))
    else:
        pass

    return imageA_, imageB_



def image_dimension_adj_3D(imageA, imageB, padding, criterion="A", verbose=False, const=0):
    height_A, width_A, channel_A=imageA.shape
    height_B, width_B, channel_B=imageB.shape

    if verbose==True:
        print("criterion="+str(criterion))
    else:
        pass

    #when criterion is equal to 0, dimension of imageB is reset to that of imageA.
    #when criterion is equal to 1, dimension of imageA is reset to that of imageB.
    #when criterion is not defined, dimension of each images are adjusted to the longer height and width.
    if criterion=="A":
        imageA_=imageA
        imageB_=np.ones((height_A, width_A, channel_A), np.uint8)*const

        if height_A>height_B:
            if width_A>width_B:
                imageB_[:height_B, :width_B, :]=imageB[:height_B, :width_B, :]
            if width_B>width_A:
                imageB_[:height_B, :width_A, :]=imageB[:height_B, :width_A, :]
                imageB_[height_B:, :, :]=padding
            else:
                imageB_[:height_B, :width_B, :]=imageB[:height_B, :width_B, :]
                imageB_[height_B:, width_B:, :]=padding
        if height_B>height_A:
            if width_A>width_B:
                imageB_[:height_A, :width_B, :]=imageB[:height_A, :width_B, :]
                imageB_[:, width_B:, :]=padding
            if width_B>width_A:
                imageB_[:height_A, :width_A, :]=imageB[:height_A, :width_A, :]
            else:
                imageB_[:height_A, :width_B, :]=imageB[:height_A, :width_B, :]
                imageB_[:, width_B:, :]=padding
        if height_A==height_B:
            if width_A>width_B:
                imageB_[:height_A, :width_B, :]=imageB[:height_A, :width_B, :]
                imageB_[:, width_B:, :]=padding
            if width_B>width_A:
                imageB_[:height_A, :width_A, :]=imageB[:height_A, :width_A, :]
            else:
                imageB_[:height_A, :width_B, :]=imageB[:height_A, :width_B, :]


    if criterion=="B":
        imageA_=np.ones((height_B, width_B, channel_B), np.uint8)*const
        imageB_=imageB

        if height_A>height_B:
            if width_A>width_B:
                imageA_[:height_B, :width_B, :]=imageA[:height_B, :width_B, :]
            if width_B>width_A:
                imageA_[:height_B, :width_A, :]=imageA[:height_B, :width_A, :]
                imageA_[:, width_A:, :]=padding
            else:
                imageA_[:height_B, :width_B, :]=imageA[:height_B, :width_B, :]
        if height_B>height_A:
            if width_A>width_B:
                imageA_[:height_A, :width_B, :]=imageA[:height_A, :width_B, :]
                imageA_[height_A:, :, :]=padding
            if width_B>width_A:
                imageA_[:height_A, :width_A, :]=imageA[:height_A, :width_A, :]
                imageA_[height_A:, width_A:, :]=padding
            else:
                imageA_[:height_A, :width_B, :]=imageA[:height_A, :width_B, :]
                imageA_[height_A:, :, :]=padding
        if height_A==height_B:
            if width_A>width_B:
                imageA_[:height_A, :width_B, :]=imageA[:height_A, :width_B, :]
            if width_B>width_A:
                imageA_[:height_A, :width_A, :]=imageA[:height_A, :width_A, :]
                imageA_[height_A:, width_A:, :]=padding
            else:
                imageA_[:height_A, :width_B, :]=imageA[:height_A, :width_B, :]


    if criterion=="AB":
        #set list
        height_list=[height_A, height_B]
        width_list=[width_A, width_B]

        #max val is extracted
        height_maxind=np.argmax(height_list)
        width_maxind=np.argmax(width_list)
        height_minind=np.argmin(height_list)
        width_minind=np.argmin(width_list)

        if height_maxind==height_minind:
            if width_maxind==width_minind:
                imageA_=imageA
                imageB_=imageB
            else:
                imageA_=np.ones((height_list[height_maxind], width_list[width_maxind], channel_A), np.uint8)*const
                imageB_=np.ones((height_list[height_maxind], width_list[width_maxind], channel_B), np.uint8)*const
                imageA_[:height_A, :width_A, :]=imageA
                imageB_[:height_B, :width_B, :]=imageB
        else:
            imageA_=np.ones((height_list[height_maxind], width_list[width_maxind], channel_A), np.uint8)*const
            imageB_=np.ones((height_list[height_maxind], width_list[width_maxind], channel_B), np.uint8)*const
            imageA_[:height_A, :width_A, :]=imageA
            imageB_[:height_B, :width_B, :]=imageB


    height_A_, width_A_, channel_A_=imageA_.shape
    height_B_, width_B_, channel_B_=imageB_.shape

    #show results
    if verbose==True:
        print("imageA: height="+str(height_A)+", width="+str(width_A))
        print("imageB: height="+str(height_B)+", width="+str(width_B))
        print("After adjustment, imageA: height="+str(height_A_)+", width="+str(width_A_))
        print("After adjustment, imageB: height="+str(height_B_)+", width="+str(width_B_))
    else:
        pass

    return imageA_, imageB_

