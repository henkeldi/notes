
# GAN

Neural Network which generates realistic data.

## Motivation

* *Stackgan* generates images from text
* *[Pix2Pix](https://affinelayer.com/pixsrv/)* generates realistic images from sketches
* Turn day scenes into night scenes
* *[CycleGAN](https://github.com/junyanz/CycleGAN)* 
* [Simulated eye](https://arxiv.org/pdf/1612.07828.pdf) images to Real images

## How it works

* Consists of Generator and Discriminator
* Generator takes in noise and generates image
* Discriminator is a classifier which takes a real and a generated image and has to decide whether it's real or fake.

## Tips and Tricks

* Use Leaky ReLu, important for gradient flow
* At least one hidden layer in G and D
* Generator output has tanh activation
* Discriminator has sigmoid activation
* Use Adam as optimizer
* Use logits for cross entropy
* Multiply labels times 0.9, helps discriminator to generalize better
* Generator gets random noise z as input
* Use Batchnorm everywhere except output layer of generator and input layer of descriminator
* Paper: [Improved Techniques for Training GANs](https://arxiv.org/pdf/1606.03498.pdf)
