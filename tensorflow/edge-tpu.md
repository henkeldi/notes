
# Edge TPU

## Python

### Prerequisites

* [Edge TPU API](https://dl.google.com/coral/edgetpu_api/edgetpu_api_latest.tar.gz)

### Usage

*[edge_tpu_example.py:](scripts/edge_tpu_example.py)*
```python
from edgetpu.detection.engine import DetectionEngine
from PIL import Image
import cv2

cap = cv2.VideoCapture(0)
model = 'mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite'
engine = DetectionEngine(model)

while True:
    ret, frame = cap.read()
    if ret:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detection_results = engine.DetectWithImage(Image.fromarray(rgb))
        draw_bounding_boxes(frame, detection_results)
        cv2.imshow('', frame)
    k = cv2.waitKey(1)
    if k == 27:
        break
```

## C++

### Prerequisites

* [Edge TPU API](https://dl.google.com/coral/edgetpu_api/edgetpu_api_latest.tar.gz)
* Tensorflow Lite API

### Usage

*[edge_tpu_demo.cc:](scripts/edge_tpu_demo.cpp)*
```cpp
#include <iostream>

#include <opencv2/opencv.hpp>

#include "edge_tpu_cpp_demo/edgetpu.h"
#include "tensorflow/lite/interpreter.h"
#include "tensorflow/lite/kernels/register.h"
#include "tensorflow/lite/model.h"

int main(int argc, char* argv[]) {
  std::string model_path = "mobilenet_ssd.tflite";
  auto model = tflite::FlatBufferModel::BuildFromFile(model_path.c_str());

  std::unique_ptr<edgetpu::EdgeTpuContext> tpu_context =
    edgetpu::EdgeTpuManager::GetSingleton()->NewEdgeTpuContext();

  tflite::ops::builtin::BuiltinOpResolver resolver;
  resolver.AddCustom(edgetpu::kCustomOp, edgetpu::RegisterCustomOp());

  std::unique_ptr<tflite::Interpreter> interpreter;
  tflite::InterpreterBuilder builder(*model, resolver)(&interpreter);

  interpreter->SetExternalContext(kTfLiteEdgeTpuContext, tpu_context.get());
  interpreter->SetNumThreads(1);

  interpreter->AllocateTensors();

  auto input_tensor = interpreter->tensor(interpreter->inputs()[0]);
  auto output_locations = interpreter->tensor(interpreter->outputs()[0]);
  auto output_classes = interpreter->tensor(interpreter->outputs()[1]);
  auto output_scores = interpreter->tensor(interpreter->outputs()[2]);
  auto num_detections_ = interpreter->tensor(interpreter->outputs()[3]);

  auto cap = cv::VideoCapture(0);

  const int height = input_tensor->dims->data[1];
  const int width = input_tensor->dims->data[2];
  const int channels = input_tensor->dims->data[3];
  const int row_elems = width * channels;

  cv::Mat frame, resized;
  int k = -1;
  while (k == -1) {
    bool ret = cap.read(frame);
    if (ret) {
      cv::resize(frame, resized, cv::Size(width, height));
      uint8_t* dst = input_tensor->data.uint8;
      for (int row = 0; row < height; row++) {
        memcpy(dst, resized.ptr(row), row_elems);
        dst += row_elems;
      }
      interpreter->Invoke();
      const float* detection_locations = output_locations->data.f;
      const float* detection_classes = output_classes->data.f;
      const float* detection_scores = output_scores->data.f;
      const int num_detections = *(num_detections_->data.f);

      for (int i = 0; i < num_detections; i++) {
        const float score = detection_scores[i];
        const int ymin = detection_locations[4 * i + 0] * frame.rows;
        const int xmin = detection_locations[4 * i + 1] * frame.cols;
        const int ymax = detection_locations[4 * i + 2] * frame.rows;
        const int xmax = detection_locations[4 * i + 3] * frame.cols;
        if (score > .3f) {
          cv::rectangle(frame, cv::Rect(xmin, ymin, xmax - xmin, ymax - ymin),
            cv::Scalar(0, 0, 255), 3);
        }
      }
      cv::imshow("", frame);
    }
    k = cv::waitKey(1);
  }
  interpreter.reset();
  tpu_context.reset();
  return 0;
}
```

*CMakeLists.txt:*

```cmake
cmake_minimum_required(VERSION 3.10)
project(edge_tpu_demo)

SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -pthread")

find_package(OpenCV REQUIRED)

set(Tensorflow_DIR $ENV{Tensorflow_DIR})
set(EdgeTPU_API_DIR $ENV{EdgeTPU_API_DIR})

include_directories(
    include
    ${OpenCV_INCLUDE_DIRS}
    ${Tensorflow_DIR}
    ${Tensorflow_DIR}/tensorflow/lite/tools/make/downloads/flatbuffers/include)

link_directories(
    ${EdgeTPU_API_DIR}/libedgetpu
    ${Tensorflow_DIR}/tensorflow/lite/tools/make/gen/linux_x86_64/lib)

add_executable(edge_tpu_demo src/edge_tpu_demo.cpp)
target_link_libraries(edge_tpu_demo
    ${OpenCV_LIBRARIES}
    tensorflow-lite
    edgetpu_x86_64)
```

*build.sh*

```bash
export Tensorflow_DIR=/path/to/tensorflow-1.14.0
export OpenCV_DIR=/path/to/opencv-4.1.0/install/lib/cmake/opencv4
export EdgeTPU_API_DIR=/path/to/edgetpu_api

rm -r build
rm edge_tpu_demo
mkdir build
cd build
cmake ..
make -j4
mv ./edge_tpu_demo ..
```
