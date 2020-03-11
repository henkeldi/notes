
# Tensorflow Dev Summit 2020

* [Data and Deployment Course Coursera](https://www.coursera.org/specializations/tensorflow-data-and-deployment)

* [Certificate](tensorflow.org/certificate)

#  Learning to Read with TensorFlow and Keras 

```python
lines = tf.data.TextLineDataset('CBTest/data/cbt_train.txt')

for line in lines.take(3):
    print(line)
```

## Clean the data

```python
lines = lines.filter(lambda x: not tf.strings.regex_full_match(x, "_BOOK_TITLE_.*"))

punctuation = r'[!"#$%&()\*\+,-\./:;<=>?@[\\\]^_`{|}~\]'

lines = lines.map(lambda x: tf.strings.regex_replace(x, punctuation, ' '))
```

## Window the data

```python
words = lines.map(tf.strings.split)
wordsets = words.unbatch().batch(11)

for row in wordsets.take(3):
    print(row)
```

## Label the data

```python
def get_example_label(row):
    example = tf.strings.reduce_join(row[:-1], separator=' ')
    example = tf.expand_dims(example, axis=0)
    label = row[-1:]
    return example, label

data = wordsets.map(get_example_label)
data = data.shuffle(1000)
```

## Preprocess the data

```python
vocab_size = 5000
vectorize_layer = tf.keras.layers.experimental.preprocessing.TextVectorization(max_tokens=vocab_size, output_sequence_length=10)
```

```python
vocab_size = 5000
vectorize_layer.adapt(lines.batch(64))

vectorize_layer.get_vocabulary()[:5]
// [the and to a of]

vectorize_layer.get_vocabulary()[-5:]
// [jar isaac invented horrified herbs]
```

## Keras preprocessing

* Image preprocessing
* Feature preprocessing

```python
import tensorflow_addons as tfa
print(tfa__version__)
'0.8.3'

print(dir(tfa.seq2seq))

// ['AttentionMechanism', 'AttentionWrapper' ...]
```

## Subclassing a Model

```python
class EncoderDecoder(tf.keras.Model):
    def __init__(self, max_features=5000, embedding_dims=200, rnn_units=512):
        super().__init__()
        self.max_features = max_features
        self.vectorize_layer = tf.keras.layers.experimental.preprocessing.TextVectorization(max_tokens=vocab_size, output_sequence_length=10)

        self.encoder_embedding = tf.keras.layers.Embedding(max_features + 1, embedding_dims)
        self.lstm_layer = tf.keras.layers.LSTM(rnn_units, return_state=True)

        self.decoder_embedding = tf.keras.layers.Embedding(max_features + 1, embedding_dims)

        projection_layer = tf.keras.layers.Dense(max_features)
        self.decoder = tfa.seq2seq.BasicDecoder(decoder_cell, samples,      output_layer=projection_layer)
        self.attention = tf.keras.layers.Attention()
    
    def train_step(self, data):
        x, y = data[0], data[1]
        x = self.vectorize_layer(x)
        # The vectorize layer pads; labels only need the first val
        y = self.vectorize_layer(y)[:, 0:1]
        y_one_hot = tf.one_hot(y, self.max_features)

        with tf.GradientTape() as tape:
            inputs = self.encoder_embedding(x)
            encoder_outputs, state_h, state_c = self.lstm_layer(inputs)

            attn_output = self.attention([encoder_outputs, state_h])
            attn_output = tf.expand_dims(attn_output, axis=1)

            targets = self.decoder_embedding(tf.zeros_like(y))
            concat_output = tf.concat([targets, attn_output], axis=-1)

            outputs, _, _ = self.decoder(concat_output, initial_state=[state_h, state_c])
            
            gradients = tape.gradient(loss, trainable_variables)
            self.optimizer.apply_gradients(zip(gradients, trainable_variables))

            self.compiled_metrics.update_state(y_one_hot, y_pred)
            return {m.name: m.result() for m in self.metrics}
```

## Configure training

```python
model = EncoderDecoder()
model.compile(loss=tf.keras.losses.CategoricalCrossentropy(...),
    optimizer='adam',
    metrics=['accuracy'])
```

## Train

```python
model.fit(data.batch(256), epochs=45, callbacks=    [tf.keras.callbacks.ModelCheckpoint('text_gen')])
```

## KerasTuner

```python
import kerastuner as kt

def build_model(hp):
    model = EncoderDecoder(rnn_units=hp.Int('units', min_value=256, max_value=1100, step=256))

    model.compile(...)
    model.vectorize_layer.adapt(lines.batch(256))
    return model

tuner = kt.tuners.RandomSearch(build_model, objective='accuracy', ...,  project_name='text_generation')

tuner.search(data.batch(256), epochs=45, callbacks=[tf.keras.callbacks.ModelCheckpoint('text_gen')])
```

## Predict the next word

```python
def predict_step(self, data, select_from_top_n=1):
    x = data
    if isinstance(x, tuple) and len(x) == 2:
        x = x[0]
    y_pred = tf.squeeze(outputs.rnn_output, axis=1)
    choices = tf.gather_nd(top_n, indices)
    words = [vectorize_layer.get_vocabulary()[i] for i in choices]
    return words
```

## Predict many words

```python
def predict(self, string_in, num_steps=50, select_from_top_n=1):
    s = tf.compat.as_bytes(string_in).split(b' ')
    for _ in range(num_steps):
        windowed = [b' '.join(s[-10:])]
        pred = self.predict_step([windowed], select_from_top_n=select_from_top_n)
        s.append(pred[0])
    return b' '.join(s)
```

## Doin this at Google-scale

* tf.text
* KerasBert
* TFHub text modules

# TFHub

