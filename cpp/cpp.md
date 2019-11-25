
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

<details><summary>cerrno</summary>

```cpp
double not_a_number = std::log(-1.0);
if (errno == EDOM) {
    std::cout << "log(-1) failed: " << std::strerror(errno) << '\n';
}

// E2BIG -> Argument list too long
// EACCES -> Permission denied
// EADDRINUSE -> Address in use
// EADDRNOTAVAIL -> Address not available
// EAFNOSUPPORT ->  Address family not supported
// EAGAIN -> Resource unavailable, try again
// EALREADY -> Connection already in progress
// EBADF -> Bad file descriptor
// EBADMSG -> Bad message
// EBUSY -> Device or resource busy
// ECANCELED -> Operation canceled
// ECHILD -> No child processes
// ECONNABORTED -> Connection aborted
// ECONNREFUSED -> Connection refused
// ECONNRESET -> Connection reset
// EDEADLK -> Resource deadlock would occur
// EDESTADDRREQ -> Destination address required
// EDOM -> Mathematics argument out of domain of function
// EEXIST -> File exists
// ...
```

```bash
log(-1) failed: Numerical argument out of domain
```

</details>

<details><summary>ciso646</summary>

```cpp
// macro -> operator
// and -> &&
// and_eq -> &=
// bitand -> &
// bitor -> |
// compl -> ~
// not -> !
// not_eq -> !=
// or -> ||
// or_eq -> |=
// xor -> ^
// xor_eq -> ^=
```

</details>

<details><summary>climits</summary>

```cpp
// CHAR_BIT -> Number of bits in a char object (byte)
// SCHAR_MIN -> Minimum value for an object of type signed char
// SCHAR_MAX -> Maximum value for an object of type signed char
// UCHAR_MAX -> Maximum value for an object of type unsigned char
// CHAR_MIN -> Minimum value for an object of type char
// CHAR_MAX -> Maximum value for an object of type char
// MB_LEN_MAX -> Maximum number of bytes in a multibyte character, for any locale
// SHRT_MIN -> Minimum value for an object of type short int
// SHRT_MAX -> Maximum value for an object of type short int
// USHRT_MAX -> Maximum value for an object of type unsigned short int
// INT_MIN -> Minimum value for an object of type int
// INT_MAX -> Maximum value for an object of type int
// UINT_MAX -> Maximum value for an object of type unsigned int
// LONG_MIN -> Minimum value for an object of type long int
// LONG_MAX -> Maximum value for an object of type long int
// ULONG_MAX -> Maximum value for an object of type unsigned long int
// LLONG_MIN -> Minimum value for an object of type long long int
// LLONG_MAX -> Maximum value for an object of type long long int
// ULLONG_MAX -> Maximum value for an object of type unsigned long long int
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
