import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import math
img=mpimg.imread('/home/pi/Pictures/1.png')
#plt.imshow(img)
#plt.show()
red_image = img[:,:,0]*255
red_image.astype(int)
#plt.imshow(red_image)
green_image = img[:,:,1]*255
#plt.imshow(green_image)
green_image.astype(int)
blue_image = img[:,:,2]*255
#plt.imshow(blue_image)
blue_image.astype(int)





R_2=np.array(red_image)
G_2=np.array(green_image)
B_2=np.array(blue_image)


counts, bins, bars = plt.hist(R_2);



