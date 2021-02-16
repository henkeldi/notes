
# C++ Basics

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

* [Include guards](https://github.com/isocpp/CppCoreGuidelines/blob/master/CppCoreGuidelines.md#Rs-guards)

# Source

* [A Tour of C++ Second Edition](http://www.stroustrup.com/tour2.html)
* [Build automation software](https://en.wikipedia.org/wiki/List_of_build_automation_software)
* [Awesome C++](https://awesomecpp.com/)
