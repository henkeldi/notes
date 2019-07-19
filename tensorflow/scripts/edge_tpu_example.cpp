#include <iostream>

#include <opencv2/opencv.hpp>

#include "edge_tpu_cpp_demo/edgetpu.h"
#include "tensorflow/lite/interpreter.h"
#include "tensorflow/lite/kernels/register.h"
#include "tensorflow/lite/model.h"


int main(int argc, char* argv[]) {
  std::string model_path =
    "./model/mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite";
  auto model = tflite::FlatBufferModel::BuildFromFile(model_path.c_str());
  if (!model) {
    std::cerr << "Fail to build FlatBufferModel from file: " << model_path
              << std::endl;
    std::abort();
  }

  std::unique_ptr<edgetpu::EdgeTpuContext> tpu_context =
    edgetpu::EdgeTpuManager::GetSingleton()->NewEdgeTpuContext();
  if (tpu_context == nullptr) {
    std::cerr << "Device cannot be found or open" << std::endl;
    std::abort();
  }

  tflite::ops::builtin::BuiltinOpResolver resolver;
  resolver.AddCustom(edgetpu::kCustomOp, edgetpu::RegisterCustomOp());

  std::unique_ptr<tflite::Interpreter> interpreter;
  tflite::InterpreterBuilder builder(*model, resolver);
  if (builder(&interpreter) != kTfLiteOk) {
    std::cerr << "Failed to create interpreter" << std::endl;
    std::abort();
  }

  interpreter->SetExternalContext(kTfLiteEdgeTpuContext, tpu_context.get());
  interpreter->SetNumThreads(1);

  if (interpreter->AllocateTensors() != kTfLiteOk) {
    std::cerr << "Failed to allocate tensors." << std::endl;
    std::abort();
  }

  auto input_tensor = interpreter->tensor(interpreter->inputs()[0]);
  auto output_locations = interpreter->tensor(interpreter->outputs()[0]);
  auto output_classes = interpreter->tensor(interpreter->outputs()[1]);
  auto output_scores = interpreter->tensor(interpreter->outputs()[2]);
  auto num_detections_ = interpreter->tensor(interpreter->outputs()[3]);

  auto cap = cv::VideoCapture(0);

  if (!cap.isOpened()) {
    std::cout << "Could not open VideoStream" << std::endl;
    std::abort();
  }

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
