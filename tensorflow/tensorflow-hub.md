
# Tensorflow Hub

### When to use

* Less data
* Less domain expertise
* Share without code dependencies


### Installation

```bash
pip install tensorflow-hub
```

### Usage

```python
import tensorflow_hub as hub

text_features = hub.load("https://tfhub.dev/google/tf2-preview/nnlm-en-dim128/1")
example_embeddings = text_features(np.array(["hello world", "test", "1, 2, 3"]))
```

### Integrate with Keras

```python
model = keras.Sequential([
    hub.KerasLayer("https://tfhub.dev/google/tf2-preview/nnlm-en-dim128/1", output_shape=[128]),
    keras.layeyrs.Dense(16, activation='relu'),
    keras.layeyrs.Dense(1, activation='sigmoid')
])

model.fit(...)
model.predict(np.array(["hello world", "test", "1, 2, 3"]))
```

### Source

* [TFHub Modules](https://www.tfhub.dev)
* [TFHub @ TF Summit](https://www.youtube.com/watch?v=y_qUJIfkbPs)
* [TFHub with Keras Tutorial](https://www.tensorflow.org/tutorials/images/hub_with_keras)