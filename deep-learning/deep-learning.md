# Deep Learning

All steps one need to go through when using a neural networks.

## Data Preprocessing

### Step 1: Load data
```python
X, y = load_CIFAR10(cifar10_dir)
```

### Step 2: Split data
```python
num_training = 40000
num_test = 10000

mask = range(num_training)
X_train = X[mask]
y_train = y[mask]

mask = range(num_test, num_training + num_test)
X_test = X[mask]
y_test = y[mask]
```

Data should shape should look like this:
```python
print 'Training data shape: ', X_train.shape
print 'Training labels shape: ', y_train.shape
print 'Test data shape: ', X_test.shape
print 'Test labels shape: ', y_test.shape
```

```bash
Training data shape:  (40000, 32, 32, 3)
Training labels shape:  (40000,)
Test data shape:  (10000, 32, 32, 3)
Test labels shape:  (10000,)
```

### Step 3: Reshape X into 2D matrix

```python
X_train = np.reshape(X_train, (X_train.shape[0], -1))
X_test = np.reshape(X_test, (X_test.shape[0], -1))
print X_train.shape, X_test.shape
```

```bash
(40000, 3072) (10000, 3072)
```

The data layout for one training example is then as follows:

### Step 4: Subtract mean

```python
mean_image = np.mean(X_train, axis=0) # axis=0 means column-wise mean
X_train -= mean_image
X_test -= mean_image
```

also possible:

```python
X -= np.mean(X)
```

### Step 5: Normalization

* Only necessary if different input features have different scales
* Not necessary for image data

```python
X /= np.std(X, axis = 0)
```

### Step 6: Whitening

```python
# whiten the data:
# divide by the eigenvalues (which are square roots of the singular values)
Xwhite = Xrot / np.sqrt(S + 1e-5)
```

### Step 7: Append one to feature vector

```python
X_train = np.hstack([X_train, np.ones((X_train.shape[0], 1))])
X_test = np.hstack([X_test, np.ones((X_test.shape[0], 1))])
```

## Network

### Weight initialization

* Small random numbers
```python
W = 0.01* np.random.randn(D,H)
```

* Calibrating the variances with `1/sqrt(n)`

```python
w = np.random.randn(n) / sqrt(n) # n is the number of inputs
```
* ensures that all neurons in the network initially have approximately the same output distribution
* empirically improves the rate of convergence
* For ReLU neurons
* Recommended by [ext. link](https://arxiv.org/abs/1502.01852)

```python
w = np.random.randn(n) * sqrt(2.0/n) # n is the number of inputs
```

### Bias initialization

* Set all to 0
* Some people like to use small constant, but it doesn't provide a consistent improvement

### Batch normalization

* Forces the activations throughout the network to take on a unit gaussian distribution
* Put BatchNorm layer immediately after fully connected layers or convolutional layers and before non-linearities
* Network becomes significantly more robust to bad initialization

### Forward pass

```python
# forward-pass of a 3-layer neural network:
ReLU = lambda x: x * (x > 0)
X = np.random.randn(3, 1) 
h1 = ReLU(np.dot(X, W1) + b1)
h2 = ReLU(np.dot(h1, W2) + b2)
out = np.dot(h2, W3) + b3
```