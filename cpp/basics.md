
# C++ Basics


* Inventor: `Bjarne Stroustrup`
*  Is an Compiled Language: Advantage Compiler checks rules before you run the code, code runs 10-15 times faster then alternatives

## Install

```bash
sudo apt update
sudo apt install build-essential
sudo apt install gdb
```

* Install extensions for VSCode: `C/C++` and `clang-format`
* Press ctrl + shift + i to format.

## Debug

`g++ build and debug active file` in launch.json add `"program": "${workspaceFolder}/a.out",`

## Basics

<details>

<summary>Output</summary>

```c++
#include <iostream>
using std::cout;

int main() {
    cout << "Hello!\n";
}
```

</details>

<details>

<summary>Vector</summary>

```c++
#include <iostream>
using std::vector;

void doStuff(const vector<int> &v) {
    for (const int &i: v) {

    }
}

int main() {
    vector<int> numbers{0, 1, 2};
    numbers.size();
    doStuff(numbers);
    numbers.push_back(3);
}
```

</details>

<details>

<summary>Reading from file</summary>

```c++
#include <fstream>

std::ifstream my_file {<path>};

if (my_file) {
    // file stream has been created!
    for (std::string line; getline(my_file, line);) {
        // use line here
    }
}
```

</details>

<details>

<summary>String to int</summary>

```c++
#include <sstream>
#include <string>

int main() {
    std::string a("1,2,3,");
    std::isstringstream my_stream(a);
    char c;
    int n;
    while(my_stream >> n >> c) {
        std::cout << n << std::endl;
    }
}
```

</details>

<details>

<summary>Enums</summary>

```c++
enum class State {kEmpty, kObstacle};

State my_state = State::kEmpty;
```

</details>

## Concurrency

### Create a Thread

```c++
void f(const std::vector<double>& v);

std::vector<double> vec{1, 2, 3, 4, 5, 6};
std::thread t{f, std::ref(vec)};
t.join();
```

### Sharing Data

```c++
std::mutex m;
int data;

void f() {
    scoped_lock lock{m};
    data += 3;
}
```

```c++
std::shared_mutex mx;

void reader() {
    std::shared_lock lock{mx};
    // read
}

void writer() {
    std::unique_lock lock{mx};
    // write
}
```

### Waiting for events

```c++
using namespace std::chrono;

using namespace std::chrono_literals;
std::this_thread::sleep_for(10ms);
```

```c++
std::queue<Message> mqueue;
std::conditional_variable mcond;
std::mutex mmutex;

void consumer() {
    while(true) {
        std::unique_lock lck {mmutex};
        mcond.wait(lck, []{return !mqueue.empty();});
        auto m = mqueue.front();
        mqueue.pop();
        lck.unlock();
        // process m
    }
}

void producer() {
    while(true) {
        Message m;
        scoped_lock lck {mmutex};
        mqueue.push(m);
        mcond.notify_one();
    }
}
```

```c++
void f(std::promise<X>& px) {
    X res;
    px.set_value(res);
    // px.set_exception(current_exception());
}

void g(std::promise<X>& fx) {
    X v = fx.get();
}
```

```c++
double accum(double* beg, double* end, double init) {
    return accumulate(beg, end, init);
}

double comp2(std::vector<double>& v) {
    using Task_type = double(double*,double*,double);

    std::packaged_task<Task_type> pt0 {accum};
    std::packaged_task<Task_type> pt1 {accum};

    std::future<double> f0 {pt0.get_future()};
    std::future<double> f1 {pt1.get_future()};

    double* first = &v[0];
    std::thread t1 {std::move(pt0), first, first+v.size()/2,0}
    std::thread t2 {std::move(pt1), first+v.size()/2, first+v.size(),0}

    return f0.get() + f1.get();
}
```

```c++
#include <chrono>
#include <future>

int g() {
    using namespace std::chrono_literals;
    std::this_thread::sleep_for(10s); // simulate work
    return 10;
}

auto f = async(g);
f.get();
```

### Map

```c++
#include <unordered_map>

std::unordered_map <string, vector<string>> my_dictionary;

if (my_dictionary.find(key) == my_dictionary.end()) {
    my_dictionary[key] = vector<string> {"foo", "bar"};
}
```

### Operator Overloading

```c++
class Matrix {
public:
  int& operator()(int row, int column) {
      return values_[row][column];
  }
}
```

### Virtual Functions

```c++
// If it's "= 0" means its a pure virtual function
// which means the child class HAS TO overload the method
class Animal {
  virtual void Talk() const = 0;
};

// Add override keyword is best practice but not required.
class Human : public Animal {
public:
  void Talk() const override;
};

void Human::Talk() const { std::cout << "Hey!\n"; }
```

### Template

```c++
template <typename T>
T Max(T a, T b) {
    return a > b ? a : b;
}
```

```c++
template <typename KeyType, typename ValueType>
class Mapping {
public:
  Mapping(KeyType key, ValueType value) : key(key), value(value) {}
  KeyType key;
  ValueType value;
};
```

## Measure Time

```c++
#include <chrono>

auto t1 = std::chrono::high_resolution_clock::now();
dostuff();
auto t2 = std::chrono::high_resolution_clock::now();
auto duration = std::chrono::duration_cast<std::chrono::microseconds>(t2 - t1).count();
std::cout << "Execution time: " << duration << " microseconds" << std::endl;
```

## Random number

```c++
#include <random>
#include <ctime>

std::mt19937 generator(int(std::time(0)));
std::uniform_int_distribution<int> dis(0, answers.size() - 1);

std::random_device rd;
std::mt19937 generator(rd());
auto random = std::bind(std::uniform_real_distribution<double>(0,1), generator);
```

## Include Guards

* [Include guards](https://github.com/isocpp/CppCoreGuidelines/blob/master/CppCoreGuidelines.md#Rs-guards)

## C++ Core Guidelines

* [Avoid trivial getter and setter](https://github.com/isocpp/CppCoreGuidelines/blob/master/CppCoreGuidelines.md#Rh-get)

# Source

* [A Tour of C++ Second Edition](http://www.stroustrup.com/tour2.html)
* [Build automation software](https://en.wikipedia.org/wiki/List_of_build_automation_software)
* [Abseil](https://abseil.io)
* [Zealdocs](https://zealdocs.org/)

* [Udacity C++](https://www.udacity.com/)
* [C++ Best Practice Guidelines](https://github.com/isocpp/CppCoreGuidelines)
* [C++ Standard Library](http://www.cplusplus.com/reference/)
* [List of C++ compilers](https://www.stroustrup.com/compilers.html)
* [GNU Make](https://www.gnu.org/software/make/manual/html_node/index.html#Top)
* [CMake](https://cmake.org/)
* [C++ Core Guidlines: Naming and layout rules](http://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#nl-naming-and-layout-rules)
* [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
* [Mozilla Coding Style: C/C++ practices](https://developer.mozilla.org/en-US/docs/Mozilla/Developer_guide/Coding_Style#CC_practices)
