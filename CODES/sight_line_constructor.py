from scipy import ndimage
import numpy as np

class Sightline:

    def __init__(self,start,end,num = 1000): #start & end are  3x1 arrays (x,y,z) each
        self.start = start
        self.end = end
        self.num = num
        self.r = np.linalg.norm(self.end - self.start)

    def calc_los(self, res, delta):
        start = (self.start/res).astype(np.int32)
        end =  (self.end/res).astype(np.int32)
        XYZ = np.linspace(start, end, self.num)
        los_delta = ndimage.map_coordinates(delta, XYZ.T, order=0, mode='nearest')
        return los_delta
    

