"""
File Created: 18th November 2021
Author: Venkata Ravi Kumar A 
-----

"""

'''
    Notes on image smoothing and bluring in images:
        
        Blurred pixel: This means that each pixel in the image is mixed in with
                       its surrounding pixel intensities. This “mixture” of pixels
                       in a neighborhood becomes our blurred pixel.
                       The goal here is to use a low-pass filter to reduce the amount of noise and
                       detail in an image.
        
        Many image processing and computer vision functions, such as thresholding
        and edge detection, perform better if the image is first smoothed or blurred.
        
        By smoothing an image prior to applying techniques such as edge detection or
        thresholding we are able to reduce the amount of high-frequency content,
        such as noise and edges (i.e., the “detail” of an image). While this may sound
        counter-intuitive, by reducing the detail in an image we can more easily
        find objects that we are interested in. Furthermore, this allows us to
        focus on the larger structural objects in the image.
        
        We will study four main smoothing and blurring options:

                    Simple average blurring
                    Gaussian blurring
                    Median filtering
                    Bilateral filtering
                    
        Simple average blurring: By taking the average of the region surrounding a pixel, 
                                we are smoothing it and replacing it with the value of its
                                local neighborhood. This allows us to reduce noise and 
                                the level of detail, simply by relying on the average.
                                as the size of the kernel increases, so will the amount in which the image is blurred.
                                Simply put: the larger your smoothing kernel is, the more 
                                blurred your image will look.
                                While average smoothing was quite simple to understand, 
                                it also weights each pixel inside the kernel area equally
                                — and by doing this it becomes easy to over-blur our image
                                and miss out on important edges. We can remedy this problem
                                by applying Gaussian blurring.
                                
        
        Gaussian blurring:
             Gaussian blurring is similar to average blurring, but instead of using a simple
             mean, we are now using a weighted mean, where neighborhood pixels that are closer 
             to the central pixel contribute more “weight” to the average. The end result is
             that our image is less blurred, but more “naturally blurred,” than using the
             average method.
             In general, it is recommend starting with a simple Gaussian blur and tuning 
             your parameters as needed. While the Gaussian blur is slightly slower than
             a simple average blur (and only by a tiny fraction), a Gaussian blur tends
             to give much nicer results, especially when applied to natural images.
             
        Median blurring:
            Traditionally, the median blur method has been most effective when removing
            salt-and-pepper noise. This type of noise is exactly what it sounds like:
            imagine taking a photograph, putting it on your dining room table, and 
            sprinkling salt and pepper on top of it. Using the median blur method,
            you could remove the salt and pepper from your image.
            The reason median blurring is more effective at removing salt-and-pepper
            style noise from an image is that each central pixel is always replaced
            with a pixel intensity that exists in the image. And since the median
            is robust to outliers, the salt-and-pepper noise will be less influential
            to the median than another statistical method, such as the average.
            
        Bilateral blurring:
            Above blurring methods have been to reduce noise and detail in an image; however,
            as a side effect we have tended to lose edges in the image.
            To reduce noise while still maintaining edges, we can use bilateral blurring. 
            Bilateral blurring accomplishes this by introducing two Gaussian distributions.
            
            The first Gaussian function only considers spatial neighbors. That is, pixels 
            that appear close together in the (x, y)-coordinate space of the image. 
            The second Gaussian then models the pixel intensity of the neighborhood,
            ensuring that only pixels with similar intensity are included in the actual
            computation of the blur.

            Intuitively, this makes sense. If pixels in the same (small) neighborhood
            have a similar pixel value, then they likely represent the same object.
            But if two pixels in the same neighborhood have contrasting values, then
            we could be examining the edge or boundary of an object — and we would like
            to preserve this edge.

            Overall, this method is able to preserve edges of an image, while still
            reducing noise. The largest downside to this method is that it is considerably
            slower than its averaging, Gaussian, and median blurring counterparts.
            
    Usage: 
        Run script as mentioned below sample
            (base) C:\TechnicalABB\Hackathon2021\Ralf_Idea\implementation>
                      python image_smoothing_blurring.py -i input_imgs\vrk_jurs_prk.png 
                                                         -o output_imgs\
         Sample output shown below:                                                    
        
        [INFO] input image name vrk_jurs_prk.png
        [INFO] Input image shown in popup window
        [INFO] Blurring image using average technique.
        [INFO] Average blurred imageimage is written successfully output_imgs\vrk_jurs_prk_avg_3_3.png
        [INFO] Average blurred imageimage is written successfully output_imgs\vrk_jurs_prk_avg_9_9.png
        [INFO] Average blurred imageimage is written successfully output_imgs\vrk_jurs_prk_avg_15_15.png
        [INFO] Blurring image using Gaussian technique.
        [INFO] Gaussian  blurred imageimage is written successfully output_imgs\vrk_jurs_prk_gauss_3_3.png
        [INFO] Gaussian  blurred imageimage is written successfully output_imgs\vrk_jurs_prk_gauss_9_9.png
        [INFO] Gaussian  blurred imageimage is written successfully output_imgs\vrk_jurs_prk_gauss_15_15.png
        [INFO] Blurring image using Median technique.
        [INFO] Median blurred imageimage is written successfully output_imgs\vrk_jurs_prk_median_3.png
        [INFO] Median blurred imageimage is written successfully output_imgs\vrk_jurs_prk_median_9.png
        [INFO] Median blurred imageimage is written successfully output_imgs\vrk_jurs_prk_median_15.png
        [INFO] Blurring image using bilateral technique.
        [INFO] Bilateral blurred imageimage is written successfully output_imgs\vrk_jurs_prk_bilateral_11_21_7.png
        [INFO] Bilateral blurred imageimage is written successfully output_imgs\vrk_jurs_prk_bilateral_11_41_21.png
        [INFO] Bilateral blurred imageimage is written successfully output_imgs\vrk_jurs_prk_bilateral_11_61_39.png
        
    Reference:
        https://www.pyimagesearch.com/2021/04/28/opencv-smoothing-and-blurring/
        
'''

