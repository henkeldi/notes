
# CMake

## Install

CMake:

```bash
sudo apt-get -y install cmake
```

CMake GUI:

```bash
sudo apt-get -y install cmake-qt-gui
```

## Example

*CMakeLists.txt:*

```cmake
cmake_minimum_required(VERSION 2.8)
project(foo)

# C-Only project
project(foo C)

# Specify project version
project(Foo VERSION 1.2.7)

# Access project version

message("  Version: ${PROJECT_VERSION}")
message("  Version (alt): ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}.${PROJECT_VERSION_PATCH}")

#output: Version 1.2.7
#        Version (alt): 1.2.7

set(condition_b "NO")

if(condition_b)
    message("Hello")
else()
    message("Bye")
endif()

# List

set(elements a b c)

foreach(element elements)
    message("element=${element}")
endforeach()

include_directories(
    include)

link_directories(
    lib)

add_executable(my_program src/my_program.cpp)
target_link_libraries(my_program
    some_lib)

add_subdirectory(foo)
```

## Build

```bash
cmake -H -B build
```

Build

```bash
cmake --build build -DCMAKE_BUILD_TYPE={Debug, Release}
```

```bash
cmake -DCMAKE_BUILD_TYPE=Release ..
```

## Project Layout

```
├── CMakeLists.txt
├── lib/
│   ├── CMakeLists.txt
│   └── fruits/
│       ├── CMakeLists.txt
│       ├── fruits.hpp
│       ├── rosaceae/
│       │   ├── CMakeLists.txt
│       │   ├── rosaceae.hpp
│       │   ├── Pear.cpp
│       │   ├── Pear.hpp
│       │   ├── Plum.cpp
│       │   ├── Plum.hpp
│       │   └── unittest/
│       │       └── Pear.cpp
│       └── tropical/
│           ├── CMakeLists.txt
│           ├── tropical.hpp
│           ├── Avocado.cpp
│           ├── Avocado.hpp
│           ├── Pineapple.cpp
│           ├── Pineapple.hpp
│           └── unittest/
│               ├── Avocado.cpp
│               └── Pineapple.cpp
├── app/
│   ├── CMakeLists.txt
│   └── fruits/
│       ├── CMakeLists.txt
│       ├── breakfast/
│       │   ├── CMakeLists.txt
│       │   ├── flatware/
│       │   │   ├── Teaspoon.cpp
│       │   │   └── Teaspoon.hpp
│       │   └── main.cpp
│       └── dinner/
│           ├── CMakeLists.txt
│           └── main.cpp
├── example/
│   ├── CMakeLists.txt
│   └── fruits/
│       ├── CMakeLists.txt
│       ├── quick_meal/
│       │   ├── CMakeLists.txt
│       │   └── main.cpp
│       └── vegan_party/
│           ├── CMakeLists.txt
│           └── main.cpp
└── test/
    ├── CMakeLists.txt
    └── fruits/
        ├── CMakeLists.txt
        ├── check_tropical/
        │   ├── CMakeLists.txt
        │   └── data/
        │       └── avocado.ini
        └── skin_off/
            └── CMakeLists.txt
```
