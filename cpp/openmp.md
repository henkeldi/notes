
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
        unsigned int cpu_thread_id = omp_get_thread_num();
        unsigned int num_cpu_threads = omp_get_num_threads();
        #pragma omp for
        for (int i = 0; i < 10; i++) {
            std::cout << "Thread: " << cpu_thread_id << " / " << num_cpu_threads << "; i = " << i << std::endl;
        }
    }
    return 0;
}
```

Output:

```bash
Thread: 1 / 4; i = 3
Thread: 1 / 4; i = 4
Thread: 1 / 4; i = 5
Thread: 3 / 4; i = 8
Thread: 3 / 4; i = 9
Thread: 0 / 4; i = 0
Thread: 0 / 4; i = 1
Thread: 0 / 4; i = 2
Thread: 2 / 4; i = 6
Thread: 2 / 4; i = 7
```