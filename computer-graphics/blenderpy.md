
# Blenderpy

## Install

Build Python 3.7 from source:

```bash
./configure \
    --prefix=`pwd`/src/Python-3.7.9/install \
    --enable-shared \
    --enable-optimizations \
    --with-system-expat \
    --with-system-ffi \
    --with-ensurepip=yes \
```

sudo apt-get install -y fftw3
sudo apt install libfftw3-dev libopenimageio-dev

```bash
sudo pip3.7 install numpy
pip3.7 install future_fstrings
pip3.7 install wheel
pip3.7 install bpy
```