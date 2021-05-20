# -*- coding: utf-8 -*-

# Author: Venkata Ravi Kumar
# File name: image_rotation_utils.py
# Reference: https://www.pyimagesearch.com/2021/01/20/opencv-rotate-image/
#            https://towardsdatascience.com/transformations-with-opencv-ff9a7bea7f8b
#            https://theailearner.com/tag/cv2-getrotationmatrix2d/
# Notes:
#      Following functionality is implemented in Albumentations library.
#         https://pypi.org/project/albumentations/
#         Implemented as part of study project for data augumentation for image training.
#          and can be used for light weight projects.

''' This module provides utilities for image rotation '''


# imports section.

import os
import pathlib
import csv
import numpy as np
import cv2



class ImageRotationUtils:
    """ 
        Utils for rotating images and bounding box in image updates after rotation.
        Bounding box specifications should specify in following format.
        [x_min, y_min, width, height]. Here (xmin, ymin) top left corner of bounding box.
        Bounding box annotations after rotation are specified in following format
        [x_new_min, y_new_min, x_new_max, y_new_max]. 
        Rotated bounding boxes are no longer rectangle and are polygons. so corners
        of polygons are stored as part of annotations file.
    """
    
    def __init__(self, image_path=None, image_name=None, output_path=None, output_annotations_file=None ):
        """ Initializes the class.
        Args:
            image_path: the relative path to the image
            image_name: image file name
            output_path: the relative path where rotated output file is stored.
            output_annotations_file: annotations file where rotated anotations are stored.
        """
        self.image_path = image_path
        self.image_name = image_name
        self.output_path = output_path
        self.output_annotations_file = output_annotations_file
        return
                
    
    def rotate_image_angle(self, angle_degrees, scale_factor, bboxes=None, bboxes_class=None):
        """ Rotates image angle_degrees in anticlockwise with provided scale factor
            from center of the input image.
            e.g., 45 value rotates image 45 degrees anti-clockwise.
            e.g., -45 value rotates image 45 degrees anti-clockwise
            
        Args:
            angle_degrees: angle in degrees image to be rotated.
            scale_factor: scacling factor of image. (Isotropic scale factor.)
            bboxes: bounding box list.
        Returns:
            True if rotation is sucessful and result is saved, False otherwise.
        """
        
        img_path = os.path.join(f'{self.image_path}',self.image_name)# read image
        image_read = cv2.imread(img_path, cv2.IMREAD_COLOR)
        
        (height, width) = image_read.shape[:2]
        (cX, cY) = (width / 2, height / 2) # rotate the image from center
        self.angle = angle_degrees
        self.scale_factor = scale_factor
        
        # grab the rotation matrix (applying the negative of the
        # angle to rotate clockwise), then grab the sine and cosine
        # (i.e., the rotation components of the matrix).
        self.rotated_transform_M = cv2.getRotationMatrix2D((cX, cY), angle_degrees, scale_factor)
        
        cos = np.abs(self.rotated_transform_M[0, 0])
        sin = np.abs(self.rotated_transform_M[0, 1])

        # compute the new bounding dimensions of the image
        rotated_nW = int((height * sin) + (width * cos))
        rotated_nH = int((height * cos) + (width * sin))

        # adjust the rotation matrix to take into account translation
        self.rotated_transform_M[0, 2] += (rotated_nW / 2) - cX
        self.rotated_transform_M[1, 2] += (rotated_nH / 2) - cY

        # perform the actual rotation and return the image
        self.rotated_img = cv2.warpAffine(image_read, self.rotated_transform_M, (rotated_nW, rotated_nH))
        (new_height, new_width) = self.rotated_img.shape[:2]
                
        #save the rotated image
        self.output_file_name = self.image_name + 'rotate' + str(self.angle) + '.png'
        self.output_img_path = os.path.join(f'{self.output_path}', self.output_file_name)
        if (cv2.imwrite(self.output_img_path, self.rotated_img)):
            print('Image ', self.output_img_path, ' saved successfully.')
        else:
            print('Image ', self.output_img_path, ' not saved *Failed!.')
        
        if(bboxes != None): 
            self.new_bounding_boxes = []
            self.new_bboxes = self._rotate_boundingbox(bboxes, cX, cY, height, width, bboxes_class)
            
        return (True, self.rotated_img, self.new_bounding_boxes)
    
    
    def _rotate_boundingbox(self, bb, cx, cy, h, w, bboxes_class):
        """ Private function rotoates bounding box in image from center of the input image.
           
        Args:
            bb: list of bounding boxes. Each bounding box is [X, Y, W, H].
            cx: x cooridnate for center of original image.
            cy: y coordinate for center of original image.
            h: height of original image.
            w: width of original image.
            bboxes_class: class representing bounding box.
        Returns:
            new bounding boxe polygons according to rotation.
        """
        
        bboxid = 0       
        for bounding_box in bb:
            # get four corners of bounding box [X, Y, W, H]
            X = bounding_box[0]
            Y = bounding_box[1]
            W = bounding_box[2]
            H = bounding_box[3]
            right_top_corner    = (X+H, Y)
            right_bottom_corner = (X+W, Y+H)
            left_top_corner     = (X, Y)
            left_bottom_corner  = (X, Y+H)
            class_type = bboxes_class[bboxid]
        
            bb_corners = [left_top_corner, left_bottom_corner,  right_bottom_corner, right_top_corner]
            new_bb = bb_corners
            for i,coord in enumerate(new_bb):
                # opencv calculates standard transformation matrix
                M = cv2.getRotationMatrix2D((cx, cy), self.angle, self.scale_factor)
                # Grab  the rotation components of the matrix)
                cos = np.abs(M[0, 0])
                sin = np.abs(M[0, 1])
                # compute the new bounding dimensions of the image
                nW = int((h * sin) + (w * cos))
                nH = int((h * cos) + (w * sin))
                # adjust the rotation matrix to take into account translation
                M[0, 2] += (nW / 2) - cx
                M[1, 2] += (nH / 2) - cy
                # Prepare the vector to be transformed
                v = [coord[0],coord[1],1]
                # Perform the actual rotation and return the image
                calculated = np.dot(M,v)
                new_bb[i] = (calculated[0],calculated[1])
                
            # save new bounding box to annotation file.
            bboxid = bboxid + 1
            self._save_annotations_rotated_image(np.array(new_bb), class_type)
            
        return np.array(new_bb)
    

    def _save_annotations_rotated_image(self, new_rotated_corners, class_type):
        """ Private function to save annotations of bounding box in file.
        Args:
            new_rotated_corners: new rotation corners
            class_type: class representing bounding box.
        Returns:
            none.
        """
        
        # fill values for return result.
        self.new_bounding_boxes.append(new_rotated_corners)
         
        # For rotation images bounding boxes are no longer rectangle as we have
        # polygons after rotations so we store corners of polygons
        file = pathlib.Path(self.output_annotations_file)
        openannotationfile = None
        writer = None
        if file.exists ():
            openannotationfile = open(self.output_annotations_file, 'a', newline='')
            writer = csv.writer(openannotationfile)                
        else:
            openannotationfile = open(self.output_annotations_file, 'a+', newline='')
            writer = csv.writer(openannotationfile)
            # left_top_corner_X, left_top_corner_Y, left_bottom_corner_X,  left_bottom_corner_Y
            # right_bottom_corner_X,  right_bottom_corner_Y, right_top_corner_X, right_top_corner_Y]
            writer.writerow(["image_id", "poly_left_top_corner_X", "poly_left_top_corner_Y",
                             "poly_left_bottom_corner_X", "poly_left_bottom_corner_Y",
                             "poly_right_bottom_corner_X", "poly_right_bottom_corner_Y",
                             "poly_right_top_corner_X", "poly_right_top_corner_Y", 'class'])
       
        writer.writerow([self.output_file_name, new_rotated_corners[0][0], new_rotated_corners[0][1],
                                                new_rotated_corners[1][0], new_rotated_corners[1][1],
                                                new_rotated_corners[2][0], new_rotated_corners[2][1],
                                                new_rotated_corners[3][0], new_rotated_corners[3][1],
                                                class_type])
        openannotationfile.close()
             
        return
    
    def __str__(self):
        """ String out put function for object which will be callled for print object for debugging.
         Args:
            None
        Returns:
            string to be printed.
        """
        return 'input image'

if __name__ == "__main__":
    
    img_rot = ImageRotationUtils()
    print('img rot is ' , img_rot)

