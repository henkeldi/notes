
# Ncurses

## Installation

```bash
sudo apt install libncurses5-dev libncursesw5-dev
```

## Usage

```c++
#include <ncurses.h>

int main() {
	initscr();			/* Start curses mode 		  */
	printw("Hello World !!!");	/* Print Hello World		  */
	refresh();			/* Print it on to the real screen */
	getch();			/* Wait for user input */
	endwin();			/* End curses mode		  */

	return 0;
}
```

*CMakeLists.txt*

```cmake
# [...]
add_executable(main main.cpp)
target_link_libraries(main ncurses)
```

# Source

* [tldp](https://tldp.org/HOWTO/NCURSES-Programming-HOWTO/init.html)
