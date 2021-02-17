
# Smart Pointers

When using raw pointers you might run into the following bugs:

1. Memory leaks
1. Freeing memory that shouldn’t be freed
1. Freeing memory incorrectly
1. Using memory that has not yet been allocated
1. Thinking that memory is still allocated after being freed

That is why you need to use smart pointers.

* `std::unique_ptr` Exclusively owns a dynamically allocaed resource on the HEAP
* `std::shared_ptr` Points to a resource on a HEAP but does not explicitly own it. Has a reference count. Resource will be deallocated when count reaches zero
* `std::weak_ptr` same as shared but without reference count.


## std::unique_ptr

```c++
std::unique_ptr<int> unique(new int); // create a unique pointer on the stack
*unique = 2; // assign a value
// delete is not neccessary

auto destPtr = std::move(unique);
// destPtr now owns the resource
```

## std::shared_ptr

```c++
std::shared_ptr<int> ptr1(new int);
// cout << ptr1.use_count() = 1
{
  std::shared_ptr<int> ptr2 = ptr1;
  // cout << ptr1.use_count() = 2
}
// cout << ptr1.use_count() = 1
```

```c++
class MyClass {
};

int main() {
  std::shared_ptr<MyClass> shared(new MyClass);
  // cout << ptr1.use_count() = 1

  shared.reset(new MyClass);
  // cout << ptr1.use_count() = 1
}
```

* Problem with shared pointers: Circular references:

```c++
class MyClass
{
public:
  std::shared_ptr<MyClass> _member;
  ~MyClass() { }
};

int main() {
  std::shared_ptr<MyClass> myClass1(new MyClass);
  std::shared_ptr<MyClass> myClass2(new MyClass);
  
  myClass1->_member = myClass2;
  myClass2->_member = myClass1;
}
```

## std::weak_ptr

```c++
int main()
{
  std::shared_ptr<int> mySharedPtr(new int);
    // cout << mySharedPtr.use_count() = 1

  std::weak_ptr<int> myWeakPtr1(mySharedPtr);
  std::weak_ptr<int> myWeakPtr2(myWeakPtr1);
  // cout << mySharedPtr.use_count() = 1
}
```

```c++
int main() {
  std::shared_ptr<int> mySharedPtr(new int);
  std::weak_ptr<int> myWeakPtr(mySharedPtr);

  mySharedPtr.reset(new int);

  if (myWeakPtr.expired() == true) {
      std::cout << "Weak pointer expired!" << std::endl;
  }
}
```

## Conversion

```c++
int main() {
  // construct a unique pointer
  std::unique_ptr<int> uniquePtr(new int);
  
  // (1) shared pointer from unique pointer
  std::shared_ptr<int> sharedPtr1 = std::move(uniquePtr);

  // (2) shared pointer from weak pointer
  std::weak_ptr<int> weakPtr(sharedPtr1);
  std::shared_ptr<int> sharedPtr2 = weakPtr.lock();

  // (3) raw pointer from shared (or unique) pointer   
  int *rawPtr = sharedPtr2.get();
  delete rawPtr;
}
```

## Recommendations

* Use unique_ptr or shared_ptr to represent ownership
* Prefer unique_ptr over std::shared_ptr unless you need to share ownership
* Use make_shared() to make shared_ptr
* Use make_unique() to make std::unique_ptr
* Use weak_ptr to break cycles of shared_ptr

## How to decide which pointer to use

* Do you want to be able to pass nullptr -> use f(object*)
* otherwise use f(object&)
* Express that the function is now responsible for the object f(unique_ptr<object>)
* Express that the function is sharing an object use f(shared_ptr<object>)

# Source

* [Udacity c++ nanodegree](https://www.udacity.com/course/c-plus-plus-nanodegree--nd213)
* [CppCoreGuidelines Smart pointers](http://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rsmart-smart-pointers)
