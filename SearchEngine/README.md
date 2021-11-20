# MLAndAIMathUtils
Reusable implementations for basic math utilities for machine learning and python

### Identifying singlular matrices (IdentifyingSpecialMatrices.py)

When coding or solving data analysis problems, one problem that can  occur is if your code encounters a special matrix that isn't invertible,  or has an infinite number of eigenvectors, or similar. On other  occasions, for example where you are reducing dimensionality, that might  even be desirable!  So here you will write a code fragment that traps  for different types of special matrices before calling the python  inversion routine, and classifies the type of special case encountered. Idea: While converting matrix to row echolean form if any diagnol element of matrix is zero, we consider matrix as singular. At present implmented for 4 * 4 matrix which can be generalized for any matrix.

### Gram-Schmidt process (GrahmSchmidtOrthonormal.py)

When coding or solving data analysis problems we have to transform given data for example in face recoginiztion we tranform images of faces to generate data from given data. Transformation step involves operations like projection, inverse, transpose  to name a few. These operations are easier to perform if we have basis vector in orthonormal form. Gram-Schmidt process helps us in constructing linearly independent vectors to orthonormal basis vector. This algorithm is implemented in GrahmSchmidtOrthonormal.py

### Image transformation using rotation (ImageTransformationUsingRotation/python/image_rotation_utils.py)
Data augumentation is technique used to generate images from available images through various tecniques like tranforming images through rotation, changing background color, changing color contrast to name a few. In folder ImageTransformationUsingRotation image roation technique is implemented. We can rotate the image and annotate the blocks programmatically. With this we have additional images which can be used for training. This code is implemented in generic way so that we can give it for any images. Though rotation functionality is implemented in python Albumentations library this functionality is light weight and can be modified according to project. It is interesting
 to know how abstract concepts like eigen vectors, transformation matrices are used in real time projects and strong in concepts helps us in using libraries and debug effectively. (Sample usage of image rotation utils are shared in  ImageTransformationUsingRotation/notebooks/ImageRotationDataAugumentation.ipynb 
 
 ### Image processing 
Image processing folder consists of image processing in python. Here we will see how we can create new images with foreground images on various background images. Along with new images we also generate corresponding image mask which helps us in creating annotation required for various machine learning algorithms. (ImageProcessing/notebook/image-composition.ipynb)

 ### SyntheticImageGenerator
 Deep learning is wonderful tool which is changing the world of innovation in particular image applications. Due to the unprecedented need for massive, annotated, image datasets, we have to explore various options in additional to manual image collection and annotation. Data is extremely expensive, either in time or in money to pay others for their time in annotating images. Here we develop a tool which generates synthetic image datasets and annotate generated images in COCO format. This tool is developed by me as part of Omdena project from references mentioned in reference section of README.md in that folder.
