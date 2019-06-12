import tensorflow as tf
import numpy as np

from tensorflow.python.platform import tf_logging
tf_logging.set_verbosity(tf_logging.ERROR)
print(tf.__version__)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=1, input_shape=[1])
])

model.compile(loss='mean_squared_error',
              optimizer=tf.keras.optimizers.Adam(0.1))

xs = np.array([-40, -10, 0, 8, 15, 22, 38], dtype=float)
ys = np.array([-40, 14, 32, 46, 59, 72, 100], dtype=float)

model.fit(xs, ys, epochs=500)

saved_model_path = '/tmp/saved_models/f2c'

print model.predict([100.0])

tf.keras.experimental.export_saved_model(model, saved_model_path)

saved_model_dir = "/tmp/saved_models/f2c/1555429677/"

converter = tf.lite.TFLiteConverter.from_saved_model(model)

tflite_model = converter.convert()

open("/tmp/model.tflite", "wb").write(tflite_model)
