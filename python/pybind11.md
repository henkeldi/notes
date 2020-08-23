# pybind11

## Install

* [Releases](https://github.com/pybind/pybind11/releases)

```bash
wget https://github.com/pybind/pybind11/archive/v2.5.0.tar.gz
```

## Use

**main.py**

```python
import numpy as np

import lib_cpp

input1 = np.ones((5, 5))
lib_cpp.func(input1)
```

**lib.cpp**

```c++
#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>

void func(const Eigen::MatrixXd& input1) {
}

PYBIND11_MODULE(lib_cpp, m) {
    m.def("func", &func);
}
```

**CMakeLists.txt**

```cmake
project(lib)
cmake_minimum_required(VERSION 3.10)

find_package(Eigen3 REQUIRED)

add_subdirectory(pybind11-2.5.0)
pybind11_add_module(lib_cpp lib.cpp)
target_link_libraries(lib_cpp
    PRIVATE
        pybind11::module
        Eigen3::Eigen
)
```
