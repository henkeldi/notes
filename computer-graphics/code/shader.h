#ifndef SHADER_H_
#define SHADER_H_

#include <string>
#include <unordered_map>
#include <vector>

#include "GL/gl.h"

class Shader {
 public:
  explicit Shader(const std::vector<std::string>& shader_paths);
  void Compile();
  void Use();
 private:
  GLuint program_;
  const std::vector<std::string> shader_paths_;
  const std::unordered_map<std::string, GLuint> kSuffixToShaderLookup = {
    {"vs", GL_VERTEX_SHADER},
    {"tcs", GL_TESS_CONTROL_SHADER},
    {"tes", GL_TESS_EVALUATION_SHADER},
    {"gs", GL_GEOMETRY_SHADER},
    {"frag", GL_FRAGMENT_SHADER},
    {"cs", GL_COMPUTE_SHADER},
  };
  GLuint doCompile(const std::string& path, const GLuint type);
  const std::vector<char> readFile(const std::string& path);
};

#endif  // SHADER_H_
