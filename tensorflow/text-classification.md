
# Text Classification

## Intent detection

* Uses Universal sentence encoder from Google (NLU in a box, Sentence to Vector)

```javascript
const use = require('@tensorflow-models/universal-sentence-encoder');
const model = await use.load();

// Embed an array of sentences.
const sentences = ['Your cellphone looks great.', 'What is the weather now?'];
const embeddings = await model.embed(sentences)

// 'embeddings' is a tensor consisting of the 512 numbers for each sentence
embeddings.print(); // [341, 4125, 8, 140, 31, 19, 54, ...],]
```

* Convert Intents to numbers with one hot encoding

PlayMusic -> \[0, 1, 0\]
AddtoPlayList -> \[0, 0, 1\]

```javascript
const tf = require('@tensorflow/tfjs')

const categories = ['GetWeather', 'PlayMusic', 'AddtoPlayList'];
const numCategories = categories.length;

// label is a tensor with the one-hot representation of 'GetWeather'
const label = tf.oneHot(categories.indexOf('GetWeather'), numCategories);
```

```javascript
const getModel = (labels) => {
    const EMBEDDING_DIMS = 512;
    const NUM_CLASSES = labels.length;
    
    const model = tf.sequential();
    model.add(tf.layers.dense({
        inputShape: [EMBEDDING_DIMS],
        units: NUM_CLASSES,
        activation: 'softmax',
    }));
    
    model.compile({
        optimizer: 'adam',
        loss: 'categoricalCrossentropy'
    })
    
    return model;
}
```

```javascript
const train = async (model, xs, ys, opts) {
    const {xsArr, ysArr} = loadJSON(dataPath);
    const metadata = loadJSON(metadataPath);

    const xs = tf.tensor(xsArr, metadata.xsShape);
    const ys = tf.tensor(ysArr, metadata.ysShape);

    const model = getModel(metadata.labels);

    // We use model.fit as the whole dataset comfortably fits in memory.
    await model.fit(xs, ys, { epochs, validationSplit });

    mkdirp(outputFolder);
    await model.save(fileIO.fileSystem(outputFolder));
}
```

```javascript
const classify = async (sentences) {
    const use = await loadUniversalSentenceEncoder();
    const model = await loadIntentClassifier(CUSTOM_MODEL_URL);
    const {labels} = await loadMetadata();

    const embeddings = await use.embed(sentences);
    const prediction = model.predict(embeddings);
    const predsArr = await prediction.array();

    tf.dispose([activations, prediction]);
    return predsArr;
}
```

## Entity extraction

Send every word through the sentence encoder. Make it a given length with \_\_PAD\_\_ token. Those are the **xs**.

The **ys** are TOK for non-entity words, ENT for entities and PAD for pad tokens.

Example: What is the weather in Cambridge MA? \_\_PAD\_\_

TOK, TOK, TOK, TOK, TOK, ENT, ENT, TOK, PAD

then one hot encode it:

\[1, 0, 0\], \[1, 0, 0\], \[1, 0, 0\], \[1, 0, 0\], \[1, 0, 0\], \[0, 1, 0\], \[0, 1, 0\], \[1, 0, 0\], \[0, 0, 1\]

```javascript
const getModel = (labels, embeddingDims = 512, sequenceLength) => {
    const NUM_CLASSES = labels.length;
    const model = tf.sequential();
    
    const lstmLayer = tf.layers.lstm({
        inputShape: [sequenceLength, embeddingDims],
        units: sequenceLength,
        recurrentInitializer: 'glorotNormal',
        returnSequences: true,
    });
    const bidirectionalLstm = tf.layers.bidirectional({layer: lstmLayer})
    model.add(bidirectionalLstm)
    
    model.add(tf.layers.timeDistributed(
        {layer: tf.layers.dense({units: NUM_CLASSES})}));
    model.add(tf.layers.activation({activation: 'softmax'})
    
    model.compile({
        optimizer: 'adam',
        loss: 'categoricalCrossentropy',
    });
    return model
}
```

## Stackoverflow Tag Prediction

Identify whether an stackoverflow post belongs to one of this categories: \[TensorFlow, Keras, Matplotlib, Pandas, Scikit-learn\]

### Step 1. Preparing the data

Bigquery:

```sql
SELECT
  LOWER(CONCAT(title, " ", REGEXP_REPLACE(body, r"<[^>]*>", ""))),
  REPLACE(tags, "|", ",") AS tags
FROM `igquery-public-data.stackoverflow.posts_questions`
WHERE REGEXP_CONTAINS(tags, r"(?:tensorflow|keras|matplotlib|pandas|scikit-learn)")
```

* Using bag of words model
* Take the most occurring words in the text, that is the vocabulary

# Source

* [Google IO 2019 Video](https://youtu.be/D7ZL45xS39I)
* [Code](https://github.com/tensorflow/tfjs-examples/tree/master/intent-classifier)

* [Google IO 2019 Stackoverflow Classifier](https://www.youtube.com/watch?v=_RPHiqF2bSs)
* [Stackoverflow Classifier Code](https://github.com/GoogleCloudPlatform/ai-platform-text-classifier-shap)