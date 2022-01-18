from scipy import ndimage
import numpy as np

class Sightline:

    def __init__(self,start,end,origin,num = 20): #start & end & origin are 3x1 arrays (x,y,z) each; num: entries per Mpc/h
        self.start = start
        self.end = end
        self.num = num
        self.origin = origin
        self.r = np.linalg.norm(self.end - self.start)

    def calc_los(self,res,delta):
        start = ((self.start-self.origin) /res)
        end =   ((self.end -self.origin)/res)
        #arr1 = np.pad(arr,(0,1),'constant') # if you want to add 0's at the end
        XYZ = np.floor(np.linspace(start, end, int(self.num*self.r))).astype(np.single)
        los_delta = ndimage.map_coordinates(delta, XYZ.T, order=0, mode='constant',cval=-10.0)
        return los_delta
    

