
# Tensorflow.js

## Motivation

* No drivers
* Interactive
* Privacy
* JavaScript runs almost everywhere: (Browser , Server side, Desktop apps, Mobile)

## Workflow

Install tensorflowjs

```bash
pip install tensorflowjs
```

Convert savedmodel

```bash
tensorflowjs_converter \
    --input_format=keras_saved_model \
    /tmp/saved_models/linear/1555429677/
    /tmp/linear
```

Use the model

```html
<html>
<head>
<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest"></script> 
<scrip>
    const run = async () => {
        const MODEL_URL = '<url>/model.json';
        const model = await tf.loadLayersModel(MODEL_URL);
        console.log(model.summary());
        const input = tf.tensor2d([10.0], [1, 1]);
        const result = model.predict(input);
        alert(result);
    }
    run();
</scrip>
</head>
<body>
</body>
</html>
```

## Example 1 body parts segmentation

```html
<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs"></script>
<script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/body-pix"></script>
```

```javascript
const net = await bodyPix.load();
const segmentation = await net.estimatePersonSegmentation(image);

// Result
{
  width: 640,
  height: 480,
  data: Uint8Array(307200) [0, 0, 1, ...]
}

// Built in rendering methods
bodyPix.drawPixelatedMask(...);
```

## Example 2 toxicity

```html
<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs"></script>
<script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/toxicity"></script>
```

```javascript
const net = await toxicity.load();
const segmentation = model.classify(['you suck']);

// Result
{
  "label": "identity_attack",
  "results" ..
}
```

## Example 3 Speech Commands

```html
<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs"></script>
<script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/speech-commands"></script>
```

```javascript
const vocabulary = 'directional4w'; // Up, down, left, right, background_noise, unknown
const recognizer = speechCommands.create('BROWSER_FFT', vocabulary);
await recognizer.ensureModelLoaded();
const words = recognizer.wordLabels();

recognizer.listen(result => {
    // We get a score for each word
    const maxScore = Math.max(...result.scores);
    const maxScoreIndex = result.scores.indexOf(maxScore);
    const detectedWord = words[maxScoreIndex];
    console.log(detectedWord, 'detected!');
}, config);
```

## Workflow
1. Python Model
2. TensorFlow.js Converter Tool
3. JavaScript App

## Layers API

### Import

```javascript
// import * as tf from '@tensorflow/tfjs';
// import * as tf from '@tensorflow/tfjs-node';
import * as tf from '@tensorflow/tfjs-node-gpu';
```

### Create Dataset

```javascript
const csvDataset = tf.data.csv(CSV_URL, {
    columnConfigs: {
        'price': { isLabel: true }
    }
});

const flattenedDataset = csvDataset
    .map(({xs, ys}) =>
        // Flatten deatures and labels
        ({xs: Object.values(xs), ys: Object.values(ys)}));

const dataset = flattenedDataset
    .shuffle()
    .batch(64)
```

### Create Model

```javascript
const model = tf.sequential();
model.add(tf.layers.conv2d({
    inputShape: [IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS],
    kernelSize: 5, filters: 8, strides: 1,
    activation: 'relu',
    kernelInitializer: 'varianceScaling'
}));

model.add(tf.layers.maxPooling2d({poolSize: [2, 2], strides: [2, 2]}));

model.add(tf.layers.flatten());
model.add(tf.layers.dense({units: NUM_CLASSES, activation: 'softmax'}));
```

### Train

```javascript
model.compile({
    loss: 'categoricalCrossentropy',
    optimizer: 'sgd'
});

// await model.fit(xs, ys, {epochs: 10});
await model.fitDataset(dataset, {epochs: 10});

await model.save('localstorage://my-js-model');

const prediction = model.predict(input);
```

## tfjs-vis

*In-browser visualization library*

```javascript
import * as tfvs from '@tensorflow/tfjs-vis';

model.fit(data, labels, {
    epochs: 10,
    callbacks: tfvis.show.fitCallbacks(
        {name: 'Training History'},
        ['loss', 'acc', 'val_loss', 'val_acc']),
});

tfvis.show.modelSummary({name: 'Model Summary'}, model);

tfvis.show.layer({name: 'Conv2D1 Details'}, model.getLayer('conv2d_Conv2D1'))
```

###  Tensorboard

```javascript
import * as tfvs from '@tensorflow/tfjs-vis';

model.fit(xs, ys, {
    epochs: 10,
    callbacks: tf.node.tensorBoard('/tmp/logdir')
});

tfvis.show.modelSummary({name: 'Model Summary'}, model);

tfvis.show.layer({name: 'Conv2D1 Details'}, model.getLayer('conv2d_Conv2D1'))
```

## Sources

[TFJS @ TF Summit](https://www.youtube.com/watch?v=x35pOvZBJk8)

[TFJS Websize](https://tensorflow.org/js)

[Pretrained Models](https://github.com/tensorflow/tfjs-models)

[Code Examples](https://github.com/tensorflow/tfjs-examples)
