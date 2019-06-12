# -*- coding: utf-8 -*-
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import tf_sentencepiece

# Some texts of different lengths.
english_sentences = ["dog", "Puppies are nice.", "I enjoy taking long walks along the beach with my dog."]
german_sentences = ["Hund", "Welpen sind nett.", "Ich genieße lange Spaziergänge am Strand entlang mit meinem Hund."]

# Set up graph.
g = tf.Graph()
with g.as_default():
    text_input = tf.placeholder(dtype=tf.string, shape=[None])
    # https://storage.googleapis.com/tfhub-modules/google/universal-sentence-encoder-xling/en-de/1.tar.gz
    en_de_embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder-xling/en-de/1")
    embedded_text = en_de_embed(text_input)
    init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
g.finalize()

# Initialize session.
session = tf.Session(graph=g)
session.run(init_op)

# Compute embeddings.
# en_result = session.run(embedded_text, feed_dict={text_input: [english_sentences[0]]})
de_result = session.run(embedded_text, feed_dict={text_input: [german_sentences[2]]})
de_result = session.run(embedded_text, feed_dict={text_input: [german_sentences[2]]})
de_result = session.run(embedded_text, feed_dict={text_input: [german_sentences[2]]})
import time
t = time.time()
de_result = session.run(embedded_text, feed_dict={text_input: [german_sentences[2]]})
print time.time() - t

# Compute similarity. Higher score indicates greater similarity.
# similarity_score = np.dot(np.squeeze(en_result), np.squeeze(de_result))
print de_result.min(), de_result.mean(), de_result.max()
