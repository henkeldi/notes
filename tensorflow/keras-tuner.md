
# Keras Tuner

*Hypertuning for humans*

## Example

A basic MNIST model
```python
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, 5, padding='same', activation='relu', input_shape=(28, 28, 1)),
    tf.keras.layers.Conv2D(64, 5, padding='same', activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(1024, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(loss='categorical_crossentopy', optimizer=Adam(0.001))
model.summary()
```

### Workflow

1. Wrap model in a function

2. Define hyper-parameters

3. Replace static value with hyper-parameters

4. Run tuner

```python
def model_fn():
    LR = Choice('learning_rate', [0.0001, 0.005, 0.0001], group='optimizer')
    DROPOUT_RATE = Linear('dropout_rate', 0.0, 0.5, 5, group='dense')
    NUM_DIMS = Range('num_dims', 8, 32, 8, group='dense')
    NUM_LAYERS = Range('num_layers', 1, 3, group='dense')
    L2_NUM_FILTERS = Range('l2_num_filters', 8, 64, 8, group='cnn')
    L1_NUM_FILTERS = Range('l1_num_filters', 8, 64, 8, group='cnn')

    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(L1_NUM_FILTERS, 5, padding='same', activation='relu', input_shape=(28, 28, 1)),
        tf.keras.layers.Conv2D(L2_NUM_FILTERS, 5, padding='same', activation='relu'),
        tf.keras.layers.Flatten(),
        for _ in range(NUM_LAYERS):
            tf.keras.layers.Dense(NUM_DIMS, activation='relu'),
            tf.keras.layers.Dropout(DROPOUT_RATE),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    
    model.compile(loss='categorical_crossentopy', optimizer=Adam(LR))
    return model

tuner = Tuner(model_fn, 'val_accuracy', epoch_budget=500, max_epochs=5)
tuner.search(tfg, validation_data=validation_data)
```

# Links

* [EAP Program](https://services.google.com/fb/forms/kerastuner/)