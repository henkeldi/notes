
## Install Tensorflow 2.0
```bash
pip3 install tensorflow
pip3 install -U tensorflow-datasets
```

## Tutorials

* [Deep Dream](https://www.bit.ly/mini-dream)
* [Style Transfer](https://www.tensorflow.org/alpha/tutorials/generative/style_transfer)
* [Pix2Pix](https://www.tensorflow.org/alpha/tutorials/generative/pix2pix)
* [Seq-to-seq](https://www.bit.ly/mini-nmt)
* [Neural Machine Translation with Attention](https://www.tensorflow.org/alpha/tutorials/text/nmt_with_attention)
* [Linear Regression](https://www.bit.ly/tf-linear)
* [Beginner Tutorial](https://www.tensorflow.org/alpha/tutorials/quickstart/beginner)

## Load Data

```python
import tensorflow_datasets as tfds
dataset = tfds.load('fashion_mnist', as_supervised=True)
# cifar10, coco2014, mnist, imagenet2012, open_images_v4

mnist_train, mnist_test = dataset['train'], dataset['test']

def scale(image, label):
    image = tf.cast(image, tf.float32)
    image /= 255
    return image, label

mnist_train = mnist_train.map(scale).batch(64)
mnist_test = mnist_test.map(scale).batch(64)
```

```python
ds = create_dataset()
ds = ds.map(preprocess, num_parallel_calls=10)
ds = ds.shuffle(1024).batch(128).repeat(10)
ds = ds.prefetch(10)
```

```python
class DatasetBuilder:
    # Source data -> Preprocessing files
    def download_and_prepare:

    # Preprocess files -> tf.data.Dataset
    def as_dataset:

    # Dataset metadata: features, stats, etc.
    def info:
        featuers = FeaturesDict({
            'image': Image(shape=(28, 28, 1), dtype=tf.uint8),
            'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=10)
        })
        total_num_examples = 70000,
        splits={
            'test': <tfds.core.SplitInfo num_examples=10000>,
            'train': <tfds.core.SplitInfo num_examples=60000>
        }
        supervised_keys=('image', 'label')
```

```python
ds = tfds.load("mnist", split="train")
for ex in tfds.as_numpy(ds):
    np_image, np_label = ex["image"], ex["label"]
```

## Train Model

```python
import tensorflow as tf

model = tf.keras.models.Sequential({
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu')
    tf.keras.layers.Dropout(0.2)
    tf.keras.layers.Flatten(10, activation='softmax')
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

tb_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)

model.fit(mnist_train, epochs=5,
          validation_data=[x_test, y_test],
          callbacks=[tb_callback]
          metrics=['accuracy'])

model.evaluate(mnist_test)
```

## Model subclassing
```python
class MyModel(tf.keras.Model):
  def __init__(self, num_classes=10):
  	super(MyModel, self).__init__(name='my_model')
  	self.dense_1 = layers.Dense(32, activation='relu')
  	self.dense_2 = layers.Dense(num_classes, activation='sigmoid')

  def call(self, inputs):
  	x = self.dense_1(inputs)
  	return self.dense_2(x)
```

## Distributed learning
```python
import tensorflow as tf

strategy = tf.distribute.MirroredStrategy()
# strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy()
# strategy = tf.distribute.experimental.TPUStrategy()

with strategy.scope():
    model = tf.keras.models.Sequential({
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512, activation=tf.nn.relu)
        tf.keras.layers.Dropout(0.2)
        tf.keras.layers.Flatten(10, activation=tf.nn.softmax)
    ])
```

## Save / Restore Model

```python
saved_model_path = tf.keras.experimental.export_saved_model(
    model, '/path/to/model')

new_model = tf.keras.experimental.load_from_saved_model(saved_model_path)

new_model.summary()
```

## Layers

```python
class Flip(tf.keras.layers.Layer):

    def __init__(self, pivot=0, **kwargs):
        super(Flip, self).__init__(**kwargs)
        self.pivot = pivot

    def call(self, inputs):
        return self.pivot - inputs

x = tf.keras.layers.Dense(units=10)(x_train)
x = Flip(pivot=100)(x)
```

## Optimizer
```python
tf.keras.optimizers.{ Adadelta, Adagrad, Adam, Adamax, Nadam, RMSprop, SGD }

optimizer = tf.keras.optimizers.Adadelta(clipvalue=0.)

optimizer.learning_rate = .3

config = optimizer.get_config()
optimizer2 = tf.keras.optimizers.Adadelta.from_config(config)
```

## Losses
```python
class AllIsLost(tf.keras.losses.Loss):
    def call(self, y_true, y_pred):
        y_true = math_ops.cast(y_true, y_pred.dtype)
        return tf.math.equal(y_pred, y_true)

model.compile('sgd', losses=[AllIsLost(),
                             'mse',
                             tf.keras.losses.Huber(delta=1.5)])
```

## Controlled training

```python
model = Model()

with tf.GradientTape() as tape:
	logits = model(images)
	loss_value = loss(logits, labels)

grads = tape.gradient(loss_value, model.trainable_variables)
optimizer.apply_gradients(zip(grads, model.trainable_variables))
```

## tf.function
```python
@tf.function
def f(x):
    while tf.reduce_sum(x) > 1:
        x = tf.tanh(x)
    return x

f(tf.random.uniform([10]))
```

## Benefits of a graph

* Robust program serialization
* Easy distribution
* Distributed computation
* Optimization on the graph
* TPUs benefit from optimization

## Tensorboard

```python
tb_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)

model.fit(mnist_train, epochs=5,
          validation_data=[x_test, y_test],
          callbacks=[tb_callback]
          metrics=['accuracy'])
```

## Useful links
* [TensorFlow 2.0 Alpha](https://www.tensorflow.org/alpha)
* [Tensorflow 2.0 Documentation](https://www.tensorflow.org/r2.0)
* [Track Tensorflow Development](https://www.github.com/orgs/tensorflow/projects/4)
* [Medium Blog](https://medium.com/tensorflow)
* [Udacity Course](https://www.udacity.com/tensorflow)
* [Coursera Course](https://www.coursera.org/learn/introduction-tensorflow)
