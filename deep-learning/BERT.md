
# BERT

*Bidirectional Encoder Representations from Transformers for Language*

Step 1: 
    * Take some text and drop 50 % of the words. Let the model predict the missing words.

Step 2:
    * Fine-tune this model on individual language tasks with small amounts of data.

# Training

```python
import tensorflow as tf
import tensorflow_datasets
import transformers

# Load tokenizer, model, dataset
tokenizer = transformers.DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = transformers.TFDistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')
data = tensorflow_datasets.load("glue/mrpc")

# Prepare dataset for GLUE
train_set = transformers.glue_convert_examples_to_features(data['train'], tokenizer, task='mrpc')
valid_set = transformers.glue_convert_examples_to_features(data['validation'], tokenizer, task='mrpc')
train_set, valid_set = train_set.shuffle(100).batch(32).repeat(2), valid_set.batch(64)

# Compile model for training
optimizer = tf.keras.optimizers.Adam(learning_rate=3e-5, epsilon=1e-0.8, clipnorm=1.0)
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
metric = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')
model.compile(optimizer=optimizer, loss=loss, metrics=[metric])

# Train model
model.fit(train_set, epochs=2, steps_per_epoch=115, validation_data=valid_set, validation_steps=7)

model.save_pretrained('./save/')
```

# Prediction (classification)

```python
import tensorflow as tf
import tensorflow_datasets
import transformers

# Load pretrained tokenizer and fine-tuned model
tokenizer = transformers.DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = transformers.TFDistilBertForSequenceClassification.from_pretrained('./save')

# Quickly test a few predictions - MRPC is a paraphrasing task, let's see if our model learned the task
sentence_0 = 'This research was consistent with his findings.'
sentence_1 = 'His findings were compatible with this research.'

inputs = tokenizer.encode_plus(sentence_0, sentence_1, add_special_tokens=True, return_tensors='tf')

pred = model(inputs)[0].argmax().item()
print('Sentence 1 is', 'a' if pred else 'not a', 'paraphrase of sentence 0')
```

# Related work

*2017 - Transformer Model - [Attention Is All You Need](https://arxiv.org/pdf/1706.03762.pdf)*

Unlike recurrent model where that processes one token after the other the transformer model processes allows to proccess a bunch of text all at once in parallel.

# Source

* [Tensorflow World Keynote](https://youtu.be/MunFeX-0MD8?t=706)
* [BERT Paper](https://arxiv.org/pdf/1810.04805.pdf)
