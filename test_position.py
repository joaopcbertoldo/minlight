
# -*- coding: utf-8 -*-


import numpy as np
import cv2
import glob
import position_detect



#read the distortion coefficient and intrinsic matrix calculated before
dist=np.loadtxt("distortion_coeffs.txt" )
mtx=np.loadtxt("intrinsic_matrix.txt" )


cap = cv2.VideoCapture(0)


while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		print('end')
		break


	position_instant=position_detect.fnpostion (dist,mtx,cap)

	xyz=position_instant[0]

	angle=position_instant[1]

	axis_rotation=position_instant[2]

	noimg=position_instant[3]

	if noimg!=1 :
		print ('-----position------')
		print (xyz)	 #(x,y,z)=R*(X,Y,Z)+T.
							#(x,y,z) is the position in coordinates of camera.
							#(X,Y,Z) is the position in coordinate of cheeseboard
							#Here we choose the point (0,0,0) on the cheeseboard to see where it is in the coordinates of camera

		print ('-------rotation--------')
		print ('theta',angle)
		print ('axis',axis_rotation)

	else :
		print ('no image')



cv2.destroyAllWindows()
