# -*- coding: utf-8 -*-


import numpy as np
import cv2
import glob




def fnpostion (dist,mtx,cap):

	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
	objp = np.zeros((6*9,3), np.float32)
	objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)*25.6


	xyz=0
	angle=0
	axis_rotation=0
	angle=0

	noimg=1


	ret, img = cap.read()
	cv2.imshow('img',img)



	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	ret, corners = cv2.findChessboardCorners(gray, (9,6),None)


	if ret == True:
		noimg=0
		corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
		# Find the rotation and translation vectors.
		_,rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)


		#tranform the rotation vectors to rotation matrix
		R,_=cv2.Rodrigues(rvecs)

		#rotation angle , unit rad, par rapport à l'axis rvecs
		theta=np.linalg.norm(rvecs)

		xyz=(np.matmul(R,[[0],[0],[0]]) + tvecs).reshape(-1,3)
		axis_rotation=rvecs.reshape(-1,3)/theta

		angle=theta*180/3.14159
		print (axis_rotation)


	return 	xyz,angle,axis_rotation,noimg





#read the distortion coefficient and intrinsic matrix calculated before
dist=np.loadtxt("distortion_coeffs.txt" )
mtx=np.loadtxt("intrinsic_matrix.txt" )


cap = cv2.VideoCapture(0)


while(1):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		print('end')
		break


	position_instant=fnpostion (dist,mtx,cap)

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
