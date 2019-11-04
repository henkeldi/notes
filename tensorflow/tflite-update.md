
# Bert

Method of pretraining language representations which obtain SOA on a wide range of NLP tasks.
 
Mobile BERT
* < 100 ms latency (4.4x faster)
* < 100 MB size (77% reduction)
* same accuracy

TF Lite Support Library
* Android
* iOS

```java
// 1. Load your model
MyImageClassifier classifier = new MyImageClassifier(activity);
MyImageClassifier.Inputs inputs = classifier.createInputs();

// 2. Transform your data.
inputs.loadImage(rgbFrameBitmap);

// Run inference.
MyimageClassifier.Outputs outputs = classifier.run(inputs);

// 4. Use the resulting output.
Map<String, float> labeledProbabilities = outputs.getOutput();
```

# Convert custom model

```python
model = build_your_model()
tf.keras.experimental.export_saved_model(model, saved_model_dir)

# Convert Keras model to TensorFlow Lite model.
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)

# Use new converter
# * Better debuggabilty, source file location identification, control flow support
converter.experimental_new_converter = True

converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILDINS,
									   tf.lite.OpsSet.SELECT_TF_OPS]

tflite_model = converter.convert()
open("converted_model.tflite", "wb").write(tf_model)
```

# TF Lite interpreter
```kotlin
private fun initializeInterpreter() {
	val model = loadModelFile(context.assets)

	val delegate = new GpuDelegate()
	// delegate = new NnApiDelegate()
	tfliteOptions.addDelegate(delegate)

	this.interpreter = Interpreter(model, tfliteOptions)
}

private fun classify(bitmap: Bitmap): String {
	val resizedImage = Bitmap.createScaledBitmap(bitmap, ...)
	val inputByteBuffer = convertBitmapToByteBuffer(resizedImage)
	val output = Array(1) { FloatArray(OUTPUT_CLASSES_COUNT) }

	this.interpreter?.run(inputByteBuffer, output)
}
```

# Per-op Profiling

* Identify performance bottlenecks

```bash
bazel build -c opt \
	--config=android_arm64 --cxxopt='--std=c++11' \
	--copt=-DTFLITE_PROFILING_ENABLED \
	//tensorflow/lite/tools/benchmark:benchmark_model
```

```bash
adb push .../benchmark_model /data/local/tmp
adb shell taskset f0 /data/local/tmp/benchmark_model
```
