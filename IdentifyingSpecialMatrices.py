# -*- coding: utf-8 -*-

# Author: Venkata Ravi Kumar
# File name: IdentifyingMatrices.py
# References: Coursera: Mathematics for Machine learning.

import numpy as np

class MatrixIsSingular(Exception): pass

class MatrixWrongShape(Exception): pass

class SpecialMatrix(object):
    """ To determine if an inverse exists. Input matrix shape (4,4)"""
    # Information about implementation (not the abstraction)
    # Convert the given matrix to echelon form, and testing.
    # Echelon form is shown below
    #  [[1, x, y, z],
    #   [0, 1, a, b],
    #   [0, 0, 1, c],
    #   [0, 0, 0, 1]
    #  ]
    # if this fails by leaving zeros that can’t be removed on the leading diagonal. 
    # then matix is singular and does not have inverse.
    
    def __init__(self):
        """ create an all zero matrix of shape (4,4) """
        self.matrix = np.zeros((4,4))
        return
    
    def isSingular(self, mat):
        # check if input shape is (4,4) and copyt to member element.
        if(mat.shape[0] != 4 or mat.shape[0] != 4 ):
            raise MatrixWrongShape
        else:
            self.matrix = np.array(mat, dtype=np.float_) 
            
        try:
            self.__fixRowZero()
            self.__fixRowOne()
            self.__fixRowTwo()
            self.__fixRowThree()
        except MatrixIsSingular:
            return True
        
        return False

    def __fixRowZero(self) :
        """ For Row Zero, all we require is the first element is equal to 1."""
        # We'll divide the row by the value of matrix[0, 0].
        # This will get us in trouble though if matrix[0, 0] equals 0, so first we'll test for that,
        # and if this is true, we'll add one of the lower rows to the first one before the division.
        # We'll repeat the test going down each lower row until we can do the division.
    
        if self.matrix[0,0] == 0 :
            self.matrix[0] = self.matrix[0] + self.matrix[1]
        if self.matrix[0,0] == 0 :
            self.matrix[0] = self.matrix[0] + self.matrix[2]
        if self.matrix[0,0] == 0 :
            self.matrix[0] = self.matrix[0] + self.matrix[3]
        if self.matrix[0,0] == 0 :
            raise MatrixIsSingular()
        self.matrix[0] = self.matrix[0] / self.matrix[0,0]
        return
    
    
    def __fixRowOne(self) :
        """ For row 1 we want data in format [0, 1, a, b] """
        # First we'll set the sub-diagonal elements to zero, i.e. matrix[1,0].
        # Next we want the diagonal element to be equal to one.
        # We'll divide the row by the value of A[1, 1].
        # Again, we need to test if this is zero.
        # If so, we'll add a lower row and repeat setting the sub-diagonal elements to zero.
        self.matrix[1] = self.matrix[1] - self.matrix[1,0] * self.matrix[0]
        if self.matrix[1,1] == 0 :
            self.matrix[1] = self.matrix[1] + self.matrix[2]
            self.matrix[1] = self.matrix[1] - self.matrix[1,0] * self.matrix[0]
        if self.matrix[1,1] == 0 :
            self.matrix[1] = self.matrix[1] + self.matrix[3]
            self.matrix[1] = self.matrix[1] - self.matrix[1,0] * self.matrix[0]
        if self.matrix[1,1] == 0 :
            raise MatrixIsSingular()
        self.matrix[1] = self.matrix[1] / self.matrix[1,1]
        return 
    

    def __fixRowTwo(self) :
        """ For row 2 we want data in format [0, 0, 1, a] """
        # First we'll set the sub-diagonal elements to zero, i.e. matrix[2,0] and matrix[2,1].
        self.matrix[2] = self.matrix[2] - self.matrix[2,0] * self.matrix[0]
        self.matrix[2] = self.matrix[2] - self.matrix[2,1] * self.matrix[1]
        # Next we'll test that the diagonal element is not zero and want diagnaol element to 1
        if self.matrix[2,2] == 0 :
            self.matrix[2] = self.matrix[2] + self.matrix[3]
            self.matrix[2] = self.matrix[2] - self.matrix[2,0] * self.matrix[0]
            self.matrix[2] = self.matrix[2] - self.matrix[2,1] * self.matrix[1]     
        if self.matrix[2,2] == 0 :
            raise MatrixIsSingular()
        self.matrix[2] = self.matrix[2] / self.matrix[2,2]
                    
        return
    
    def __fixRowThree(self) :
        """ For row 3 we want data in format [0, 0, 0, 1] """
        # First we'll set the sub-diagonal elements to zero, i.e. matrix[2,0] and matrix[2,1].
        self.matrix[3] = self.matrix[3] - self.matrix[3,0] * self.matrix[0]
        self.matrix[3] = self.matrix[3] - self.matrix[3,1] * self.matrix[1]
        self.matrix[3] = self.matrix[3] - self.matrix[3,2] * self.matrix[2]
        # Next we'll test that the diagonal element is not zero and want diagnaol element to 1
        
        if self.matrix[3,3] == 0 :
           raise MatrixIsSingular()
        self.matrix[3] = self.matrix[3] / self.matrix[3,3]
            
        return
 
    
if __name__ == "__main__":
    
    A = np.array([
        [2, 0, 0, 0],
        [0, 3, 0, 0],
        [0, 0, 4, 4],
        [0, 0, 5, 5]
    ], dtype=np.float_)
    
    specMat = SpecialMatrix()
    print('given matrix is singlular', specMat.isSingular(A) ) 
    
    # To check our code is right verify like below
    
    if(np.allclose(np.linalg.det(A), 0)):
        print('Singular Matrix, above answer is correct')
    else:
        print('Non Singular Matrix, above answer is correct')
        