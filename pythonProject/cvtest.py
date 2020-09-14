import cv2
import numpy as np


def trim(frame):
    # crop top
    if not np.sum(frame[0]):
        return trim(frame[1:])
    # crop bottom
    elif not np.sum(frame[-1]):
        return trim(frame[:-2])
    # crop left
    elif not np.sum(frame[:, 0]):
        return trim(frame[:, 1:])
    # crop right
    elif not np.sum(frame[:, -1]):
        return trim(frame[:, :-2])
    return frame


# Open the image files.
img1_color = cv2.imread("r.jpg")  # Image to be aligned.
img2_color = cv2.imread("l.jpg")  # Reference image.

# Convert to grayscale.
img1 = cv2.cvtColor(img1_color, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2_color, cv2.COLOR_BGR2GRAY)
height, width = img2.shape

# Create ORB detector with 5000 features.
orb_detector = cv2.ORB_create(5000)

# Find keypoints and descriptors.
# The first arg is the image, second arg is the mask
# (which is not reqiured in this case).
kp1, d1 = orb_detector.detectAndCompute(img1, None)
kp2, d2 = orb_detector.detectAndCompute(img2, None)

# Match features between the two images.
# We create a Brute Force matcher with
# Hamming distance as measurement mode.
matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match the two sets of descriptors.
matches = matcher.match(d1, d2)

# Sort matches on the basis of their Hamming distance.
matches.sort(key=lambda x: x.distance)

# Take the top 90 % matches forward.
matches = matches[:int(len(matches) * 90)]
no_of_matches = len(matches)

# Define empty matrices of shape no_of_matches * 2.
p1 = np.zeros((no_of_matches, 2))
p2 = np.zeros((no_of_matches, 2))

for i in range(len(matches)):
    p1[i, :] = kp1[matches[i].queryIdx].pt
    p2[i, :] = kp2[matches[i].trainIdx].pt

# Find the homography matrix.
homography, mask = cv2.findHomography(p1, p2, cv2.RANSAC)
# print(homography)

# cv2.imshow("output image", img1_color)
# cv2.waitKey()

# martix = np.float32([[1,0,width],[0,1,height]])
# img1_big = cv2.warpAffine(img1_color,martix,(width*3,height*3))
# cv2.imwrite('img1_big.jpg', img1_big)
# cv2.imshow("big image", img1_big)
# cv2.waitKey()

# img2_big = cv2.warpAffine(img2_color,martix,(width*3,height*3))
# cv2.imwrite('img2_big.jpg', img2_big)

# Use this matrix to transform the
# colored image wrt the reference image.
transformed_img = cv2.warpPerspective(img1_color,
                                      homography, (width * 2, height * 2))

transformed_img[0:height, 0:width] = img2_color

# print(transformed_img[0][0])
# print(transformed_img[height*2-1][width*2-1])

# Save the output.
cv2.imwrite('output.jpg', trim(transformed_img))
# cv2.imwrite('output.jpg', transformed_img)
# cv2.imshow("output image", transformed_img)
# cv2.waitKey()
