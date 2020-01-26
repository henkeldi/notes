import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import time

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from tensorflow.keras import backend as K

imdb, info = tfds.load("imdb_reviews", with_info=True, as_supervised=True)

vocab_size = 10000
oov_tok = "<OOV>"
padding_type = "post"
trunc_type = "post"
max_length = 120
num_epochs = 50
embedding_dim = 16

train_data, test_data = imdb['train'], imdb['test']

training_sentences = []
training_labels = []

testing_sentences = []
testing_labels = []

for s,l in train_data:
  training_sentences.append(str(s.numpy()))
  training_labels.append(l.numpy())

for s,l in test_data:
  testing_sentences.append(str(s.numpy()))
  testing_labels.append(l.numpy())

training_labels_final = np.array(training_labels)
testing_labels_final = np.array(testing_labels)

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(training_sentences)

word_index = tokenizer.word_index

training_sequences = tokenizer.texts_to_sequences(training_sentences)
training_padded = pad_sequences(training_sequences, maxlen=max_length,
    padding=padding_type, truncating=trunc_type)

testing_sequences = tokenizer.texts_to_sequences(testing_sentences)
testing_padded = pad_sequences(testing_sequences, maxlen=max_length,
    padding=padding_type, truncating=trunc_type)


def create_model(name):
    if name == 'simple':
        return tf.keras.Sequential([
            tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(6, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
    elif name == 'lstm':
        return tf.keras.Sequential([
            tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
            tf.keras.layers.Dense(6, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
    elif name == 'gru':
        return tf.keras.Sequential([
            tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
            tf.keras.layers.Bidirectional(tf.keras.layers.GRU(32)),
            tf.keras.layers.Dense(6, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
    elif name == 'conv':
       return tf.keras.Sequential([
            tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
            tf.keras.layers.Conv1D(128, 5, activation='relu'),
            tf.keras.layers.GlobalAveragePooling1D(),
            tf.keras.layers.Dense(6, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

model_names = ['simple', 'conv', 'lstm', 'gru']
model_stats = {}

for model_name in model_names:
    model = create_model(model_name)
    model.summary()
    trainable_param_count = int(
        np.sum([K.count_params(p) for p in model.trainable_weights]))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    t0 = time.time()
    history = model.fit(
        training_padded, training_labels_final,
        epochs=num_epochs,
        validation_data=(testing_padded, testing_labels_final))
    dt = time.time() - t0
    model_stats[model_name] = {
        'trainable_param_count': trainable_param_count,
        'history': history.history,
        'training_time': dt
    }
    tf.keras.backend.clear_session()
    np.save(f"{model_name}.npy", model_stats[model_name])


# Print results

fig = plt.figure(figsize=(10.0, 10.0))
plt.title("Comparison of different network archituectures on imdb dataset")

plt.subplot(3, 2, 1)
plt.title('Training Accuracy')
for model_name, stats in model_stats.items():
    print(model_name)
    print(stats['history'])
    plt.plot(stats['history']['accuracy'], label=model_name)
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")

plt.ylim([0.75, 1.0])
plt.legend()

plt.subplot(3, 2, 2)
plt.title('Validation Accuracy')
for model_name, stats in model_stats.items():
    print(model_name)
    print(stats['history'])
    plt.plot(stats['history']['val_accuracy'], label=model_name)
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")

plt.legend()
plt.ylim([0.75, 1.0])

plt.subplot(3, 2, 3)
plt.title('Training Loss')
for model_name, stats in model_stats.items():
    print(model_name)
    print(stats['history'])
    plt.plot(stats['history']['loss'], label=model_name)
    plt.xlabel("Epochs")
    plt.ylabel("Loss")

plt.ylim([ 0.0, 3.5])
plt.legend()

plt.subplot(3, 2, 4)
plt.title('Validation Loss')
for model_name, stats in model_stats.items():
    print(model_name)
    print(stats['history'])
    plt.plot(stats['history']['val_loss'], label=model_name)
    plt.xlabel("Epochs")
    plt.ylabel("Loss")


plt.legend()
plt.ylim([ 0.0, 3.5])

plt.subplot(3, 2, 5)
data = [s['training_time'] / 50 for n, s in model_stats.items()]
names = [n for n, s in model_stats.items()]

plt.title('Training time')
X = np.arange(len(names))

rects = plt.bar(X, data, align='center')
for val, rect in zip(data, rects):
    height = rect.get_height()
    plt.gca().text(rect.get_x() + rect.get_width()/2.,
                   height+0.0125,
                   '{:.2f}'.format(val),
                   ha='center',
                   va='bottom')

plt.xticks(X, names, rotation=30., ha='right')

ylim_upper = np.ceil(max(data) * 1000.0) / 1000.0 + 10.0
plt.ylim([0, ylim_upper])
plt.ylabel('Training time [s] / Epoch')


plt.subplot(3, 2, 6)
data = [s['trainable_param_count'] for n, s in model_stats.items()]
names = [n for n, s in model_stats.items()]

plt.title('Parameter count')
X = np.arange(len(names))

rects = plt.bar(X, data, align='center')
for val, rect in zip(data, rects):
    height = rect.get_height()
    plt.gca().text(rect.get_x() + rect.get_width()/2.,
                   height+0.0125,
                   '{:.2f}'.format(val),
                   ha='center',
                   va='bottom')

plt.xticks(X, names, rotation=30., ha='right')

ylim_upper = np.ceil(max(data) * 1000000.0) / 1000000.0 + 100000.0
plt.ylim([0, ylim_upper])
plt.ylabel('#Parameter')

plt.tight_layout()
plt.savefig("plot.svg")

plt.show()
