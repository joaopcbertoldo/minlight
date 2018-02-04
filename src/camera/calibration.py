import numpy as np

import cv2


def fncalibration(cap):
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*9,3), np.float32)
    objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)*25.6 #the length of square is 2.56cm


    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.




    count=0 #count the number of picture taken

    cv2.namedWindow('img',0)

    while(1):

        ret, img = cap.read()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            mark=0
            print('end')
            break

        #take 20 picture to calibrate
        if count==20: #!!!!!!!!!!wasnt it supposed to be count? how could it have worked like this?
            break


        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

        # If found, add object points, image points (after refining them)
        if ret == True:


            corners2 = cv2.cornerSubPix(gray,corners,(15,15),(-1,-1),criteria)


            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (9,6), corners2,ret)
            cv2.imshow('img',img)


           	#take piciture every 5s
            if (cv2.waitKey(500) & 0xFF >0):

                print(count)
                count+=1
                objpoints.append(objp)
                imgpoints.append(corners2)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            cv2.imshow('img',img)
    cv2.destroyAllWindows()

    #calibaration
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)


    #caculate the average error
    tot_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        tot_error += error
        errormoyen=tot_error/len(objpoints)

    return  dist,mtx,errormoyen


cap = cv2.VideoCapture(0)

resultat=fncalibration(cap)


print ("total error: ", resultat[2])

#save the distortion coefficient and the intrinsic matrix
np.savetxt("distortion_coeffs.txt" ,resultat[0])
np.savetxt("intrinsic_matrix.txt" ,resultat[1])

cv2.destroyAllWindows()
