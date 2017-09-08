#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 13:27:41 2017

@author: hp
"""

import numpy as np
import scipy.sparse as sps
from pyspark.mllib.linalg import Vectors

dvect1 = np.array([5.0 , 0.0, 1.0 , 7.0])
dvect2 = [5.0 , 0.0, 1.0 , 7.0]
svect1 = Vectors(4 , [0,2,3] , [5.0 , 1.0 , 7.0])
svect2 = sps.csc_matrix((np.array([5.0 , 1.0 , 7.0]),np.array([0,2,3])) ,  shape = (4,1))

