
# Resource Acquisition Is Initialization (RAII)

Resource usage is usually as follows:

* Optain
* Use
* Release

Rule: Who owns the resource also dealocates it

A RAII class:

1. Allocates resources in the constructor
1. Deallocates resources in the ~destructor
1. All instances of a RAII class are allocated on the stack

Without RAII

```c++
double den[] = {1.0, 2.0, 3.0, 4.0, 5.0};

for (size_t i = 0; i < 5; i++) {
  double *en = new double(i);

  std::cout << *en << "/" << den[i] << " = " << *en / den[i] << std::endl;

  // Easy to forget:
  delete en;
}
```

With RAII

```c++
  double den[] = {1.0, 2.0, 3.0, 4.0, 5.0};
  for (size_t i = 0; i < 5; i++) {
    // Good: Allocated on the STACK
    MyInt en(new int(i));

    // Bad: Allocated on the HEAP
    // MyInt *en = new MyInt(new int(i));

    std::cout << *en << "/" << den[i] << " = " << *en / den[i] << std::endl;
  }
```

```c++
class MyInt {
  public:
    MyInt(int *p = nullptr) { p_ = p; }
    ~MyInt() {
      delete p_;
    }
  private:
    int *p_;
}
```

# Source

* [Udacity c++ nanodegree](https://www.udacity.com/course/c-plus-plus-nanodegree--nd213)
