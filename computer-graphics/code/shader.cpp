#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "GL/glew.h"
#include "GL/gl.h"

#include "shader.h"

Shader::Shader(const std::vector<std::string>& shader_paths) :
    shader_paths_(shader_paths) {
}

void Shader::Compile() {
  program_ = glCreateProgram();
  for (const auto& path : shader_paths_) {
    auto dot_index = path.rfind(".");
    auto suffix = path.substr(dot_index+1, path.length());
    if (kSuffixToShaderLookup.find(suffix) == kSuffixToShaderLookup.end()) {
      throw std::runtime_error("Invalid shader suffix: " + suffix);
    }
    auto type = kSuffixToShaderLookup.at(suffix);
    auto shader = doCompile(path, type);
    glAttachShader(program_, shader);
  }
  glLinkProgram(program_);
  GLint isLinked = 0;
  glGetProgramiv(program_, GL_LINK_STATUS, &isLinked);
  if (isLinked == GL_FALSE) {
      GLint maxLength = 0;
      glGetProgramiv(program_, GL_INFO_LOG_LENGTH, &maxLength);
      std::vector<GLchar> infoLog(maxLength);
      glGetProgramInfoLog(program_, maxLength, &maxLength, &infoLog[0]);
      glDeleteProgram(program_);
      throw std::runtime_error("Program linking failed: \n\n" +
        std::string(begin(infoLog), end(infoLog)));
  }
}

GLuint Shader::doCompile(const std::string& path, const GLuint type) {
  auto shader = glCreateShader(type);
  auto shader_code = readFile(path);
  const char *shader_code_ptr = shader_code.data();
  glShaderSource(shader, 1, &shader_code_ptr, nullptr);
  glCompileShader(shader);
  GLint isCompiled = 0;
  glGetShaderiv(shader, GL_COMPILE_STATUS, &isCompiled);
  if (isCompiled == GL_FALSE) {
      GLint maxLength = 0;
      glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &maxLength);
      std::vector<GLchar> infoLog(maxLength);
      glGetShaderInfoLog(shader, maxLength, &maxLength, &infoLog[0]);
      glDeleteShader(shader);
      throw std::runtime_error("("+ path +"): Shader compilation failed: " +
        std::string(begin(infoLog), end(infoLog)));
  }
  return shader;
}

const std::vector<char> Shader::readFile(const std::string& path) {
  std::ifstream ifs(path, std::ios::ate | std::ios::binary);
  if (!ifs.is_open()) {
    throw std::runtime_error("Failed to open " + path + " for reading.");
  }
  size_t fileSize = (size_t) ifs.tellg();
  std::vector<char> buffer(fileSize);
  ifs.seekg(0);
  ifs.read(buffer.data(), fileSize);
  ifs.close();
  return buffer;
}

void Shader::Use() {
  glUseProgram(program_);
}
