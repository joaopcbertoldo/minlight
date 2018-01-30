# -*- coding: utf-8 -*-


import numpy as np
import cv2
import glob




def fnpostion (dist,mtx,ret, img):

	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
	objp = np.zeros((6*9,3), np.float32)
	objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)*25.6


	xyz=0
	angle=0
	axis_rotation=0
	angle=0

	noimg=1





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


cv2.destroyAllWindows()
