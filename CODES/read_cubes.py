"""
open 1024**3 float cube and return np.array
"""

import numpy as np

def read(path): 
    nc = 1024
    file = np.fromfile(path, dtype=np.single).reshape(nc,nc,nc)
    return (file)


def read_many(simlist):
    a = np.genfromtxt(simlist,dtype='str')
    files = a[:,0]
    redshifts = a[:,1].astype(np.single)
    return (files,redshifts)