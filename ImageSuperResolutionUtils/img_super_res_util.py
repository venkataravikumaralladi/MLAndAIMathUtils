"""
File Created: 14th November 2021
Author: Venkata Ravi Kumar A 
-----

"""

'''
    Notes on Super resolution of images:
        
        Super resolution encompases a set of algorithms and techniques used to enhance,
        increase, and upsample the resolution of an input image. More simply, take an input
        image and increase the width and height of the image with minimal (and ideally zero)
        degradation in quality.
        
        We user "OpenCV" python library. In this module we use "dnn_superes".
        This module provideds an easy to use interface for implementing super resolution
        based on deep learning methods. This interface contains pre-contained models that 
        can be used for inference.
        
        Following models are supported by this script.
            Enhanced Deep Super resolution (EDSR),
            Efficient Sub-pixel convolution Convolution Neural network (ESPCN),
            Faster Super resolution convolution neural network (FSRCNN), and
            Laplacian Pyramid Super resolution network (LapSRN)
        
        Requirments to run this script: This can be done by creating seperate environement to 
        avoid conflicts with your present environement.
            
            conda create --name hackathon-opencv-env python=3.8
            conda activate opencv-env
            pip install numpy scipy matplotlib scikit-learn
            pip install opencv-contrib-python
            
        Usage:
            (opencv-env) C:\TechnicalABB\Hackathon2021\Ralf_Idea\implementation>
                python img_super_res_util.py -m models\EDSR_x3.pb
                                             -i input_imgs\sample_data.png
                                             -o output_imgs\sr_sample_data_x3.png
                                             
            Successfull sample output is shown below
                
                [INFO] loading super resolution model: models\EDSR_x3.pb
                [INFO] model name: edsr
                [INFO] model scale: 3
                [INFO] w: 32, h: 32
                [INFO] super resolution took 0.382183 seconds
                [INFO] w: 96, h: 96
                [INFO] bicubic interpolation took 0.000000 seconds
                [INFO] upscaled super resolution image is written successfully output_imgs\sr_sample_data_x3.png
        
        References: 
            https://www.pyimagesearch.com/2020/11/09/opencv-super-resolution-with-deep-learning/
            https://towardsdatascience.com/deep-learning-based-super-resolution-with-opencv-4fd736678066
            https://note.nkmk.me/en/python-opencv-imread-imwrite/
            https://bleedai.com/super-resolution-going-from-3x-to-8x-resolution-in-opencv/
'''

# import the necessary packages
import argparse
import time
import cv2
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
	help="path to super resolution model")
ap.add_argument("-i", "--image", required=True,
	help="path to input image we want to increase resolution of")
ap.add_argument("-o", "--output", required=False,
        help="[OPTIONAL] path to output super res image")
args = vars(ap.parse_args())

# extract the model name and model scale from the file path
modelName = args["model"].split(os.path.sep)[-1].split("_")[0].lower()
modelScale = args["model"].split("_x")[-1]
modelScale = int(modelScale[:modelScale.find(".")])

# initialize OpenCV's super resolution DNN object, load the super
# resolution model from disk, and set the model name and scale
print("[INFO] loading super resolution model: {}".format(
	args["model"]))
print("[INFO] model name: {}".format(modelName))
print("[INFO] model scale: {}".format(modelScale))
sr = cv2.dnn_superres.DnnSuperResImpl_create()
sr.readModel(args["model"])
sr.setModel(modelName, modelScale)

# load the input image from disk and display its spatial dimensions
image = cv2.imread(args["image"])
print("[INFO] w: {}, h: {}".format(image.shape[1], image.shape[0]))

# use the super resolution model to upscale the image, timing how long it takes
start = time.time()
upscaled = sr.upsample(image)
end = time.time()
print("[INFO] super resolution took {:.6f} seconds".format(
	end - start))

# show the spatial dimensions of the super resolution image
print("[INFO] w: {}, h: {}".format(upscaled.shape[1],
	upscaled.shape[0]))

# resize the image using standard bicubic interpolation
start = time.time()
bicubic = cv2.resize(image, (upscaled.shape[1], upscaled.shape[0]),
	interpolation=cv2.INTER_CUBIC)
end = time.time()
print("[INFO] bicubic interpolation took {:.6f} seconds".format(
	end - start))

if args["output"] is not None:
    cv2.imwrite(args["output"], upscaled)
    print("[INFO] upscaled super resolution image is written successfully {}".format(args["output"]))

# show the original input image, bicubic interpolation image, and
# super resolution deep learning output
#cv2.imshow("Original", image)
#cv2.imshow("Bicubic", bicubic)
#cv2.imshow("Super Resolution", upscaled)
#cv2.waitKey(0)