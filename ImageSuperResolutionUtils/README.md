# Image super resolution
Super resolution encompases a set of algorithms and techniques used to enhance, increase, and upsample the resolution of an input image. More simply, take an input image and increase the width and height of the image with minimal (and ideally zero) degradation in quality. <br>
Get pre-trained model paramters mentioned at below links and copy in to models folder.<br>
https://github.com/Saafke/EDSR_Tensorflow/tree/master/models <br>
https://github.com/fannymonori/TF-ESPCN/tree/master/export <br>
https://github.com/Saafke/FSRCNN_Tensorflow/tree/master/models <br>
https://github.com/fannymonori/TF-LapSRN/tree/master/export <br>

### Input data (`.xlsx file`)

In case project requirments mentions that input data is in excel file. We have to convert this data to png image which is used as input to pre-built models present in `opencv` library. This conversion can be performed by using utility named `excel_data_to_image_converter.py` provided.

### Image super resolution process (`img_super_res_util.py`)

We’ll be utilizing four pre-trained super resolution models. EDSR: Enhanced Deep Residual Networks for Single Image Super-Resolution. ESPCN: Real-Time Single Image and Video Super-Resolution Using an Efficient Sub-Pixel Convolutional Neural Network. FSRCNN: Accelerating the Super-Resolution Convolutional Neural Network and LapSRN: Fast and Accurate Image Super-Resolution with Deep Laplacian Pyramid Network. Super resolution image is stored in `output_imgs' folder 

### Converting super resolution image to csv file (`image_to_csv_data_converter.py`)
Upscaled super resolution image is converted to .csv file. The converted .csv file is used to compare pixel values of input file (.xlsx file). 

### Image down size process (`image_down_size.py`)
This command tool can be used to down size given image. This scripts down size the image according to percentage passed as argument to script. This can be used to generate data for training model. Original image acts a ground truth and resized small acts as input. This generated data can be used to train super-resolution models.

### Image bluring process (`image_smoothing_blurring.py`)
This command tool can be used to blurr given image. Smoothing and blurring is one of the most important preprocessing steps in all of computer vision and image processing. By smoothing an image prior to applying techniques such as edge detection or thresholding  we are able to reduce the amount of high-frequency content, such as noise and edge. While this may sound counter-intuitive, by reducing the detail in an image we can more easily find objects that we are interested in.Techniques Simple blurring, Weighted Gaussian blurring, Median filtering, and Bilateral blurring are supported in this tool.
