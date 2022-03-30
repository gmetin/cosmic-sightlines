from scipy import ndimage
import numpy as np

class Sightline:

    def __init__(self,start,end,origin, periodic = False, num = 20): #start & end & origin are 3x1 arrays (x,y,z) each; num: entries per Mpc/h
        self.start = start
        self.end = end
        self.num = num
        self.origin = origin
        self.r = np.linalg.norm(self.end - self.start)
        self.periodic = periodic

    def calc_los(self,res,delta):
        self.res = res
        start = ((self.start-self.origin) /res)
        end =   ((self.end -self.origin)/res)
        #arr1 = np.pad(arr,(0,1),'constant') # if you want to add 0's at the end
        XYZ = np.floor(np.linspace(start, end, int(self.num*self.r))).astype(np.single)
        self.los = []
        if (self.periodic==True):
            los_delta = ndimage.map_coordinates(delta, XYZ.T, order=0,  mode='grid-wrap')
        else:
            los_delta = ndimage.map_coordinates(delta, XYZ.T, order=0, mode='constant',cval=-10.0)
        self.los = los_delta
        self.dist = np.linspace(0, self.r, len(self.los))
        return los_delta
    
    def save_sightline(self,name):
        tp = np.dtype([('distance', np.single), ('density', np.single)])
        arr = np.zeros(self.los.size,dtype=tp)
        arr["distance"]=self.dist
        arr["density"]=self.los
        np.save("sightline_"+str(name),arr)
         