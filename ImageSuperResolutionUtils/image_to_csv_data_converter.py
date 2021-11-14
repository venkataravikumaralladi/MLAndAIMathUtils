# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 19:18:27 2021

@author: INVERAV
"""
'''
    Utility to convert png image to csv file.
    The csv file can be used to compare values to original excel file input used.
    
    Execute command:
        
            (opencv-env) C:\TechnicalABB\Hackathon2021\Ralf_Idea\implementation>
                    python image_to_csv_data_converter.py
                            -i output_imgs\sr_sample_data_x3.png 
                            -o output_data\sr_sample_data_x3.csv
                            
            Successfull execution sample output shown below:
                [INFO] loading input image : output_imgs\sr_sample_data_x3.png
                [INFO] Input image converted to csv file written to : output_data\sr_sample_data_x3.csv

        
'''

# import the necessary packages
import argparse
import numpy as np
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to input image  .png format")
ap.add_argument("-o", "--output", required=True,
	help="path to output csv file we want to save input image after conversion")
args = vars(ap.parse_args())


print("[INFO] loading input image : {}".format(
	args["input"]))
input_image = args["input"]
pd_from_img = cv2.imread(input_image, cv2.IMREAD_GRAYSCALE)

# Saving the array
np.savetxt(args["output"], pd_from_img, delimiter=",")

print("[INFO] Input image converted to csv file written to : {}".format(
	args["output"]))