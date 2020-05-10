# Neural Structured Learning

Jointly optimizes both features & structured signals for better models.

## Install

```bash
pip install --quiet neural-structured-learning
```

## Use

You need:

- Training samples with labels
- Batch of labeled samples with neighbors, Sample 1, neighbor 1 .. K, Sample 2, neighbor 1 .. K

```python
import neural_structured_learning as nsl

# Augment training data by merging neighbors into sample features.
nsl.tools.pack_nbrs('/tmp/train.tfr', '', '/tmp/graph.tsv', 
                    '/tmp/nsl_train.tfr', add_undirected_edges=True, max_nbrs=3)

# Extract features required for the model from the input.
train_dataset, test_dataset = make_datasets('/tmp/nsl_train.tfr', '/tmp/test.tfr')

# Create a base model -- sequential, functional, or subclass.
base_model = tf.keras.Sequential(...)

# Wrap the base model with graph regularization.
graph_config = nsl.configs.GraphRegConfig(
    neighbor_config=nsl.configs.GraphNeighborConfig(max_neighbors=3))
graph_model = nsl.keras.GraphRegularization(base_model, graph_config)

# compile, train, evaluate.
graph_model.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=['accuracy'])
graph_model.fit(train_dataset, epochs=5)
graph_model.evaluate(test_dataset)
```

## Example (Sentiment classification)

```python
import neural_structured_learning as nsl
import tensorflow as tf
import tensorflow_hub as hub

imdb = tf.keras.datasets.imdb
(pp_train_data, pp_train_labels), (pp_test_data, pp_test_labels) = imdb.load_data(num_words=10000)

pretrained_embedding = 'https//tfhub.dev/google/tf2-preview/gnews-swivel-20dim/1'
hub_layer = hub.KerasLayer(pretrained_embedding, input_shape=[], dtype=tf.string, trainable=True)

# Generate embeddings.
record_if = int(0)
with tf.io.TFRecordWriter('/tmp/imdb/embeddings.tfr') as writer:
    for word_vector in pp_train_data:
        text = decode_review(word_vector)
        sentence_embedding = hub_layer(tf.reshape(text, shape=[-1,]))
        sentence_embedding = tf.reshape(sentence_embedding, shape=[-1])
        write_embedding_example(sentence_embedding, record_id)
        record_id += 1
```

### Build graph and prepare graph input for NSL

```python
# Build a graph from embeddings.
nsl.tools.build_graph(['/tmp/imbd/embeddings.tfr'],
                       '/tmp/imdb/graph_80.tsv',
                       similarity_threshold=0.8)

# Create example features.
next_record_id = create_examples(pp_train_data, pp_train_labels,
                                 '/tmp/imdb/train_data.tfr',
                                 starting_record_id=0)
create_examples(pp_test_data, pp_test_labels,
                '/tmp/imdb/test_data.tfr',
                starting_record_id=next_record_id)

# Augment training data by merging neighbors into sample features.
nsl.tools.pack_nbrs('/tmp/imdb/train_data.tfr', '',
                    '/tmp/imdb/graph_80.tsv',
                    '/tmp/imdb/nsl_train_data.tfr',
                    add_undirected_edges=True, max_nbrs=3)
```

### Graph-regularized keras model

```python
# Extract features required for the model from the input.
train_ds, test_ds = make_datasets('/tmp/imdb/nsl_train_data.tfr',
                                  '/tmp/imdb/test_data.tfr')

# Create a base model -- sequential, functional, or subclass.
base_model = tf.keras.Sequential(...)

# Wrap the base model with graph regularization.
graph_config = nsl.configs.GraphRegConfig(
    neighbor_config=nsl.configs.GraphNeighborConfig(max_neighbors=3))
graph_model = nsl.keras.GraphRegularization(base_model, graph_config)

# Compile, train, and evaluate
graph_model.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=['accuracy'])
graph_model.fit(train_ds, epochs=5)
graph_model.evaluate(test_ds)
```

## Adversarial learning for image classification

- gen_adv_neighbor(...)
- apply_feature_mask(...)
- adv_regularizer(...)

Karas API

- AdversarialRegularization
- AdvNeighborConfig
- AdvRegConfig

```python
import neural_structured_learning as nsl

# Prepare data.
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# Create a base model -- sequential, functional, or subclass.
model = tf.keras.Sequential(...)

# Wrap the model with adversarial regularization.
adv_config = nsl.configs.make_adv_reg_config(multiplier=0.2, adv_step_size=0.05)
adv_model = nsl.keras.AdversarialRegularization(model, adv_config)

# Compile, train, and evaluate.
adv_model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuarcy'])
adv_model.fit({'features': x_train, 'label': y_train}, epochs=5)
adv_model.evaluate({'features': x_test, 'label': y_test})
```

# Source

- [Neural Structured Learning - Part 1: Framework overview](https://www.youtube.com/watch?v=N_IS3x5wFNI)
- [Neural Structured Learning - Part 2: Training with natural graphs](https://www.youtube.com/watch?v=pJRRdtJ-rPU)
- [Neural Structured Learning - Part 3: Training with synthesized graphs](https://www.youtube.com/watch?v=3RQqTTOY0U0)
- [Neural Structured Learning - Part 4: Adversarial learning for image classification](https://www.youtube.com/watch?v=Js2WJkhdU7k)
- [Open-source Interactive Semi-Supervised Learning tool like in Jeremy Howard TEDx talk
  ](https://www.reddit.com/r/MachineLearning/comments/4i9vjb/opensource_interactive_semisupervised_learning/)
