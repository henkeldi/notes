
# Makefile

```make
.PHONY: all
all: format test build

.PHONY: format
format:
	clang-format src/* include/* -i

.PHONY: build
build:
	mkdir -p build
	cd build && \
	cmake .. && \
	make

.PHONY: debug
debug:
	mkdir -p build
	cd build && \
	cmake -DCMAKE_BUILD_TYPE=debug .. && \
	make

.PHONY: clean
clean:
	rm -rf build
```

# Source

* [Udacity C++ Nanodegree System Monitor Github](https://github.com/udacity/CppND-System-Monitor/blob/master/Makefile)
