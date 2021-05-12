# -*- coding: utf-8 -*-

# Author: Venkata Ravi Kumar
# File name: GrahmSchmidtOrthonormal.py
# References: Coursera: Mathematics for Machine learning.


import numpy as np
import numpy.linalg as la

class GrahmSchmidtOrthonormal(object):
    
    ''' Gram-Schmidt procedure is implemented in class.
        Converts list of vectors to orthonormal basis.
        As a corollary, we determine the dimension of the space 
        spanned by the basis vectors, which is equal to or less 
        than the space which the vectors sit. 
        Input: 4 basis vectors is given as list of vectors as columns of input matrix
    '''
    
    # Information about implementation (not the abstraction)
    # Convert the given matrix to orthonormal form.
   
    def __init__(self):
        """ create an all zero matrix of shape (4,4) """
        self.inputmatrix = np.zeros((4,4))
        self.zeroapprox = 1e-14 # That's 1×10⁻¹⁴ = 0.00000000000001
        return
    
    # Following function will perform the Gram-Schmidt procedure for
    # 4 basis vectors. vectors are represented as list of vectors as 
    # the columns of a matrix. Loop through the vectors one at a time
    # and set them to be orthogonal to all the vectors that came before it
    # before normalising. Note: to take the dot product between vectors. This
    # can be done using the @ operator. To dot product vectors u and v,  we 
    # use the code, u @ v. we shall make use of the @ operator.
    # In general the @ operator will combine vectors and/or matrices in 
    # the expected linear algebra way, i.e. it will be either the vector
    # dot product, matrix multiplication, or matrix operation on a vector,
    # depending on it's input. For example to calculate the following expressions,
    # a = s. t, s = At, and M = AB can be computed as
    # a = s @ t, s = A @ t, and M = A @ B

    def gsBasis4(self, inputMat) :
        # Make B as a copy of input matrix, since we're going to alter it's values.
        orthoNormalMatrix = np.array(inputMat, dtype=np.float_) 
        
        # The zeroth column is easy, since it has no other vectors to make it normal to.
        # All that needs to be done is to normalise it, i.e. divide by its modulus, or norm.
        orthoNormalMatrix[:, 0] = orthoNormalMatrix[:, 0] / la.norm(orthoNormalMatrix[:, 0])
        
        # For the first column, we need to subtract any overlap with our new zeroth vector.
        orthoNormalMatrix[:, 1] = orthoNormalMatrix[:, 1] - orthoNormalMatrix[:, 1] @ orthoNormalMatrix[:, 0] * orthoNormalMatrix[:, 0]
        
        # If there's anything left after that subtraction, then orthoNormalMatrix[:, 1] is
        # linearly independant of orthoNormalMatrix[:, 0]
        # If this is the case, we can normalise it. Otherwise we'll set that vector to zero.
        if la.norm(orthoNormalMatrix[:, 1]) > self.zeroapprox :
            orthoNormalMatrix[:, 1] = orthoNormalMatrix[:, 1] / la.norm(orthoNormalMatrix[:, 1])
        else :
            orthoNormalMatrix[:, 1] = np.zeros_like(orthoNormalMatrix[:, 1])
            
        # Now we need to repeat the process for column 2.
        # First to subtract the overlap with the zeroth vector,
        # and the second to subtract the overlap with the first.
        orthoNormalMatrix[:, 2] = orthoNormalMatrix[:, 2] - orthoNormalMatrix[:, 2] @ orthoNormalMatrix[:, 0] * orthoNormalMatrix[:, 0]
        orthoNormalMatrix[:, 2] = orthoNormalMatrix[:, 2] - orthoNormalMatrix[:, 2] @ orthoNormalMatrix[:, 1] * orthoNormalMatrix[:, 1]
        
        # Again we'll need to normalise our new vector, just like vector 1
        # If there's anything left above actions, then orthoNormalMatrix[:, 2] is
        # linearly independant of orthoNormalMatrix[:, 0] and orthoNormalMatrix[:, 1]
        # If this is the case, we can normalise it. Otherwise we'll set that vector to zero.
        if la.norm(orthoNormalMatrix[:, 2]) > self.zeroapprox :
            orthoNormalMatrix[:, 2] = orthoNormalMatrix[:, 2] / la.norm(orthoNormalMatrix[:, 2])
        else :
            orthoNormalMatrix[:, 2] = np.zeros_like(orthoNormalMatrix[:, 2])
        
        # Now we need to repeat the process for column 3
        # First to subtract the overlap with the zeroth vector,
        # the second to subtract the overlap with the first vector,
        # the third to substract the overlap with the second vector.
        orthoNormalMatrix[:, 3] = orthoNormalMatrix[:, 3] - orthoNormalMatrix[:, 3] @ orthoNormalMatrix[:, 0] * orthoNormalMatrix[:, 0]
        orthoNormalMatrix[:, 3] = orthoNormalMatrix[:, 3] - orthoNormalMatrix[:, 3] @ orthoNormalMatrix[:, 1] * orthoNormalMatrix[:, 1]
        orthoNormalMatrix[:, 3] = orthoNormalMatrix[:, 3] - orthoNormalMatrix[:, 3] @ orthoNormalMatrix[:, 2] * orthoNormalMatrix[:, 2]
        
        
        # Again we'll need to normalise our new vector, just like vector 1
        # If there's anything left above actions, then orthoNormalMatrix[:, 2] is
        # linearly independant of orthoNormalMatrix[:, 0], orthoNormalMatrix[:, 1] and rthoNormalMatrix[:, 2]
        # If this is the case, we can normalise it. Otherwise we'll set that vector to zero.
        if la.norm(orthoNormalMatrix[:, 3]) > self.zeroapprox :
            orthoNormalMatrix[:, 3] = orthoNormalMatrix[:, 3] / la.norm(orthoNormalMatrix[:, 3])
        else :
            orthoNormalMatrix[:, 3] = np.zeros_like(orthoNormalMatrix[:, 3])
    
        # dimensions function uses the Gram-schmidt process to calculate the dimension
        # spanned by a list of vectors. Since each vector is normalised to one, or is zero,
        # the sum of all the norms will be the dimension.
        dimensions =  np.sum(la.norm(orthoNormalMatrix, axis=0))
        
        # Finally, we return the result:
        return orthoNormalMatrix, dimensions
    
    
    # gsBasis4 is implemented for 4 x 4 matrix. Now we will generalise the procedure.
    # Previously, we could only have four vectors, and there was a lot of repeating in the code.
    # We'll use a for-loop here to iterate the process for each vector.
    def gsBasis(self, inputmatrix) :
        orthoNormalMatrix = np.array(inputmatrix, dtype=np.float_) # Make B as a copy of input matrix, since we're going to alter it's values.
        
        # Loop over all vectors, starting with zero, label them with currVecIdx
        for currVecIdx in range(orthoNormalMatrix.shape[1]) :
            # Inside that loop, loop over all previous vectors, prevVecIdx, to subtract.
            for prevVecIdx in range(currVecIdx) :
                # following code to subtract the overlap with previous vectors.
                # you'll need the current vector B[:, currVecIdx] and a previous vector B[:, prevVecIdx]
                 orthoNormalMatrix[:, currVecIdx] = orthoNormalMatrix[:, currVecIdx] - orthoNormalMatrix[:, currVecIdx] @ orthoNormalMatrix[:, prevVecIdx] * orthoNormalMatrix[:, prevVecIdx]
            # Next insert code to do the normalisation test for B[:, currVecIdx]
            if la.norm(orthoNormalMatrix[:, currVecIdx]) > self.zeroapprox :
                orthoNormalMatrix[:, currVecIdx] = orthoNormalMatrix[:, currVecIdx] / la.norm(orthoNormalMatrix[:, currVecIdx])
            else :
                orthoNormalMatrix[:, currVecIdx] = np.zeros_like(orthoNormalMatrix[:, currVecIdx])
                
        # dimensions function uses the Gram-schmidt process to calculate the dimension
        # spanned by a list of vectors. Since each vector is normalised to one, or is zero,
        # the sum of all the norms will be the dimension.
        dimensions =  np.sum(la.norm(orthoNormalMatrix, axis=0))
        
        # Finally, we return the result:
        return orthoNormalMatrix, dimensions
    

    
    
if __name__ == "__main__":
    
    V = np.array([[1,0,2,6],
                  [0,1,8,2],
                  [2,8,3,1],
                  [1,-6,2,3]], dtype=np.float_)

    
    GrahmSchmidtAlgo = GrahmSchmidtOrthonormal()
    orthonormalV, dimensionsV = GrahmSchmidtAlgo.gsBasis4(V)
    
    if(dimensionsV == 4):
        print('Orthogonal matrix for input V dimensions correct')
    else:
        print('Orthogonal matrix for input V dimensions correct')
        
    # Now let's see what happens when we have one vector that is 
    # a linear combination of the others.
    C = np.array([[1,0,2],
              [0,1,-3],
              [1,0,2]], dtype=np.float_)

    orthonormalC, dimensionsC = GrahmSchmidtAlgo.gsBasis(C)
    if(dimensionsC == 2):
        print('Orthogonal matrix for input V dimensions correct')
    else:
        print('Orthogonal matrix for input V dimensions correct')