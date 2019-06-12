
# Tensorflow Probability

### Motivation

```python
model = tf.keras.Sequential([...])

model.compile(optimizer='adam',
              loss=lambda y, dist: -dist.log_prob(y)')

rv_y_given_x = model(x)
rv_y_given_x.prob(y)
rv_y_given_x.mean()
rv_y_given_x.variance()
```

### Installation

```bash
pip install tensorflow-probability
```

or

```bash
pip install tfp-nightly
```

### Example: Regression

#### Learn known unknowns

```python
model = tf.keras.Sequential([
    tf.keras.layers.Dense(hidden_units, ...),
    tf.keras.layers.Dense(1+1), # mean and variance
    tfp.layers.DistributionLambda(lambda t:
        tfd.Normal(loca=t[..., 0], scale=tf.softplus(t[..., 1])))
})
```

#### Learn unknown unknowns

```python
model = tf.keras.Sequential([
    tf.keras.layers.DenseVariational(hidden_units, ...),
    tf.keras.layers.DenseVariational(1),
    tfp.layers.DistributionLambda(lambda t:
        tfd.Normal(loca=t[..., 0], scale=1))
})
```

#### Learn known and unknown unknowns

```python
model = tf.keras.Sequential([
    tf.keras.layers.DenseVariational(hidden_units, ...),
    tf.keras.layers.DenseVariational(1+1),
    tfp.layers.DistributionLambda(lambda t:
        tfd.Normal(loca=t[..., 0], scale=tf.softplus(t[..., 1])))
})
```

#### Uncertainty in the loss function

```python
model = tf.keras.Sequential([
    tf.keras.layers.Dense(hidden_units, ...),
    tf.keras.layers.Dense(1), # mean and variance
    tfp.layers.VariationalGaussianProcess(
        num_inducing_points, kernel_provider)
})
```

### Useful links

* [Baysian Methods for Hackers using Tensorflow Probability](https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/blob/master/Chapter1_Introduction/Ch1_Introduction_TFP.ipynb)
* [Demo Code](https://github.com/tensorflow/probability/blob/master/tensorflow_probability/examples/jupyter_notebooks/Probabilistic_Layers_Regression.ipynb)
* [Tensorflow Probability Tutorial](https://www.tensorflow.org/probability)
* [Tensorflow Probability @ TF Summit](https://www.youtube.com/watch?v=BrwKURU-wpk)
* [Book: Baysian Methods for Hackers](https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers)