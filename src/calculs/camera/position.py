import numpy as np
import cv2
import glob


#read the distortion coefficient and intrinsic matrix calculated before
dist=np.loadtxt("distortion_coeffs.txt" )
mtx=np.loadtxt("intrinsic_matrix.txt" )

cap = cv2.VideoCapture(0)



criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)*25.6





while(1):
	
	ret, img = cap.read()
	if cv2.waitKey(1) & 0xFF == ord('q'):
		print('end')
		break



	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

	
	if ret == True:
		corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
		# Find the rotation and translation vectors.
		_,rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)


		#tranform the rotation vectors to rotation matrix
		R,_=cv2.Rodrigues(rvecs)

		#rotation angle , unit rad, par rapport à l'axis rvecs
		theta=np.linalg.norm(rvecs)

		print '-----position------'
		print np.matmul(R,[[0],[0],[0]])+tvecs	# (x,y,z)=R*(X,Y,Z)+T. (x,y,z) is the position in coordinates of camera. 
												#(X,Y,Z) is the position in coordinate of cheeseboard
												# Here we choose the point (0,0,0) on the cheeseboard to see where it is in the coordinates of camera
		print '-------rotation--------'
		print 'theta',theta*180/3.14159
		print 'axis',rvecs/theta
		

		cv2.imshow('img',img)
	else :
		cv2.imshow('img',img)
		
cv2.destroyAllWindows()