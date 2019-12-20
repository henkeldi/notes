
# OpenMP

## Install

```bash
sudo apt-get install libomp-dev
```

## Compile

```bash
g++ main.cpp -fopenmp -o main
```

## Example

**main.cpp**

```c++
#include <iostream>

#include <omp.h>

int main() {
    #pragma omp parallel
    {
        #pragma omp for
        for (int i = 0; i < 10; i++) {
            std::cout << "Thread: " << omp_get_thread_num() << " i = " << i << std::endl;
        }
    }
    return 0;
}
```