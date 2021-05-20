
# Python Code Snippets

## Check operating system

```python
import platform

def is_windows():
  return platform.system() == 'Windows'

def is_linux():
  return platform.system() == 'Linux'

def is_macos():
  return platform.system() == 'Darwin'

def is_ppc64le():
  return platform.machine() == 'ppc64le'

def is_cygwin():
  return platform.system().startswith('CYGWIN_NT')
```

## Argument Parser

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '--output-path',
    type=str,
    default=os.path.abspath(os.path.dirname(__file__)),
    help='The absolute path to an output folder.')
args = parser.parse_args()
```

## Get location of current file

```python
import pathlib
pathlib.Path(__file__).parent.absolute()
```

## Measure execution time

```python
timeit.timeit(lambda: lstm_cell(input, state), number=10)
```

# Source

* [Tensorflow Config File](https://raw.githubusercontent.com/tensorflow/tensorflow/master/configure.py)
