# MLAndAIMathUtils
Reusable implementations for basic math utilities for machine learning and python

### Identifying singlular matrices (IdentifyingSpecialMatrices.py)

When coding or solving data analysis problems, one problem that can  occur is if your code encounters a special matrix that isn't invertible,  or has an infinite number of eigenvectors, or similar. On other  occasions, for example where you are reducing dimensionality, that might  even be desirable!  So here you will write a code fragment that traps  for different types of special matrices before calling the python  inversion routine, and classifies the type of special case encountered. Idea: While converting matrix to row echolean form if any diagnol element of matrix is zero, we consider matrix as singular. At present implmented for 4 * 4 matrix which can be generalized for any matrix.

### Gram-Schmidt process (GrahmSchmidtOrthonormal.py)

When coding or solving data analysis problems we have to transform given data for example in face recoginiztion we tranform images of faces to generate data from given data. Transformation step involves operations like projection, inverse, transpose  to name a few. These operations are easier to perform if we have basis vector in orthonormal form. Gram-Schmidt process helps us in constructing linearly independent vectors to orthonormal basis vector. This algorithm is implemented in GrahmSchmidtOrthonormal.py