# Import the necessary packages
import os
import argparse
import cv2


# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image")
ap.add_argument("-o", "--output", required = False,
        help="path to output blured image folder")
args = vars(ap.parse_args())

input_img_name = args["image"].split(os.path.sep)[-1].lower()
img_name_withoug_ext = input_img_name.split('.')[0]
print('[INFO] input image name {} '.format(input_img_name))


# load the image, display it to our screen, and initialize a list of
# kernel sizes (so we can evaluate the relationship between kernel
# size and amount of blurring)
image = cv2.imread(args["image"])
print('[INFO] Input image shown in popup window')
cv2.imshow("Original", image)

print('[INFO] Blurring image using average technique.')
# Let's apply standard "averaging" blurring first. Average
# blurring (as the name suggests), takes the average of all
# pixels in the surrounding area and replaces the centeral
# element of the output image with the average. Thus, in
# order to have a central element, the area surrounding the
# central must be odd. Here are a few examples with varying
# kernel sizes. Notice how the larger the kernel gets, the
# more blurred the image becomes
kernelSizes = [(3, 3), (9, 9), (15, 15)]
# loop over the kernel sizes
for (kX, kY) in kernelSizes:
    # apply an "average" blur to the image using the current kernel size
    blurred = cv2.blur(image, (kX, kY))
    cv2.imshow("Average ({}, {})".format(kX, kY), blurred)
    cv2.waitKey(0)
    if args["output"] is not None:
        output_img_name = args["output"] + img_name_withoug_ext + "_avg_" + str(kX) + "_" + str(kY) + ".png"
        cv2.imwrite(output_img_name, blurred)
        print("[INFO] Average blurred imageimage is written successfully {}".format(output_img_name))


print('[INFO] Blurring image using Gaussian technique.')
# We can also apply Gaussian blurring, where the relevant
# parameters are the image we want to blur and the standard
# deviation in the X and Y direction. Again, as the standard
# deviation size increases, the image becomes progressively
# more blurred
# close all windows to cleanup the screen
cv2.destroyAllWindows()
cv2.imshow("Original", image)

