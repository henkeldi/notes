
# Vulkan

## Install

```bash
sudo apt install libglfw3-dev
```

##  Compile

```bash
g++ main.cpp -o main -lvulkan -lglfw -std=c++17
```

## Use

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

<details><summary>Instance</summary>

```c++
#include <vulkan/vulkan.h>
#include <cassert>
#define APP_SHORT_NAME "my_app_name"
// [...]
VkApplicationInfo app_info = {};
app_info.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
app_info.pNext = nullptr;
app_info.pApplicationName = APP_SHORT_NAME;
app_info.applicationVersion = VK_MAKE_VERSION(1, 0, 0);
app_info.pEngineName = APP_SHORT_NAME;
app_info.engineVersion = VK_MAKE_VERSION(1, 0, 0);
app_info.apiVersion = VK_API_VERSION_1_1;

VkInstanceCreateInfo inst_info = {};
inst_info.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
inst_info.pNext = nullptr;
inst_info.flags = 0;
inst_info.pApplicationInfo = &app_info;
inst_info.enabledExtensionCount = 0;
inst_info.ppEnabledExtensionNames = nullptr;
inst_info.enabledLayerCount = 0;
inst_info.ppEnabledLayerNames = nullptr;

VkInstance instance;
VkResult res = vkCreateInstance(&inst_info, nullptr, &instance);
assert(!res);
// [...]
vkDestroyInstance(instance, nullptr);
```
</details>

<details><summary>Enumerate Devices</summary>

```c++
#include <vector>
// [...]
std::vector<VkPhysicalDevice> gpus;
uint32_t gpu_count = -1;
res = vkEnumeratePhysicalDevices(instance, &gpu_count, nullptr);
assert(gpu_count);
gpus.resize(gpu_count);
res = vkEnumeratePhysicalDevices(instance, &gpu_count, gpus.data());
assert(!res && gpu_count >= 1);
```
</details>

## Source

* [Vulkan Tutorial](https://vulkan-tutorial.com/)
* [VulkanSamples Utils](https://github.com/LunarG/VulkanSamples/blob/master/API-Samples/utils/util_init.cpp)
* [LunarG Vulkan Samples](https://github.com/LunarG/VulkanSamples)
