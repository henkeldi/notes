
# Tensorflow API C++

## Prerequisites

<details><summary>CUDA</summary>

[Link](https://developer.nvidia.com/Cuda-Toolkit-archive)

</details>

<details><summary>CUDNN</summary>

[Link](https://developer.nvidia.com/rdp/cudnn-download)

</details>

<details><summary>Bazel</summary>

* Check which version tensorflow needs [here](https://www.tensorflow.org/install/source#gpu). Bazel releases are [here](https://github.com/bazelbuild/bazel/releases).

```sudo apt install openjdk-14-jdk```

```bash
wget https://github.com/bazelbuild/bazel/releases/download/3.1.0/bazel-3.1.0-dist.zip
unzip bazel-3.1.0-dist.zip -d bazel-3.1.0-dist
cd bazel-3.1.0-dist
./compile.sh
```
</details>

<details><summary>Tensorflow</summary>

```bash
wget https://github.com/tensorflow/tensorflow/archive/v2.1.0-rc1.tar.gz
tar xvf v2.1.0-rc1.tar.gz
cd v2.1.0-rc1

export TF_PYTHON_VERSION='python3.6'
export TF_NEED_GCP=0
export TF_NEED_HDFS=1
export TF_NEED_S3=0
export TF_NEED_CUDA=1
export TF_CUDA_VERSION=10.1
export TF_CUDNN_VERSION=7
export TF_NEED_TENSORRT=1
export CC_OPT_FLAGS='-mavx'
export PYTHON_BIN_PATH=$(which ${TF_PYTHON_VERSION})
export PYTHON_LIB_PATH=/usr/local/lib/${TF_PYTHON_VERSION}/dist-packages
export LD_LIBRARY_PATH="/usr/local/cuda:/usr/local/cuda/lib64"
export TF_CUDA_COMPUTE_CAPABILITIES=5.2
export TF_ENABLE_XLA=1
export TF_NEED_OPENCL_SYCL=0
export TF_NEED_ROCM=0
export TF_NEED_CUDA=1
export TF_NEED_TENSORRT=1
export TF_CUDA_CLANG=0
export GCC_HOST_COMPILER_PATH=/usr/bin/gcc
export TF_SET_ANDROID_WORKSPACE=0

./configure

bazel build --config=monolithic --config=opt --config=v2 --config=cuda --config=noaws --config=nogcp --config=nonccl //tensorflow:libtensorflow_cc.so
```
</details>

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

