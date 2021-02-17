
# Move semantics

When ever you overwrite one of the following: the copy constructor the assignment operator or the destructor you have to overwrite also the other two.

```c++
MyClass obj1(10);  // regular constructor
MyClass obj2(obj1); // copy constructor
obj2 = obj1 // assign operator
```

```c++
class MyClass {
public:
  MyClass(size_t size) {
    size_ = size;
    data_ = new int[size_];
  }
  // Copy constructor
  // Performs a deep copy
  MyClass(const MyClass &source) {
    size_ = source.size_;
    data_ = new int[size_];
    data_* = *source.data_;
  }
  // Move constructor
  // rvalue reference to source
  // Reuses the momory
  // Invalidates the source object
  MyClass (MyClass &&source) {
    data_ = source.data_;
    size_ = source.size_;
    source.data_ = nullptr;
    source.size_ = 0;
    return *this;
  }
  // Destructor
  ~MyClass() {
    delete[] data_;
  }
  // Assignment operator
  MyClass &operator=(const MyClass &source) {
    if (this == &source) {
      return *this;
    }
    delete[] data_;
    data_ = new int[source.size_];
    *data_ = *source.data_;
    size_ = source.size_;
    return *this;
  }
  // Move assignment operator
  MyClass &operator=(MyClass &&source) {
    if (this == &source) {
      return *this;
    }
    delete[] data_;
    data_ = source.data_;
    size_ = source.size_;

    source.data_ = nullptr;
    source.size_ = 0;

    return *this;
  }
private:
  int size_;
  int* data_;
};
```
```c++
int main() {
    MyClass obj1(100), obj2(200); // constructor
    MyClass obj3(obj1); // copy constructor
    MyClass obj4 = obj1; // copy constructor
    obj4 = obj2; // copy assignment operator

    obj1 = MyClass(200); // move assignment operator
    MyClass obj2 = MyMovableClass(300); // move constructor
    return 0;
}
```
```c++
void useObject(MyMovableClass obj) {
    std::cout << "using object " << &obj << std::endl;
}

int main() {
  MyMovableClass obj1(100);
  // std::mode
  // accepts an lvalue argument
  // and returns it as an rvalue 
  // without triggering copy construction.
  useObject(std::move(obj1));

  // obj1 object invalid here
}

```

## Transfering ownership

```c++
class MyClass {
public:
  MyClass(int val) : _member{val} {}
  void printVal() { std::cout << ", managed object " << this << " with val = " << _member << std::endl; }
private:
    int _member;  
};

void f(std::unique_ptr<MyClass> ptr) {
  std::cout << "unique_ptr " << &ptr;
  ptr->printVal();
}

int main() {
  std::unique_ptr<MyClass> uniquePtr = std::make_unique<MyClass>(23);
  std::cout << "unique_ptr " << &uniquePtr;
  uniquePtr->printVal();

  f(std::move(uniquePtr));

  if (uniquePtr)
    uniquePtr->printVal();
}
```

```c++
void f(std::shared_ptr<MyClass> ptr) {
    std::cout << "shared_ptr (ref_cnt= " << ptr.use_count() << ") " << &ptr;
    ptr->printVal();
}

int main() {
    std::shared_ptr<MyClass> sharedPtr = std::make_shared<MyClass>(23);
    std::cout << "shared_ptr (ref_cnt= " << sharedPtr.use_count() << ") " << &sharedPtr;
    sharedPtr->printVal();

    f(sharedPtr);

    std::cout << "shared_ptr (ref_cnt= " << sharedPtr.use_count() << ") " << &sharedPtr;
    sharedPtr->printVal();
}
```

# Source

* [Udacity c++ nanodegree](https://www.udacity.com/course/c-plus-plus-nanodegree--nd213)
* [Copy elision](https://de.cppreference.com/w/cpp/language/copy_elision)
