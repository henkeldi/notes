
# Tensorflow Lite

*Framework for deploying ML on mobile devices and embedded systems*

## Motivation

* Lower latency
* Network connectivity
* Privacy preserving

## Challanges

* Reduce compute power
* Limited memory
* Battery constraints

## Workflow

1. Tensorflow (estimator or Keras)
2. Saved Model (+ Calibration Data)
3. TF Lite Converter
4. TF Lite Model

## Point of failure

* Limited ops
* Unsupported semantics (i.e. control-flow in RNNs)

## Getting started

### Jump start

1. [Use pretrained models](https://www.tensorflow.org/tflite/models)
2. [Retrain a model](https://codelabs.developers.google.com/codelabs/tensorflow-for-poets)
3. Get up and running

```java
// Load your model
tfliteModel = loadModelFile(activity)
tflite = new Interpreter(tfliteModel, tfliteOptions)

imgData = ByteBuffer.allocateDirect(
    DIM_BATCH_SIZE
    * getImageSizeX()
    * getImageSizeY()
    * DIM_PIXEL_SIZE
    * getNumBytesPerChannel())
imgData.order(ByteOrder.nativeOrder())

// Transforming data
convertBitmapToByteBuffer(bitmap)

// Run inference
tflite.run(imageData, labelProbarray)

# Use the resulting output
```

### Custom model

```python
import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
tflite_model = converter.convert()
open("converted_model.tflite", "wb").write(tflite_model)
```

#### Tensorflow Select

* Enables hundreds more ops from TensorFlow on CPU
* Caveat: Binary size increase (~6MB compressed)

```python
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)

converter.target_ops = [tf.lite.OpsSet.TFLITE_BUILDINS,
                        tf.lite.OpsSet.SELECT_TF_OPS]

tflite_model = converter.convert()
open("converted_model.tflite", "wb").write(tflite_model)
```

### Performance

* Utilize the TensorFlow Lite benchmark tooling
* Validate that the model gets the right accuracy, size & performance
* Utilize GPU acceleration via the Delegation API

#### Delegation APi

Android:

```java
tfliteModel = loadModelFile(activity)

// tfliteOptions.setUseNNAPI(true) or
tfliteGpuDelegate = new GpuDelegate()
tfliteOptions.addDelegate(tfliteGpuDelegate)

tflite = new Interpreter(tfliteModel, tfliteOptions)
```

C++:

```cpp
unique_ptr<Interpreter> interpreter;
InterpreterBuilder interpreter_builder(model, op_resolver);
interpreter_builder(&interpreter);

auto* delegate = NewTfLiteGpuDelegate(nullptr);
if(interpreter->ModifyGraphWithDelegate(delegate != KtfLiteOk) return false;

WriteToInputTensor(interpreter->typed_input_tensor<float>(0))
if(interpreter->Invoke() != kTfLiteOk) return false;
ReadFromOutputTensor(interpreter->typed_output_tensor<float>(0));

DeleteTfLiteGpuDelegate(delegate);
```


#### Per-op profiling command line

Build

```bash
bazel build -c opt \
  --config=android_arm64 \
  --cxxopt='--std=c++11' \
  --copt=-DTFLITE_PROFILING_ENABLED \
// tensorflow/lite/tools/benchmark:benchmark_model
```
Deploy
```bash
adb push .../benchmark_model /data/local/tmp
adb shell taskset f0 /data/local/tmp/benchmark_model
```

### Optimize

#### Quantization

* Huge speedup
* ~4x smaller size

*Achieved by reducing the precision of weights and activations in your graph*

```python
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)

converter.optimizations = [tf.lite.Optimize.OPTIMIZE_FOR_SIZE]

tflite_quant_model = converter.convert()
```

#### Keras-based quantization API

```python
model = tf.keras.models.Sequential({
    tf.keras.layers.Flatten(),
    quantize.Quantize(tf.keras.layers.Dense(512, activation='relu')),
    tf.keras.layers.Dropout(0.2),
    quantize.Quantize(tf.keras.layers.Dense(10, activation='softmax'))
])
```

#### Keras-based pruning API

```python
model = tf.keras.models.Sequential({
    tf.keras.layers.Flatten(),
    prune.Prune(tf.keras.layers.Dense(512, activation='relu')),
    tf.keras.layers.Dropout(0.2),
    prune.Prune(tf.keras.layers.Dense(10, activation='softmax'))
])
```

## TensorFlow Lite for Microcontrollers

[TensorFlow Lite for Microcontrollers](https://www.tensorflow.org/lite/microcontrollers/overview)

## Sources

[TF Lite @ Google IO 2019](https://www.youtube.com/watch?v=Jjm7MT6W0Dc)

[TF Lite Talk @ TF Summit](https://www.youtube.com/watch?v=DKosV_-4pdQ)

[TF Lite Documentation](https://tensorflow.org/lite)

[Corel Dev Board](https://aiyprojects.withgoogle.com/edge-tpu)