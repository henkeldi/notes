
# GCC under the hood


# Steps GCC Performs

1. Preprocessing
1. Compiler
1. Assembler
1. Linker

*hello.c*

```c++
#include <stdio.h>

int main() {
    printf("Hello");
    return 0;
}
```

Step 1:
```bash
cpp hello.c > hello.i
```

Step 2:

*Generate assembler code*

```bash
gcc -S hello.i
```

Step 3:

```bash
as -o hello.o hello.s
```

Step 4:

```bash
ld -o hello hello.o
```
Will give you error cannot find _start, cannot find printf
Solution:

```bash
ld -e main -o hello hello.o /lib/libc.so -I /lib64/ld-linux-x86-64.so.2
```

![](./images/callgraph.png)

# Source

* [GCC ПОД КАПОТОМ](https://www.youtube.com/watch?v=HBFA6dKW7qE)
* [Linux Program Startup](http://dbp-consulting.com/tutorials/debugging/linuxProgramStartup.html)
