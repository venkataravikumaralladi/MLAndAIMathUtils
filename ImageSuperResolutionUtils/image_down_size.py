"""
File Created: 18th November 2021
Author: Venkata Ravi Kumar A 
-----

"""

'''
    Notes:
        This scripts down size the image according to percentage passed as
        argument to script. This can be used to generate data for training
        model. Original image acts a ground truth and resized small acts as input.
        This data can be used to train super-resolution models.
        
    Sample Run command:
        (base) C:\TechnicalABB\Hackathon2021\Ralf_Idea\implementation>
                           python image_down_size.py -i input_imgs\sample_data.png 
                                                     -r 50
                                                     -o output_imgs\
                                                         
    Sample output of successfull run of above command
    
        [INFO] Original image sample_data.png Dimensions (32, 32)
        [INFO] Resized image output_imgs\sample_data_16_16.png dimensions(16, 16)
        [INFO] Reduced image is written to output_imgs\sample_data_16_16.png
        
'''

# Import the necessary packages
import os
import argparse
import cv2


# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image")
ap.add_argument("-r", "--reduceper", required = True,
	help = "Path to the image")
ap.add_argument("-o", "--output", required = True,
        help="path to output image folder")
args = vars(ap.parse_args())

input_img_name = args["image"].split(os.path.sep)[-1].lower()
img_name_withoug_ext = input_img_name.split('.')[0]

img = cv2.imread(args["image"], cv2.IMREAD_GRAYSCALE)
 
print('[INFO] Original image {} Dimensions {} '.format(input_img_name,img.shape))
 
reduce_pecentage = int(args["reduceper"])
scale_percent = reduce_pecentage # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)

# resize image
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
output_img_name = args["output"] + img_name_withoug_ext + "_" + str(resized.shape[0]) + "_" + str(resized.shape[1]) + ".png"
print('[INFO] Resized image {} dimensions{} '.format(output_img_name, resized.shape))
cv2.imwrite(output_img_name, resized)
print('[INFO] Reduced image is written to {} '.format(output_img_name))

