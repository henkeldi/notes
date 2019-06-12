
# WebAssembly

## Wrap C++ library into JavaScript

```bash
cd node_modules/mozjpeg
autoconf -fiv
emconfigure ./configure --without-simd
emmake make libjpeg.la
```

*mozjpeg_enc.cpp*


```cpp
#include "jpeglib.h"

val encode(
    std::string image_in,
    int image_width,
    int image_height
) {
  uint8_t* image_buffer = (uint8_t*) malloc();
  // ... Use MozJPEG ...
  return val(typed_memory_view(size, image_buffer));
}

EMSCRIPTEN_BINDINGS(mozjpeg_wasm) {
  function("encode", &encode);
}
```

```bash
emcc \
    --bind \
    -I node_modules/mozjpeg \
    -o ./mozjpeg_enc.js
    -x c++ -std=c++11
    mozjpeg_enc.cpp \
    node_modules/mozjpeg/.libs/libjpeg.a
```

## AssemblyScript

* Write WebAssembly in Typescript

```typescript
export function rotate(inputWidth: i32, inputheight: i32, rotate: i32): void {
  for (let y = 0; y < inputHeight; y++) {
    for (let x = 0; x < inputWidth; x++) {
      let inputPixel = load<32>(y * inputWidth + x)
      store<u32>(rotate(x,y), inputPixel);
    }
  }
}
```

* Has no garbage collector yet
```typescript
import "allocator/tlsf"
let ptr = memory.allocate(64)
// do something with pts ...
 
// ... and free it again
memory.free(ptr);
```