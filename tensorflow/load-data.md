
# Tensorflow Dataset

## From Numpy Array

```python
def data_parser(sample):
    x = sample['x']
    y = tf.one_hot(sample['label'], total_words)
    return (x, y)

dataset = tf.data.Dataset.from_tensor_slices({'x': xs, 'label': labels})\
    .map(data_parser)\
    .batch(1024)\
    .prefetch(10)
```

## TFRecord

### Create TFRecord

```python
import tensorflow as tf
import numpy as np
import os
from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string('output_dir', './data/tfrecord', 'Root directory to raw face dataset.')
flags.DEFINE_integer('num_shards', '10', 'Number of tfrecord shards')


def create_example(i):
    x = [float(a) for a in xs[i]]
    label = labels[i]
    feature = {
        'x': tf.train.Feature(float_list=tf.train.FloatList(value=x)),
        'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[label]))
    }
    return tf.train.Example(features=tf.train.Features(feature=feature))


def create_tf_record(record_base_path, num_shards, N):
    writers = [tf.io.TFRecordWriter('{}-{:05d}-of-{:05d}'.format(record_base_path, i, num_shards))
        for i in range(num_shards)]
    writer_idx = 0
    for i in range(N):
        tf_example = create_example(i)
        writers[writer_idx].write(tf_example.SerializeToString())
        writer_idx = (writer_idx + 1) % num_shards
    (w.close() for w in writers)


def main(argv):
    del argv
    train_output_path = os.path.join(FLAGS.output_dir, 'data.record')
    if not os.path.exists(FLAGS.output_dir):
        os.makedirs(FLAGS.output_dir)

    N = xs.shape[0]

    create_tf_record(
        train_output_path,
        FLAGS.num_shards,
        N)


if __name__ == '__main__':
    app.run(main)
```

### Use TFRecord

```python
feature_description = {
    'x': tf.io.FixedLenFeature([max_sequence_len-1], tf.float32),
    'label': tf.io.FixedLenFeature([], tf.int64)
}

def data_parser(proto):
    sample = tf.io.parse_single_example(proto, feature_description)
    x = sample['x']
    y = tf.one_hot(sample['label'], total_words)
    return (x, y)

tfrecords = glob.glob('./data/tfrecord/data.record*')
dataset = tf.data.TFRecordDataset(tfrecords)\
    .shuffle(10000)\
    .map(data_parser)\
    .batch(1024)\
    .prefetch(10)
```

### Create TFRecord Example for images

```python
def create_example(image_path):
    img_name = image_path[image_path.rindex('/')+1:image_path.rindex('.')]
    img_root = image_path[:image_path.rindex('/')+1]
    mat_file_path = os.path.join(img_root, img_name + '.mat')

    mat = sio.loadmat(mat_file_path)
    pt2d = mat['pt2d']

    xmin = int(min(pt2d[0,:]))
    ymin = int(min(pt2d[1,:]))
    xmax = int(max(pt2d[0,:]))
    ymax = int(max(pt2d[1,:]))
    pitch, yaw, roll, = mat['Pose_Para'][0][:3]

    image_string = open(image_path, 'rb').read()
    H, W, C = tf.image.decode_jpeg(image_string).shape[:3]
    feature = {
        'filename': tf.train.Feature(bytes_list=tf.train.BytesList(value=[image_path.encode('utf-8')])),
        'height': tf.train.Feature(int64_list=tf.train.Int64List(value=[H])),
        'width': tf.train.Feature(int64_list=tf.train.Int64List(value=[W])),
        'depth': tf.train.Feature(int64_list=tf.train.Int64List(value=[C])),
        'pitch': tf.train.Feature(float_list=tf.train.FloatList(value=[pitch])),
        'yaw': tf.train.Feature(float_list=tf.train.FloatList(value=[yaw])),
        'roll': tf.train.Feature(float_list=tf.train.FloatList(value=[roll])),
        'bbox/xmin': tf.train.Feature(int64_list=tf.train.Int64List(value=[xmin])),
        'bbox/ymin': tf.train.Feature(int64_list=tf.train.Int64List(value=[ymin])),
        'bbox/xmax': tf.train.Feature(int64_list=tf.train.Int64List(value=[xmax])),
        'bbox/ymax': tf.train.Feature(int64_list=tf.train.Int64List(value=[ymax])),
        'image_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[image_string]))
    }
    return tf.train.Example(features=tf.train.Features(feature=feature))
```

### Use TFRecord for images

```python
image_feature_description = {
    'filename': tf.io.FixedLenFeature([], tf.string),
    'height': tf.io.FixedLenFeature([], tf.int64),
    'width': tf.io.FixedLenFeature([], tf.int64),
    'depth': tf.io.FixedLenFeature([], tf.int64),
    'pitch': tf.io.FixedLenFeature([], tf.float32),
    'yaw': tf.io.FixedLenFeature([], tf.float32),
    'roll': tf.io.FixedLenFeature([], tf.float32),
    'bbox/xmin': tf.io.FixedLenFeature([], tf.int64),
    'bbox/ymin': tf.io.FixedLenFeature([], tf.int64),
    'bbox/xmax': tf.io.FixedLenFeature([], tf.int64),
    'bbox/ymax': tf.io.FixedLenFeature([], tf.int64),
    'image_raw': tf.io.FixedLenFeature([], tf.string)
}

def data_parser(proto):
    sample = tf.io.parse_single_example(proto, image_feature_description)
    image_decoded = tf.image.decode_jpeg(sample['image_raw'], channels=3)

    image_decoded = tf.image.resize(image_decoded, (224, 224))

    image_decoded = tf.cast(image_decoded, tf.float32)
    image_decoded /= 255

    label = tf.stack([sample['pitch'], sample['yaw'], sample['roll']]) 

    return (image_decoded, label)

train_dataset = raw_train_dataset\
    .shuffle(256)\
    .map(data_parser)\
    .batch(16)\
```
