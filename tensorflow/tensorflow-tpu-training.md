
# TPU training


Tensorflow 1.14:
```python
import tensorflow as tf
tpu = tf.contrib.tpu.cluster_resolver.TPUClusterResolver()
tf.contrib.distribute.initialize_tpu_system(tpu)
strategy = tf.contrib.distribute.TPUStrategy(tpu, steps_per_run=100)
with strategy.scope():
    # standard tf.keras code here
    model = tf.keras.models.Sequential()
    # .. layers
    model.compile(...)
```
