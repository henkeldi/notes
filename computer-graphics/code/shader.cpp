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
      std::cerr << "Invalid shader suffix: " << suffix << std::endl;
      std::cerr << "Please use one of the following:" << std::endl;
      for (const auto& suffix_to_type : kSuffixToShaderLookup) {
        std::cout << suffix_to_type.first << std::endl;
      }
      std::abort();
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
      std::cerr << "Program linking failed:" << std::endl;
      std::cerr << std::string(begin(infoLog), end(infoLog)) << std::endl;
      std::abort();
  }
}

GLuint Shader::doCompile(const std::string& path, const GLuint type) {
  auto shader = glCreateShader(type);
  auto shader_code = readFile(path);
  const char *shader_code_ptr = shader_code.c_str();
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
      std::cerr << "Shader compilation failed:" << std::endl;
      std::cerr << std::string(begin(infoLog), end(infoLog)) << std::endl;
      std::abort();
  }
  return shader;
}

const std::string Shader::readFile(const std::string& path) {
  std::ifstream ifs{path};
  if (!ifs) {
    std::cerr << "Couldn't open [" << path << "] for reading." << std::endl;
    std::abort();
  }
  std::string line;
  std::ostringstream oss;
  while (std::getline(ifs, line)) {
    oss << line << "\n";
  }
  ifs.close();
  return oss.str();
}

void Shader::Use() {
  glUseProgram(program_);
}
