import numpy as np
import cv2
import glob
import position_detect



#piece High=4m Large=8.5m Wide=5m


#function : change from the coordinate system camera to coordinate used by group trajectory
def change_repere(x,y,z,position):
    xyz=position[0]
    angle=position[1]
    axis_rotation=position[2]
    noimg=position[3]


    if noimg==0:
        x_abs=xyz[2]
        y_abs=y-xyz[0]
        z_abs=z-xyz[1]


        #Tait Bryan angles:zyx
        rall=angle
        yaw=np.arctan(-axis_rotation[0]/axis_rotation[2])
        pitch=np.arcsin(-axis_rotation[1])
    else :
        x_abs,y_abs,z_abs,yaw,pitch,rall=0,0,0,0,0,0

    return noimg,x_abs,y_abs,z_abs,yaw,pitch,rall


#function : whether chessboard is too inclined / is captured by camera
def quality(position,limite_pitch,limite_yaw):
    bon=1
    axis_rotation=position[2]
    noimg=position[3]

    #if not captured by camera
    if noimg==1:
        bon=0

    #if captured,
    #imite_yaw and limite_pitch are defined by characteristic, obtain by experiment

    elif abs(axis_rotation[1])>(np.cos(limite_yaw)*np.sin(limite_pitch) or abs(axis_rotation[2])>np.sin(limite_yaw)):
        bon=0
    return bon




cap=[]
dist=[]
mtx=[]
camera_y=[2.5,2.5,2.5,2.5]
camera_z=[2,2,2,2]
limite_pitch,limite_yaw=np.pi/3,np.pi/3


for i in range (4):
    cap.append(cv2.VideoCapture(0))
    dist.append (np.loadtxt("distortion_coeffs"+str(i)+".txt" ))
    mtx.append(np.loadtxt("intrinsic_matrix"+str(i)+".txt" ))



while(1):
    position =[0,0,0,0,0,0,0]
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('end')
        break



    for j in range(4):
        position_j=position_detect.fnpostion(dist[j],mtx[j],cap[j])

        #defalut : 60 degree for limite_pitch and limite_yaw
        if quality(position_j,np.pi/3,np.pi/3):
            position_ab_j=change_repere(0,camera_y[j],camera_z[j],position_j)
            position=np.add(position,position_ab_j)

    position=[c/4.0 for c in position]
    x_abs,y_abs,z_abs,yaw,pitch,rall=position[1:7]

    print ('-----position------')
    print (x_abs,y_abs,z_abs)

    print ('-------rotation--------')
    print (yaw,pitch,rall)



cv2.destroyAllWindows()
