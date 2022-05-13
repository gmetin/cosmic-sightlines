
import numpy as np
from sight_line_constructor import Sightline
import read_cubes
from scipy import ndimage
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib as mpl
from astropy.io import ascii

from astropy.cosmology import FlatLambdaCDM
from astropy import units as u

from multiprocessing import Pool


from scipy import interpolate
from colossus.cosmology import cosmology



path = "/var/lib/libvirt/images/nbody/baorsd/run101/density_field/"
files = ascii.read('/home/mata/cosmic-sightlines/simlist.txt',names=["filename", 'redshift'])

files = files[::-1] #lowest redshift first
n_files = len(files)
nc = 1024
L = 2048
res = L/nc

#Function to read in files
l_arr = []
for i in range(len(files)):
    tmp = read_cubes.read(path+str(files[i]['filename']))
    l_arr.append(tmp)



"""Create k^2 in box (nc x nc x nc)"""
def k_box(nc,L):
    kfac = 2.*np.pi/L
    k= np.fft.fftfreq(nc,d=1./nc/kfac) #d controls spacing
    a = np.transpose(np.indices((nc,nc,nc)).T, (2, 1, 0, 3)) #1 grid cell 3 coordinates
    k2=(k[a]**2).sum(axis=-1) # each grid cell is sum of squares of coordinates
    return k2.astype(np.float16)
k2 = k_box(len(l_arr[0]),len(l_arr[0])*res)


def worker(file):
    delta_k = np.fft.fftn(file)
    delta_kk2 = delta_k /k2
    delta_kk2[0,0,0] =  0
    phi = np.fft.ifftn(delta_kk2)
    phi_r = phi.real 
    return phi_r


phi_arr = []
for i in l_arr:
   phi_arr.append(worker(i))
 

for i in range(len(phi_arr)):
    np.asarray(phi_arr[i]).astype(np.single).tofile("phi_"+str(files[i]['filename']))

#p = Pool(10)
#res_los =    p.map(worker,l_arr)


#for i in range(len(res_los)):
    #res_los[i].tofile("phi_"+str(files[i]['filename'])).astpye(np.single)