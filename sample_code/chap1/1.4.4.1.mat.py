from numpy import *
import scipy.io

x = array([0,1,2,3])

data = {} 
data['x'] = x
scipy.io.savemat('test.mat',data)

data = scipy.io.loadmat('test.mat')
print data
