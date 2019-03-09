
# Tensorflow Extended

### Installation

```
pip install tfx
```

## Parts of the Pipeline

### ExampleGen

* Emits: tf.Example records

```python
from tfx.utils.dsl_utils import csv_input
from tfx.components import ExamplesGen

examples = csv_input(os.path.join(base_dir, 'no_split/span_1'))
examples_gen = ExamplesGen(input_data=examples)
```

### StatisticsGen

* Takes in Data and creates statistics

```python
from tfx import components

compute_eval_stats = components.StatisticsGen(
      input_data=examples_gen.outputs.eval_examples,
      name='compute-eval-stats')
```

### SchemaGen

* What you expect from your data, how it should look like, datatypes

```python
infer_schema = components.SchemaGen(stats=compute_training_stats.outputs.output)
```

### ExampleValidator

* Missing features, training serving skew, data distribution drift

```python
validate_stats = components.ExampleValidator(
      stats=compute_eval_stats.outputs.output,
      schema=infer_schema.outputs.output)
```

### Transform

* Transforms data, like scaling, map string to int, bucketize

```python
transform_training = components.Transform(
    input_data=examples_gen.outputs.training_examples,
    schema=infer_schema.outputs.output,
    module_file=taxi_pipeline_utils,
    name='transform-training')
```

### Trainer

```python
trainer = components.Trainer(
      module_file=taxi_pipeline_utils,
      train_files=transform_training.outputs.output,
      eval_files=transform_eval.outputs.output,
      schema=infer_schema.outputs.output,
      tf_transform_dir=transform_training.outputs.output,
      train_steps=10000,
      eval_steps=5000,
      warm_starting=True)
```

### Evaluator

* Assess overall model quality
* Assess model quality on specific segments / slices
* Track performance over time

```python
from tfx import components
import tensorflow_model_analysis as tfma

# For TFMA evaluation
taxi_eval_spec = [
    tfma.SingleSliceSpec(),
    tfma.SingleSliceSpec(columns=['trip_start_hour'])
]

model_analyzer = components.Evaluator(
      examples=examples_gen.outputs.eval_examples,
      eval_spec=taxi_eval_spec,
      model_exports=trainer.outputs.output)
```


### ModelValidator

* Avoid pushing models with degraded quality
* Avoid breaking downstream components (e.g. serving)

```python
from tfx import components
import tensorflow_model_analysis as tfma

# For model validation
taxi_mv_spec = [tfma.SingleSliceSpec()]

model_validator = components.ModelValidator(
      examples=examples_gen.outputs.output,
      model=trainer.outputs.output,
      eval_spec=taxi_mv_spec)
```

### Pusher

* If passed validation then copies the model to disk

```python
from tfx import components

pusher = components.Pusher(,
  model_export=trainer.outputs.output,
  model_blessing=model_validator.outputs.blessing,
  serving_model_dir=serving_model_dir)
```

## Tensorflow Serving

### Motivation

* Multi-tenancy (Multiple Versions on one Server)
* Optimize with GPU and TensorRT
* Expose gRPC or REST API
* Low-latency
* Request Batching
* Traffic Isolation
* Used for years at Google, millions of QPS
* Scale in minutes
* Dynamic version refresh

### Deploying REST API with Docker

```bash
docker run -p 8501:8501 -v '/path/to/savedmodel':/models/chicago_taxi -e MODEL_NAME=chicago_taxi -t tensorflow/serving
```

Run on GPU:

```bash
docker run --runtime=nvidia -p 8501:8501 -v '/path/to/savedmodel':/models/chicago_taxi -e MODEL_NAME=chicago_taxi -t tensorflow/serving:latest-gpu
```

Use TensorRT

```bash
saved_model_cli convert --dir '/path/to/savedmodel' --output_dir '/path/to/trt-savedmodel' --tag_set serve tensorrt
```
```bash
docker run --runtime=nvidia -p 8501:8501 -v '/path/to/trt-savedmodel':/models/chicago_taxi -e MODEL_NAME=chicago_taxi -t tensorflow/serving:latest-gpu
```

### Deploying REST API locally

```bash
apt-get install tensorflow-model-server
```
```bash
tensorflow_model_server --port=8501 --model_name=chicago_taxi --model_base_path='/path/to/savedmodel'
```

### Source
* [TF Extended Github](https://github.com/tensorflow/tfx)
* [TF Extended Documentation](https://tensorflow.org/tfx)
* [TF Extended @ TF Summit](https://www.youtube.com/watch?v=0O201IQlkxc)
