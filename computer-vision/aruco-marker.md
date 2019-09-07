
# Aruco Marker

## Prerequisites

OpenCV

```bash
mkdir -p $HOME/src
cd $HOME/src
wget https://github.com/opencv/opencv/archive/4.1.1.tar.gz
tar xvf 4.1.1.tar.gz
rm 4.1.1.tar.gz
wget https://github.com/opencv/opencv_contrib/archive/4.1.1.tar.gz
tar xvf 4.1.1.tar.gz
rm 4.1.1.tar.gz
cmake -DOPENCV_EXTRA_MODULES_PATH=$HOME/src/opencv_contrib-4.1.1/modules\
      -DCMAKE_BUILD_TYPE=RELEASE -DBUILD_EXAMPLES=OFF -DBUILD_DOCS=OFF\
      -DBUILD_PERF_TESTS=OFF -DBUILD_TESTS=OFF -DENABLE_PRECOMPILED_HEADERS=OFF ..
make -j4
sudo make install
```

## Create Marker

```python
import cv2

d = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# some other dicts:
# cv2.aruco.DICT_4X4_50
# cv2.aruco.DICT_4X4_100
# cv2.aruco.DICT_4X4_250
# cv2.aruco.DICT_4X4_1000

img = cv2.aruco.drawMarker(d, 0, 1000)
# 0 -> marker-id valid 0 .. 49
# 1000 -> marker-size in pixels

cv2.imwrite('img.png', img)
```
Example Output:

<img src="./images/aruco-marker-example.png" width="256">

## Detect Marker

```cpp
#include "opencv2/opencv.hpp"
#include "opencv2/aruco.hpp"

cv::Mat gray;
cv::cvtColor(image, gray, cv::COLOR_BGR2GRAY);

auto dictionary = cv::aruco::getPredefinedDictionary(cv::aruco::DICT_4X4_50);
std::vector<std::vector<cv::Point2f>> id_corners;
std::vector<int> ids;
auto detectorParams = cv::aruco::DetectorParameters::create();
std::vector<std::vector<cv::Point2f>> rejected;

cv::aruco::detectMarkers(gray, dictionary, id_corners, ids, detectorParams, rejected);

for (int i = 0; i < ids.size(); i++) {
	int id = ids[i];
    auto corners = id_corners[i];
}
```