# loop over the kernel sizes
for (kX, kY) in kernelSizes:
    # apply an "Gaussian" blur to the image using the current kernel size
    # second argument 0 stands for we let opencv to calculate std dev for us based on kernel size.
    blurred = cv2.GaussianBlur(image, (kX, kY), 0)
    cv2.imshow("Gaussian ({}, {})".format(kX, kY), blurred)
    cv2.waitKey(0)
    if args["output"] is not None:
        output_img_name = args["output"] + img_name_withoug_ext + "_gauss_" + str(kX) + "_" + str(kY) + ".png"
        cv2.imwrite(output_img_name, blurred)
        print("[INFO] Gaussian  blurred imageimage is written successfully {}".format(output_img_name))


print('[INFO] Blurring image using Median technique.')
# The cv2.medianBlur function is mainly used for removing
# what is called "salt-and-pepper" noise. Unlike the Average
# method mentioned above, the median method (as the name
# suggests), calculates the median pixel value amongst the
# surrounding area.    
# close all windows to cleanup the screen
cv2.destroyAllWindows()
cv2.imshow("Original", image)

# loop over the kernel sizes. For median kernel is square.
for k in (3, 9, 15):
    # apply a "median" blur to the image
    blurred = cv2.medianBlur(image, k)
    cv2.imshow("Median {}".format(k), blurred)
    cv2.waitKey(0)
    if args["output"] is not None:
        output_img_name = args["output"] + img_name_withoug_ext + "_median_" + str(k) + ".png"
        cv2.imwrite(output_img_name, blurred)
        print("[INFO] Median blurred imageimage is written successfully {}".format(output_img_name))


print('[INFO] Blurring image using bilateral technique.')
# You may have noticed that blurring can help remove noise,
# but also makes edge less sharp. In order to keep edges
# sharp, we can use bilateral filtering. We need to specify
# the diameter of the neighborhood (as in examples above),
# along with sigma values for color and coordinate space.
# The larger these sigma values, the more pixels will be
# considered within the neighborhood.

# load the image, display it to our screen, and construct a list of
# bilateral filtering parameters that we are going to explore
# close all windows to cleanup the screen
cv2.destroyAllWindows()
cv2.imshow("Original", image)

params = [(11, 21, 7), (11, 41, 21), (11, 61, 39)]
'''
Notes on parameters for bilateral API:
    We need to define the diameter of our pixel neighborhood — the larger this diameter is,
    the more pixels will be included in the blurring computation. Think of this parameter
    as a square kernel size.
    
    The color standard deviation. A larger value for color standard deviation means that 
    more colors in the neighborhood will be considered when computing the blur. If we
    let color standard deviation get too large in respect to the diameter, then we 
    essentially have broken the assumption of bilateral filtering — that only pixels
    of similar color should contribute significantly to the blur.
    
    The space standard deviation, A larger value of standard deviation means that pixels
    farther out from the central pixel diameter will influence the blurring calculation.
    
'''
# loop over the diameter, sigma color, and sigma space
for (diameter, sigmaColor, sigmaSpace) in params:
    # apply bilateral filtering to the image using the current set of parameters
    blurred = cv2.bilateralFilter(image, diameter, sigmaColor, sigmaSpace)
    # show the output image and associated parameters
    title = "Blurred d={}, sc={}, ss={}".format(diameter, sigmaColor, sigmaSpace)
    cv2.imshow(title, blurred)
    cv2.waitKey(0)
    if args["output"] is not None:
        output_img_name = args["output"] + img_name_withoug_ext + "_bilateral_" + str(diameter) + "_" + str(sigmaColor) + "_" + str(sigmaSpace) + ".png"
        cv2.imwrite(output_img_name, blurred)
        print("[INFO] Bilateral blurred imageimage is written successfully {}".format(output_img_name))
    
