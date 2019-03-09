
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
* Unsupported semantics

## Keras-based quantization API

```
model = tf.keras.models.Sequential({
    tf.keras.layers.Flatten(),
    quantize.Quantize(tf.keras.layers.Dense(512, activation='relu')),
    tf.keras.layers.Dropout(0.2),
    quantize.Quantize(tf.keras.layers.Dense(10, activation='softmax'))
])
```

## Keras-based pruning API

```
model = tf.keras.models.Sequential({
    tf.keras.layers.Flatten(),
    prune.Prune(tf.keras.layers.Dense(512, activation='relu')),
    tf.keras.layers.Dropout(0.2),
    prune.Prune(tf.keras.layers.Dense(10, activation='softmax'))
])
```

## Add GPU Support

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

## Sources

[TF Lite Documentation](https://tensorflow.org/lite)

[TF Lite Talk @ TF Summit](https://www.youtube.com/watch?v=DKosV_-4pdQ)

[Corel Dev Board](https://aiyprojects.withgoogle.com/edge-tpu)