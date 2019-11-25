
# C++

## Libraries

### C Library

<details><summary>cassert</summary>

```cpp
assert(("There are five lights", 2 + 2 == 5));
```

```bash
test: test.cc:10: int main(): Assertion `((void)"There are five lights", 2+2==5)' failed.
Aborted
```

</details>

<details><summary>cctype</summary>

```cpp
// 0-9a-zA-Z
isalnum()

// a-zA-Z
isalpha()

// tab (\t), space( )
isblank()

// NUL, \t, \f, \v, \n, \r, DEL
iscntrl()

// 0-9
isdigit()

// a-z
islower()

// A-Z
isupper()

// all printable characters
isprint()

// !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
ispunct()

// \t, \f, \v, \n, \r, space( )
isspace()

// 0123456789 ABCDEF abcdef
isxdigit()
```

</details>

### Misc

<details><summary>algorithm</summary>

<details><summary>shuffle</summary>

```cpp
std::vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
std::random_device rd;
std::mt19937 g(rd());
std::shuffle(v.begin(), v.end(), g);
```

```bash
8 6 10 4 2 3 7 1 9 5
```
</details>

<details><summary>{all, any, none}_of</summary>

```c++
std::vector<int> v(10, 2);
if (std::all_of(v.cbegin(), v.cend(), [](int i){ return i % 2 == 0; })) {
    std::cout << "All numbers are even\n";
}
```

```bash
All numbers are even
```
</details>

<details><summary>find</summary>

```c++
std::vector<int> v{0, 1, 2, 3, 4};
auto result1 = std::find(std::begin(v), std::end(v), 3);
if (result1 != std::end(v)) {
    std::cout << "v contains: 3\n";
} else {
    std::cout << "v does not contain: " << n1 << '\n';
}
```

```bash
v contains: 3
```
</details>

<details><summary>transform</summary>

```c++
std::string s("hello");
std::transform(s.begin(), s.end(), s.begin(),
                [](unsigned char c) -> unsigned char { return std::toupper(c); });
```

```bash
HELLO
```
</details>

<details><summary>max</summary>

```c++
std::cout << "larger of 1 and 9999: " << std::max(1, 9999) << '\n';
```
```bash
larger of 1 and 9999: 9999
```
</details>

<details><summary>clamp</summary>

```c++
std::clamp(10, 0, 100);
std::clamp(-10, 0, 100);
```
```bash
10
0
```
</details>

<details><summary>next_permutation</summary>

```c++
std::string s = "aba";
std::sort(s.begin(), s.end());
do {
    std::cout << s << '\n';
} while(std::next_permutation(s.begin(), s.end()));
```

```bash
aab
aba
baa
```
</details>

</details>
