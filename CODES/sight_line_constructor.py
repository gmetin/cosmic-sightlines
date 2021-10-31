from scipy import ndimage
import numpy as np

class Sightline:
    def __init__(self,start,end,num = 1000):

        self.start = start
        self.end = end
        self.r = []
        self.delta = []
        self.num = num


    def calc_los(self,start, end, num, delta):
        XYZ = np.linspace(self.start, self.end, self.num)
        los_delta = ndimage.map_coordinates(delta, XYZ, order=0, mode='nearest')
        return los_delta
    

