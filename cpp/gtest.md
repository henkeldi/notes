
# GoogleTest

## Usage

**src/adder.cpp**

```c++
int add(int a, int b) {
    return a + b;
}
```

**src/adder.h**

```c++
#ifndef ADDER_H
#define ADDER_H

int add(int a, int b);

#endif
```

**test/test_adder.cpp**

```c++
#include "gtest/gtest.h"

#include "../src/adder.h"

TEST(AdderTest, TestAddFunction) {
    EXPECT_EQ(add(1, 1), 2);
}
```

**CMakeLists.txt.in**

```
cmake_minimum_required(VERSION 2.8.12)

project(googletest-download NONE)

include(ExternalProject)
ExternalProject_Add(googletest
  GIT_REPOSITORY    https://github.com/google/googletest.git
  GIT_TAG           master
  SOURCE_DIR        "${CMAKE_CURRENT_BINARY_DIR}/googletest-src"
  BINARY_DIR        "${CMAKE_CURRENT_BINARY_DIR}/googletest-build"
  CONFIGURE_COMMAND ""
  BUILD_COMMAND     ""
  INSTALL_COMMAND   ""
  TEST_COMMAND      ""
)
```

**CMakeLists.txt**

```cmake
cmake_minimum_required(VERSION 3.11.3)

set(CMAKE_CXX_STANDARD 17)

project(my_project)

# Download and unpack googletest at configure time
configure_file(CMakeLists.txt.in googletest-download/CMakeLists.txt)
execute_process(COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" .
  RESULT_VARIABLE result
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/googletest-download )
if(result)
  message(FATAL_ERROR "CMake step for googletest failed: ${result}")
endif()
execute_process(COMMAND ${CMAKE_COMMAND} --build .
  RESULT_VARIABLE result
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/googletest-download )
if(result)
  message(FATAL_ERROR "Build step for googletest failed: ${result}")
endif()

# Add googletest directly to our build. This defines
# the gtest and gtest_main targets.
add_subdirectory(${CMAKE_CURRENT_BINARY_DIR}/googletest-src
                 ${CMAKE_CURRENT_BINARY_DIR}/googletest-build
                 EXCLUDE_FROM_ALL)

add_executable(test test/test_adder.cpp src/adder.cpp)
target_link_libraries(test gtest_main)
add_test(NAME main_test COMMAND test)
```

**Build**

```bash
mkdir build
cd build
cmake ..
make
```
**Run Tests**

```bash
$ ./test
Running main() from /tmp/tmp/build/googletest-src/googletest/src/gtest_main.cc
[==========] Running 1 test from 1 test suite.
[----------] Global test environment set-up.
[----------] 1 test from AdderTest
[ RUN      ] AdderTest.TestAddFunction
[       OK ] AdderTest.TestAddFunction (0 ms)
[----------] 1 test from AdderTest (0 ms total)

[----------] Global test environment tear-down
[==========] 1 test from 1 test suite ran. (0 ms total)
[  PASSED  ] 1 test.
```

# Source

* [GoogleTest Github Page](https://github.com/google/googletest)
