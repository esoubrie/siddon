#!/usr/bin/env python
import time
import numpy as np
import siddon
# object
header = {'SIMPLE':True,'BITPIX':-64,
          'NAXIS1':128, 'NAXIS2':128, 'NAXIS3':128,
          'CRPIX1':64., 'CRPIX2':64., 'CRPIX3':64.,
          'CDELT1':0.02, 'CDELT2':0.02, 'CDELT3':0.02,
          'CRVAL1':0., 'CRVAL2':0., 'CRVAL3':0.,}
obj = siddon.simu.object_from_header(header)
obj[:] = siddon.phantom.shepp_logan(obj.shape)
# number of images
n = 20
# reshape object for 4d model
obj4 = obj.reshape(obj.shape + (1,)).repeat(n, axis=-1)
obj4.header.update('NAXIS', 4)
obj4.header.update('NAXIS4', obj4.shape[3])
obj4.header.update('CRVAL4', 0.)

# data 
image_header = {'n_images':n,
                'SIMPLE':True, 'BITPIX':-64,
                'NAXIS1':128, 'NAXIS2':128,
                'CRPIX1':64, 'CRPIX2':64,
                'CDELT1':6e-5, 'CDELT2':6e-5,
                'CRVAL1':0., 'CRVAL2':0.,
                }
image_header['radius'] = 200.
data = siddon.simu.circular_trajectory_data(**image_header)
data[:] = np.zeros(data.shape)
# projection
t = time.time()
data = siddon.projector4d(data, obj4)
print("projection time : " + str(time.time() - t))
# backprojection
x0 = obj4.copy()
x0[:] = 0.
t = time.time()
x0 = siddon.backprojector4d(data, x0)
print("backprojection time : " + str(time.time() - t))