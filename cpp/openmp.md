
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

Output:

```bash
Thread: 1 i = 3
Thread: 1 i = 4
Thread: 1 i = 5
Thread: 3 i = 8
Thread: 3 i = 9
Thread: 0 i = 0
Thread: 0 i = 1
Thread: 0 i = 2
Thread: 2 i = 6
Thread: 2 i = 7
```