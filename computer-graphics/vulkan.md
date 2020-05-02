
# Vulkan

## Install

```bash
sudo apt install libglfw3-dev
```

##  Compile

```bash
g++ main.cpp -o main -lvulkan
```

## Use

<details><summary>Window (GLFW)</summary>

Install

```bash
sudo apt install libglfw3-dev
```

Linker flag: **-lglfw**

```c++
#define GLFW_INCLUDE_VULKAN
#include <GLFW/glfw3.h>
// [...]
glfwInit();
glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API);
auto window = glfwCreateWindow(
    500, 500, "<Window Title>", nullptr, nullptr);
uint32_t glfwExtensionCount;
auto glfwExtensions = glfwGetRequiredInstanceExtensions(
    &glfwExtensionCount);
std::vector<const char*> instance_extension_names(
    glfwExtensions, glfwExtensions + glfwExtensionCount);
// [...]
glfwDestroyWindow(window);
glfwTerminate();
```
</details>

<details><summary>Window (XCB)</summary>

Linker flag: **-lxcb**

```c++
#include <xcb/xcb.h>
#include <vulkan/vulkan_xcb.h>
// [...]
const xcb_setup_t *setup;
xcb_screen_iterator_t iter;
int scr;

auto connection = xcb_connect(NULL, &scr);
assert(connection != nullptr);
assert(xcb_connection_has_error(connection) == 0);

setup = xcb_get_setup(connection);
iter = xcb_setup_roots_iterator(setup);
while (scr-- > 0) xcb_screen_next(&iter);

auto screen = iter.data;

auto window = xcb_generate_id(connection);

uint32_t value_mask, value_list[32];
value_mask = XCB_CW_BACK_PIXEL | XCB_CW_EVENT_MASK;
value_list[0] = screen->black_pixel;
value_list[1] = XCB_EVENT_MASK_KEY_RELEASE | XCB_EVENT_MASK_EXPOSURE;

int16_t width = 500, height = 500;
xcb_create_window(connection, XCB_COPY_FROM_PARENT, window, screen->root, 0, 0, width, height, 0,
                    XCB_WINDOW_CLASS_INPUT_OUTPUT, screen->root_visual, value_mask, value_list);

/* Magic code that will send notification when window is destroyed */
xcb_intern_atom_cookie_t cookie = xcb_intern_atom(connection, 1, 12, "WM_PROTOCOLS");
xcb_intern_atom_reply_t *reply = xcb_intern_atom_reply(connection, cookie, 0);

xcb_intern_atom_cookie_t cookie2 = xcb_intern_atom(connection, 0, 16, "WM_DELETE_WINDOW");
auto atom_wm_delete_window = xcb_intern_atom_reply(connection, cookie2, 0);

xcb_change_property(connection, XCB_PROP_MODE_REPLACE, window, (*reply).atom, 4, 32, 1,
                    &(*atom_wm_delete_window).atom);
free(reply);

xcb_map_window(connection, window);

// Force the x/y coordinates to 100,100 results are identical in consecutive
// runs
const uint32_t coords[] = {100, 100};
xcb_configure_window(connection, window, XCB_CONFIG_WINDOW_X | XCB_CONFIG_WINDOW_Y, coords);
xcb_flush(connection);

xcb_generic_event_t *e;
while ((e = xcb_wait_for_event(connection))) {
    if ((e->response_type & ~0x80) == XCB_EXPOSE) break;
}

std::vector<const char*> instance_extension_names = {
    VK_KHR_XCB_SURFACE_EXTENSION_NAME
    VK_KHR_SWAPCHAIN_EXTENSION_NAME
};
// [...]
xcb_destroy_window(connection, window);
xcb_disconnect(connection);
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
inst_info.enabledExtensionCount = static_cast<uint32_t>(extensions.size());
inst_info.ppEnabledExtensionNames = extensions.data();
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
vkDeviceWaitIdle(device);
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

<details><summary>Surface (GLFW)</summary>

```c++
VkSurfaceKHR surface;
res = glfwCreateWindowSurface(instance, window, nullptr, &surface);
assert(res == VK_SUCCESS);
```
</details>

<details><summary>Surface (XCB)</summary>

```c++
VkXcbSurfaceCreateInfoKHR createInfo = {};
createInfo.sType = VK_STRUCTURE_TYPE_XCB_SURFACE_CREATE_INFO_KHR;
createInfo.pNext = nullptr;
createInfo.connection = connection;
createInfo.window = window;

VkSurfaceKHR surface;
res = vkCreateXcbSurfaceKHR(instance, &createInfo, nullptr, &surface);
assert(res == VK_SUCCESS);
// ...
vkDestroySurfaceKHR(instance, surface, nullptr);
```
</details>

<details><summary>Surface (Android)</summary>

```c++
assert(Android_application != nullptr);
auto fpCreateAndroidSurfaceKHR =
    reinterpret_cast<PFN_vkCreateAndroidSurfaceKHR>(vkGetInstanceProcAddr(instance, "vkCreateAndroidSurfaceKHR"));
assert(fpCreateAndroidSurfaceKHR != nullptr);

VkAndroidSurfaceCreateInfoKHR createInfo;
createInfo.sType = VK_STRUCTURE_TYPE_ANDROID_SURFACE_CREATE_INFO_KHR;
createInfo.pNext = nullptr;
createInfo.flags = 0;
createInfo.window = Android_application->window;

VkSurfaceKHR surface;
res = fpCreateAndroidSurfaceKHR(instance, &createInfo, nullptr, &surface);
assert(res == VK_SUCCESS);
```
</details>

## Source

* [Vulkan Tutorial](https://vulkan-tutorial.com/)
* [VulkanSamples Utils](https://github.com/LunarG/VulkanSamples/blob/master/API-Samples/utils/util_init.cpp)
* [LunarG Vulkan Samples](https://github.com/LunarG/VulkanSamples)
