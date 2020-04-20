
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
assert(res == VK_SUCCESS);
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

<details><summary>Device</summary>

```c++
std::vector<VkQueueFamilyProperties> queue_props;
uint32_t queue_family_count = -1;
vkGetPhysicalDeviceQueueFamilyProperties(gpus[0], &queue_family_count, nullptr);
assert(queue_family_count >= 1);
queue_props.resize(queue_family_count);
vkGetPhysicalDeviceQueueFamilyProperties(gpus[0], &queue_family_count, queue_props.data());

VkDeviceQueueCreateInfo queue_info = {};
bool found = false;
for (size_t i = 0; i < queue_family_count; i++) {
    if (queue_props[i].queueFlags & VK_QUEUE_GRAPHICS_BIT) {
        queue_info.queueFamilyIndex = i;
        found = true;
        break;
    }
}
assert(found);
assert(queue_family_count >= 1);

float queue_priorities[1] = {0.0};
queue_info.sType = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO;
queue_info.pNext = nullptr;
queue_info.queueCount = 1;
queue_info.pQueuePriorities = queue_priorities;

VkDeviceCreateInfo device_info = {};
device_info.sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO;
device_info.pNext = nullptr;
device_info.queueCreateInfoCount = 1;
device_info.pQueueCreateInfos = &queue_info;
device_info.enabledExtensionCount = 0;
device_info.ppEnabledExtensionNames = nullptr;
device_info.enabledLayerCount = 0;
device_info.ppEnabledLayerNames = nullptr;
device_info.pEnabledFeatures = nullptr;

VkDevice device;
res = vkCreateDevice(gpus[0], &device_info, nullptr, &device);
assert(res == VK_SUCCESS);
// [...]
vkDestroyDevice(device, nullptr);
```
</details>

<details><summary>Command buffer</summary>

```c++
VkCommandPoolCreateInfo cmd_pool_info = {};
cmd_pool_info.sType = VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO;
cmd_pool_info.pNext = nullptr;
cmd_pool_info.queueFamilyIndex = queue_info.queueFamilyIndex;
cmd_pool_info.flags = 0;

VkCommandPool cmd_pool;
res = vkCreateCommandPool(device, &cmd_pool_info, nullptr, &cmd_pool);
assert(res == VK_SUCCESS);
VkCommandBufferAllocateInfo cmd_buf_info = {};
cmd_buf_info.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO;
cmd_buf_info.pNext = nullptr;
cmd_buf_info.commandPool = cmd_pool;
cmd_buf_info.level = VK_COMMAND_BUFFER_LEVEL_PRIMARY;
cmd_buf_info.commandBufferCount = 1;

VkCommandBuffer cmd_bufs[1];
res = vkAllocateCommandBuffers(device, &cmd_buf_info, cmd_bufs);
assert(res == VK_SUCCESS);
// [...]
vkFreeCommandBuffers(device, cmd_pool, 1, cmd_bufs);
vkDestroyCommandPool(device, cmd_pool, nullptr);
```
</details>

## Source

* [Vulkan Tutorial](https://vulkan-tutorial.com/)
* [VulkanSamples Utils](https://github.com/LunarG/VulkanSamples/blob/master/API-Samples/utils/util_init.cpp)
* [LunarG Vulkan Samples](https://github.com/LunarG/VulkanSamples)
