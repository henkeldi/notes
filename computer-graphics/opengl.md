
# OpenGL 4.5

## Includes

```cpp
#include "GL/glew.h"
#include "GL/gl.h"
#include "GLFW/glfw3.h"
```

## Compile

```bash
g++ main.cpp -o main -lglfw -lGL -lGLEW
```

## Initialization

```cpp
if (!glfwInit()) {
    std::cerr << "Could not start GLFW3" << std::endl;
    std::abort();
}

GLFWmonitor* monitor = fullscreen? glfwGetPrimaryMonitor(): nullptr;
GLFWwindow* window = glfwCreateWindow(window_width, window_height, "Title", monitor, nullptr);
if (!window) {
    std::cerr << "Could not open window with GLFW3" << std::endl;
    std::abort();
}

glfwMakeContextCurrent(window);

if (glewInit() != GLEW_OK) {
    std::cerr << "GlewInit failed" << std::endl;
    std::abort();
}
```

## Create program

```cpp
auto program = glCreateProgram();
glAttachShader(program, vertex_shader);
glAttachShader(program, fragment_shader);
glLinkProgram(program);
GLint isLinked = 0;
glGetProgramiv(program, GL_LINK_STATUS, &isLinked);
if (isLinked == GL_FALSE) {
    GLint maxLength = 0;
    glGetProgramiv(program, GL_INFO_LOG_LENGTH, &maxLength);
    std::vector<GLchar> infoLog(maxLength);
    glGetProgramInfoLog(program, maxLength, &maxLength, &infoLog[0]);
    glDeleteProgram(program);
    std::cerr << "Program linking failed:" << std::endl;
    std::cerr << std::string(begin(infoLog), end(infoLog)) << std::endl;
    std::abort();
}
glDeleteShader(vertex_shader);
glDeleteShader(fragment_shader);
glUseProgram(program);
```

## Create shader

```cpp
auto shader = glCreateShader(type);
glShaderSource(shader, 1, &shader_code, nullptr);
glCompileShader(shader);
GLint isCompiled = 0;
glGetShaderiv(shader, GL_COMPILE_STATUS, &isCompiled);
if (isCompiled == GL_FALSE) {
    GLint maxLength = 0;
    glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &maxLength);
    std::vector<GLchar> infoLog(maxLength);
    glGetShaderInfoLog(shader, maxLength, &maxLength, &infoLog[0]);
    glDeleteShader(shader);
    std::cerr << "Shader compilation failed:" << std::endl;
    std::cerr << std::string(begin(infoLog), end(infoLog)) << std::endl;
    std::abort();
}
```

## Vertex shader

```c
#version 450

out vec2 Tex_Coords;

layout (location = 0) uniform vec2 screen_size;
layout (location = 1) uniform vec2 image_size;
layout (location = 2) uniform bool fill_screen = false;
layout (location = 3) uniform float scale = 1;

void main(void) {
    if ((screen_size.x/screen_size.y>image_size.x/image_size.y)^^fill_screen) {
        const float image_width_half = (image_size.x*screen_size.y)/(screen_size.x*image_size.y);
        const vec2 vertices[4] = vec2[4](
            vec2(-image_width_half, -1),
            vec2(-image_width_half, 1),
            vec2(image_width_half, -1),
            vec2(image_width_half, 1));
        gl_Position = vec4(scale*vertices[gl_VertexID].xy, 0, 1.0);
    } else {
        const float image_height_half = (image_size.y*screen_size.x)/(screen_size.y*image_size.x);
        const vec2 vertices[4] = vec2[4](
            vec2(-1, -image_height_half),
            vec2(-1, image_height_half),
            vec2(1, -image_height_half),
            vec2(1, image_height_half));
        gl_Position = vec4(scale*vertices[gl_VertexID].xy, 0, 1.0);
    }
    const vec2 tex_coords[4] = vec2[4](
        vec2(0, 1),
        vec2(0, 0),
        vec2(1, 1),
        vec2(1, 0));
    Tex_Coords = tex_coords[gl_VertexID];
}
```

## Fragment shader

```c
#version 450

#extension GL_NV_bindless_texture : require

layout (binding=0) readonly buffer TEXTURES {
    sampler2D textures[];
};

layout (location=0) out vec4 color;

layout (location=4) uniform int tex_id = 0;

in vec2 Tex_Coords;

void main(void) {
    vec3 rgb = texture(textures[tex_id], Tex_Coords).rgb;
    color = vec4(rgb, 1.0);
}
```

# Create Texture

```cpp
GLuint tex_id;
GLuint64 handle;

glCreateTextures(GL_TEXTURE_2D, 1, &tex_id);

glTextureStorage2D(tex_id, 1, GL_RGB8, img.cols, img.rows);

glTextureParameteri(tex_id, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
glTextureParameteri(tex_id, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
glTextureParameteri(tex_id, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
glTextureParameteri(tex_id, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);

// #include "opencv2/opencv.hpp"
auto img = cv::imread("path/to/image.png");

glTextureSubImage2D(tex_id, /* level */ 0, /* offsetX */ 0, /* offsetY */ 0,
    img.cols, img.rows, GL_BGR, GL_UNSIGNED_BYTE, img.data);

auto handle = glGetTextureHandleNV(tex_id);
glMakeTextureHandleResidentNV(handle);

GLuint handles_buffer;
glCreateBuffers(1, &handles_buffer);
glNamedBufferStorage(handles_buffer, 1*sizeof(GLuint64), &handle, 0);
glBindBufferRange(
    GL_SHADER_STORAGE_BUFFER,
    0,
    handles_buffer,
    0,
    1*sizeof(GLuint64));
```

## Set Uniform

```cpp
glUniform2f(UNIFORM_LOCATION, float1, float2);
```

## Render loop

```cpp
while (!glfwWindowShouldClose(window)) {
    glViewport(0, 0, window_width, window_height);
    glClear(GL_COLOR_BUFFER_BIT);

    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);

    glfwSwapBuffers(window);
    glfwPollEvents();
}
```

## Cleanup

```cpp
glfwTerminate();
```

# Source

* [Example Code Khronos](https://www.khronos.org/opengl/wiki/Example_Code)
