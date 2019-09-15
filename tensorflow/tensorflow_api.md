
# Tensorflow API C++

**Building the library:**

```bash
bazel build --config=cuda --config=v2 //tensorflow:libtensorflow_cc.so
```

**main.cpp:**

```c++
#include "opencv2/opencv.hpp"

#include "tensorflow/core/public/session.h"
#include "tensorflow/core/framework/tensor.h"
#include "tensorflow/cc/saved_model/loader.h"
#include "tensorflow/cc/saved_model/tag_constants.h"
#include "tensorflow/cc/saved_model/constants.h"
#include "tensorflow/core/lib/io/path.h"
#include "tensorflow/core/util/tensor_bundle/naming.h"

int main() {
  tensorflow::SessionOptions session_options;
  tensorflow::RunOptions run_options;
  tensorflow::SavedModelBundle bundle;
  const std::string export_dir;

  tensorflow::Status status = tensorflow::LoadSavedModel(
	session_options, run_options, export_dir, {tensorflow::kSavedModelTagServe}, &bundle);

  if (!status.ok()) {
    std::cout << "Could not load model: " << export_dir << std::endl;
    std::abort();    
  }

  tensorflow::Session* session = bundle.session.release();

  tensorflow::Tensor input_tensor(tensorflow::DT_FLOAT, tensorflow::TensorShape({1, 224, 224, 3}));
  float *p = input_tensor.flat<float>().data();
  cv::Mat image(height, width, CV_32FC3, p);
  cv::Mat resized;
  // cv::resize(frame(fixed_rect), resized, cv::Size(width, height));
  // cv::cvtColor(resized, resized, cv::COLOR_RGB2BGR);
  resized.convertTo(image, CV_32FC3);

  std::vector<tensorflow::Tensor> outputs;
  // to get input and output tensor names run:
  // saved_model_cli show --dir <model-dir> --tag_set serve --signature_def serving_default
  status = recognizer_session->Run(
  	{{"serving_default_input_1:0", input_tensor}},
  	{"PartitionedCall:0"}, {}, &outputs);

  if (status.ok()) {
  	float* output = outputs[0].flat<float>().data();
  }
}
```

**CMakeLists.txt:**

```cmake

set(Tensorflow_DIR $ENV{Tensorflow_DIR})

find_package(OpenCV REQUIRED)

include_directories(
  ${Tensorflow_DIR}
  ${Tensorflow_DIR}/bazel-genfiles
  ${Tensorflow_DIR}/bazel-tensorflow/external/com_google_protobuf/src
  ${Tensorflow_DIR}/bazel-tensorflow/tensorflow/lite/tools/make/downloads/eigen
  ${Tensorflow_DIR}/bazel-tensorflow/tensorflow/lite/tools/make/downloads/absl
  ${Tensorflow_DIR}/tensorflow/lite/tools/make/downloads/flatbuffers/include
)

link_directories(
  ${Tensorflow_DIR}/bazel-bin/tensorflow)

add_executable(main main.cpp)

target_link_libraries(main
   ${OpenCV_LIBRARIES}
   dl
   rt
   tensorflow_cc
   ${Tensorflow_DIR}/bazel-bin/tensorflow/libtensorflow_framework.so.1.14.0)
```

