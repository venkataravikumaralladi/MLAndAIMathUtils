# Image super resolution
Super resolution encompases a set of algorithms and techniques used to enhance, increase, and upsample the resolution of an input image. More simply, take an input image and increase the width and height of the image with minimal (and ideally zero) degradation in quality.

### Input data (.xlsx file)

In case project requirments mentions that input data is in excel file. We have to convert this data to png image which is used as input to pre-built models present in `opencv` library. This conversion can be performed by using utility named `excel_data_to_image_converter.py` provided.

### Image super resolution process (img_super_res_util.py)

We’ll be utilizing four pre-trained super resolution models. EDSR: Enhanced Deep Residual Networks for Single Image Super-Resolution. ESPCN: Real-Time Single Image and Video Super-Resolution Using an Efficient Sub-Pixel Convolutional Neural Network. FSRCNN: Accelerating the Super-Resolution Convolutional Neural Network and LapSRN: Fast and Accurate Image Super-Resolution with Deep Laplacian Pyramid Network. Super resolution image is stored in `output_imgs' folder 

### Converting super resolution image to csv file for comparsion with input excel file (image_to_csv_data_converter.py)
Upscaled super resolution image is converted to .csv file. The converted .csv file is used to compare pixel values of input file (.xlsx file). 
