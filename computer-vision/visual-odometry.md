
# Visual Odometry

**Visual Odometry** (VO) is the process of incrementally estimating the pose of the vehicle by examining the changes that motion induces on the images of its onboard cameras
* VO Pros:
    * Not affected by wheel slip in uneven terrain, rainy/snowy weather, or other adverse conditions
    * More accurate trajectory estimates compared to wheel odometry
* VO Cons:
    * Usually need an external sensor to estimate absolute scale
    * Camera is a passive sensor, might not be very robust against weather conditions and illumination changes
    * Any form of odometry (incremental state estimation) drifts over time

* Problem Formulation:
    * Given two consecutive images Ik-1 and Ik estimate the camera motion Tk
    * Concatenationg these single movements allows the recovery of the full trajectory of the camera, given frames C1 .. Cm


## Feature Detection

* Features are points of interest in an image
* They should have the following characteristics:
	* **Saliency**: distinctive, indentifiable and different from its immediate neighborhood
	* **Repeatability:** can be found in multiple images using same operations
	* **Locality:** occupies a relatively small subset of image space
	* **Quantity:** enough points represented in the image
	* **Efficiency:** reasonable computation time 

```python
orb = cv2.ORB_create()
kp = orb.detect(gray, None)
cv2.drawKeypoints(gray, kp, frame)
```

## Feature Description

* Summary of the image information around the detected feature
* They should have the following characteristics:
    * **Repeatability:** manifested as robustness and invariance to translation, rotation, scale and illumination changes
    * **Distinctiveness:** should allow us to distinguish between two close by features, very important for matching later on
    * **Compactness & Efficiency:** reasonable computation time

```python
kp, des = orb.compute(img, kp)
```

## Feature Matching

* Define a distance function d(fi, fj) that compares two descriptors
* Define distance ratio threshold p
* For every feature fi in Image 1:
    * Compute d(fi, fj) with all features fj in image 2
    * Find the closest match fc and the second closest match fs
    * Compute the distance ratio d(fi, fc)/d(di,fs)
    * Keep matches with distance ratio < p
* Might not be fast enough for extremly large amounts of features
* Use a multidimensional search tree, usually a k-d tree to speed the search by constraining it spatially

### Brute Force

```python
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# Hamming because its ORB
# crossCheck for better results
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)
```

### K-D tree based

```python
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# FLANN parameters for ORB
FLANN_INDEX_KDTREE = 0
index_params= dict(algorithm=FLANN_INDEX_LSH,
                   table_number=6,      # 12
                   key_size=12,         # 20
                   multi_probe_level=1) #2
search_params = dict(checks=50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1, des2, k=2)
```

### Handling Ambiguity in Matching

```python
good = []
for m,n in matches:
    if m.distance < 0.7*n.distance:
        good.append(m)
```

### Outlier Rejection 

RANSAC (Random Sample Consensus) Algorithm:

* Initialization:
    1. Given a Model, find the smallest number of samples M from which the model can be computed
* Main Loop:
    1. From your data, randomly select M samples
    2. Compute model parameters using the selected M samples
    3. Check how many samples from the rest of your data actually fits the model. We call this number the number of inliers C
    4. If C > inlier ratio threshold or maximum iterations reached, terminate and return the best inlier set. Else, go back to step i. 

## Motion Estimation

* Correspondence types:
    * **2D-2D:** both fk-1 and fk are defined in Image coordinates (used for tracking objects in image frame, visual tracking, image stabilization)
    * **3D-3D:** both fk-1 and fk are specified in 3D
    * **3D-2D:** fk-1 is specified in 3D and fk are their corresponding projection on 2D

### 3D-2D

* Perspective N point (PNP)
    * Solve for initial guess of [R|t] using Direct Linear Transform (DLT). It Forms a linear model and solves for [R|t] with methods such as SVD
    * Improve solution using Levenberg-Marquardt algorithm (LM)
    * Need at least 3 points to solve (P3P), 4 is we don't want ambiguous solutions. However the more features we have, the better

```python
# Solves for camera position given 3D points in frame k-1,
# their projection in frame k and the camera intrinsic calibration matrix
cv2.solvePnP()

# Same as above but uses RANSAC to handle outliers
cv2.solvePnPRansac()
```

# Sources

* Coursera Course: [Visual Perception for Self-Driving Cars](https://www.coursera.org/learn/visual-perception-self-driving-cars/lecture/V7iCJ/lesson-1-introduction-to-image-features-and-feature-detectors)
* OpenCV Documentation: [Feature Detectors](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_table_of_contents_feature2d/py_table_of_contents_feature2d.html), [Matcher](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_matcher/py_matcher.html), [solvePnP](https://docs.opencv.org/3.4.3/d9/d0c/group__calib3d.html#ga549c2075fac14829ff4a58bc931c033d), [solvePnPRansac](https://docs.opencv.org/3.4.3/d9/d0c/group__calib3d.html#ga50620f0e26e02caa2e9adc07b5fbf24e)
* Original implementation of the [FAST detector](https://www.edwardrosten.com/work/fast.html)
* [Camera Calibration Toolbox for Matlab](http://www.vision.caltech.edu/bouguetj/calib_doc/)
* [OCamCalib](https://sites.google.com/site/scarabotix/ocamcalib-toolbox): Omnidirectional Camera Calibration Toolbox for Matlab
* [FAB-MAP](http://www.robots.ox.ac.uk/~mjc/Software.htm): Visual-word-base loop detection
* [G2O](https://openslam-org.github.io/g2o): Library for graph-based nonlinear function optimization. Contains several variants of SLAM and bundle ajustment.
* [VisualSFM](http://ccwu.me/vsfm/): A Visual Structure from Motion System
* [COLMAP](https://demuc.de/colmap/): A general-purpose, end-to-end image-based 3D reconstruction pipeline