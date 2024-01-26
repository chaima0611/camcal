import numpy as np
import cv2 as cv
import glob
# import pickle
import json

# chessboardSize = (9,6)
chessboardSize = (7,7)
frameSize = (8000,6000)
# frameSize = (9152,6944)

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1],3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob.glob('imgs3/*.jpg')
for fname in images:
    img = cv.imread(fname)
    # cv.imshow('Image', img)
    # cv.waitKey(1000)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # cv.waitKey(1000)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)
    print(fname)
    print(ret)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)
        # Draw and display the corners
        cv.drawChessboardCorners(img, chessboardSize, corners2, ret)
        # cv.imshow('img', img)
        # cv.waitKey(500)
cv.destroyAllWindows()

############## CALIBRATION #######################################################

ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, frameSize, None, None)

# Save the camera calibration result for later use (we won't worry about rvecs / tvecs)
# pickle.dump((cameraMatrix, dist), open( "calibration.pkl", "wb" ))
# pickle.dump(cameraMatrix, open( "cameraMatrix.pkl", "wb" ))
# pickle.dump(dist, open( "dist.pkl", "wb" ))

# Save camera calibration data to a JSON file
calibration_data = {
    "cameraMatrix": cameraMatrix.tolist(),
    "dist": dist.tolist()
}

with open("calibration.json", "w") as json_file:
    json.dump(calibration_data, json_file)

############## UNDISTORTION #####################################################

img = cv.imread('imgs3/output_5.jpg')
scaled_image = cv.resize(img, (800, 600))
cv.imshow('Image', scaled_image)
cv.waitKey(1000)
h,  w = img.shape[:2]
newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))



# Undistort
dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imwrite('newResult5_2.jpg', dst)

# cv.imshow('dst', dst)
# cv.waitKey(500)