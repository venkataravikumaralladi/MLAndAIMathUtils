# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 19:18:27 2021

@author: INVERAV
"""
'''
    Utility to convert excel sheet data to png image.
    The png image will be used to convert to super resolution image.
    
    Execute command:
        (opencv-env) C:\TechnicalABB\Hackathon2021\Ralf_Idea\implementation>
        python excel_data_to_image_converter.py
                    -i input_data\sample_data.xlsx
                    -o input_imgs\sample_data.png
                    
        Successfull execution sample output shown below:
            [INFO] loading input data from excel: input_data\sample_data.xlsx
            [INFO] input data shape w: 32, h: 32
            [INFO] output image is written successfully input_imgs\sample_data.png
        
'''

# import the necessary packages
import argparse
import pandas as pd
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to input excel sheet file in .xlsx format")
ap.add_argument("-o", "--output", required=True,
	help="path to output image we want to save input data after conversion")
args = vars(ap.parse_args())

print("[INFO] loading input data from excel: {}".format(
	args["input"]))
input_file = args["input"]

input_df = pd.read_excel(input_file, header=None)  
input_df = input_df/1000

input_numpy= input_df.to_numpy()
print("[INFO] input data shape w: {}, h: {}".format(input_df.shape[1], input_df.shape[0]))

cv2.imwrite(args["output"], input_numpy, input_df.shape)
print("[INFO] output image is written successfully {}".format(args["output"]))