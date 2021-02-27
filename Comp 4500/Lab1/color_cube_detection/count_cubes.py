import cv2
import numpy as np

#TODO: Modify these values for yellow color range. Add thresholds for detecting green also.
yellow_lower = np.array([11, 150, 140])
yellow_upper = np.array([60, 255, 255])
green_lower = np.array([8, 25, 13])
green_upper = np.array([179, 254, 79])


#TODO: Change this function so that it filters the image based on color using the hsv range for each color.
def filter_image(img, hsv_lower, hsv_upper):

    # Modify mask
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
   # this line was for checking the source image with the keymap as i went
    # cv2.imshow("orig", img)

    mask = cv2.inRange(hsv, hsv_lower, hsv_upper)
    return mask

    
#TODO: Change the parameters to make blob detection more accurate. Hint: You might need to set some parameters to specify features such as color, size, and shape. The features have to be selected based on the application. 
def detect_blob(mask):
    
    img = cv2.medianBlur(mask, 99)
    img = cv2.medianBlur(mask, 15)
    img = cv2.bitwise_not(img)

   # Set up the SimpleBlobdetector with default parameters with specific values.
    params = cv2.SimpleBlobDetector_Params()
   # a square is .785
    params.filterByCircularity = True
    params.maxCircularity = 0.95
    params.minCircularity = 0.50
   # 225 is the min area in order to ignore blobs discovered by accident when scanning for yellow
    params.filterByArea = True
    params.minArea = 225
    params.maxArea = 19200
   # this is set low because of the off chance of certain mishaps involving dark or brighter hues than expected
    params.filterByConvexity = True
    params.minConvexity = 0.5

   # builds a blob detector with the given parameters 
    detector = cv2.SimpleBlobDetector_create(params)

   # use the detector to detect blobs.
    keypoints = detector.detect(img)

    keymap = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
   # these lines were the second portion of lines i used to check the source image and keymaps
    # cv2.imshow("keypoints", keymap)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    return len(keypoints)

    
def count_cubes(img):
    mask_yellow = filter_image(img, yellow_lower, yellow_upper)
    num_yellow = detect_blob(mask_yellow)
    mask_green = filter_image(img, green_lower, green_upper)
    num_green = detect_blob(mask_green)

    #TODO: Modify to return number of detected cubes for both yellow and green (instead of 0)
    return num_yellow, num_green

