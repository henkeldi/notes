
# Vulkan

## Install

```bash
sudo apt install libglfw3-dev
```

##  Compile

```bash
g++ main.cpp -o main -lvulkan -lglfw -std=c++17
```

## Usage

<details><summary>Window</summary>

```c++
#define GLFW_INCLUDE_VULKAN
#include <GLFW/glfw3.h>
// [...]
glfwInit();
glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API);
window = glfwCreateWindow(
    width, height, "<Window Title>", nullptr, nullptr);
// [...]
glfwDestroyWindow(window);
glfwTerminate();
```
</details>

# Source

* [VulkanSamples Utils](https://github.com/LunarG/VulkanSamples/blob/master/API-Samples/utils/util_init.cpp)
