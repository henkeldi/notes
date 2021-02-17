
# C

## Allocate Memory

```c
#include "stdlib.h"

// Memory allocation
pointer = (cast-type*) malloc(<size>);

int *pointer = (int*) malloc(sizeof(int));

// Cleared Memory allocation, initialized with '0'
pointer = (cast-type*) calloc(num_elems, size_elem);

if (pointer) {
    // memory was sucessfully allocated
}

free(pointer);
```
