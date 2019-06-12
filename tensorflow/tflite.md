
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

0. [Super simple example](./scripts/tflite_sample.py)
1. [Use pretrained models](https://www.tensorflow.org/tflite/models)
2. [Retrain a model](https://codelabs.developers.google.com/codelabs/tensorflow-for-poets)
3. Get up and running

```kotlin
// Load your model
val tfliteModel = loadModelFile(activity)
val tfliteOptions = Interpreter.Options()

// tfliteOptions.setUseNNAPI(true)
// tfliteGpuDelegate = new GpuDelegate()
// tfliteOptions.addDelegate(tfliteGpuDelegate)
tfliteoptions.setNumThreads(1)

tflite = new Interpreter(tfliteModel, tfliteOptions)

val inputVal = floatArrayOf(100.f)
val outputVal = ByteBuffer.allocateDirect(4)
outputVal.order(ByteOrder.nativeOrder())

// Run inference
tflite.run(inputVal, outputVal)

// Use the resulting output
outputVal.rewind()
var prediction = outputVal.getFloat()
```

Android build.gradle:

```gradle
aaptOptions{
    noCompress "tflite"
}
dependencies {
    implementation 'org.tensorflow:tensorflow-lite'
}
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
std::unique_ptr<tflite::Interpreter> interpreter;
tflite::InterpreterBuilder(*model, resolver)(&interpreter);

auto* delegate = NewTfLiteGpuDelegate(nullptr);
if(interpreter->ModifyGraphWithDelegate(delegate != KtfLiteOk) return false;

// Get the index of first input tensor.
int input_tensor_index = interpreter->inputs()[0];
// Get the pointer to the input buffer.
uint8_t* ibuffer = interpreter->typed_tensor<uint8_t>(input_tensor_index);

// Get the index of first output tensor.
const int output_tensor_index = interpreter->outputs()[0];
// Get the pointer to the output buffer.
uint8_t* obuffer = interpreter->typed_tensor<uint8_t>(output_tensor_index);

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

## Edge TPU

```python
# Load the TensorFlow Lite model
engine = edgetpu.classification.engine.ClassificationEngine(args.model)
# engine = edgetpu.classification.engine.BasicEngine(args.model)
# engine = edgetpu.classification.engine.DetectionEngine(args.model)
# engine = edgetpu.classification.engine.ImprintingEngine(args.model)


# Grab input from a camera stream
input = np.frombuffer(stream.getValue(), dtype=np.uint8)

# Run inference
result = engine.ClassifyWithInputTensor(input, top_k=1)

# Annotate image with results
if results:
    camera.annotate_text = "%s %.2f" % (
        labels[results[0][0]], results[0][1])
```

## Microcontrollers

[TensorFlow Lite for Microcontrollers](https://www.tensorflow.org/lite/microcontrollers/overview)

```cpp
const tflite::Model* model = 
    ::tflite::GetModel(g_tiny_conv_micro_features_model_data);
    
// Pull in all the operation implementations we need
tflite::ops::micro::AllOpsResolver resolver;

// Create an area of memory to use for input, output and intermediate arrays
const int tensor_arena_size = 10 * 1024;
uint8_t tensor_arena[tensor_arena_size];
tflite::SimpleTensorAllocator tensor_allocator(tensor_arena,
                                               tensor_arena_size);

// Build an interpreter to run the model with
tflite::MicroInterpreter interpreter(model, resolver, &tensor_allocator,
                                     error_reporter);

// Get information about the memory area to use for the model's input.
TfLiteTensor* model_input = interpreter.input(0);

// Prepare to access the audio spectrograms from a microphone or other source
// that will provide the inputs to the neural network.
FeatureProvider feature_provider(kFeatureElementCount,
                                 model_input->data.uint8);

// Perform feature extraction and populate the input array
feature_provider.PopulateFeatureData(...);

// Run the model
TfLiteStatus invoke_status = interpreter.Invoke();

// Figure out the highest scoring category
TfLiteTensor* output = interpreter.output(0);
uint8_t top_category_score = 0;
for (int category_index = 0; category_index < kCategoryCount;
     ++category_index) {
  const uint8_t category_score = output->data.uint8[category_index];
  if (category_score > top_category_score) {
    top_category_score = category_score;
  }
}
```

## Sources

[TF Lite @ Google IO 2019](https://www.youtube.com/watch?v=Jjm7MT6W0Dc)

[TF Lite Talk @ TF Summit](https://www.youtube.com/watch?v=DKosV_-4pdQ)

[TF Lite Documentation](https://tensorflow.org/lite)

[Corel Dev Board](https://aiyprojects.withgoogle.com/edge-tpu)