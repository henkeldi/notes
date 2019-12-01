
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
// macro  -> operator
// and    -> &&
// and_eq -> &=
// bitand -> &
// bitor  -> |
// compl  -> ~
// not    -> !
// not_eq -> !=
// or     -> ||
// or_eq  -> |=
// xor    -> ^
// xor_eq -> ^=
```

</details>

<details><summary>climits</summary>

[climits](http://www.cplusplus.com/reference/climits/)

```cpp
// CHAR_BIT   -> Number of bits in a char object (byte)
// SCHAR_MIN  -> Minimum value for an object of type signed char
// SCHAR_MAX  -> Maximum value for an object of type signed char
// UCHAR_MAX  -> Maximum value for an object of type unsigned char
// CHAR_MIN   -> Minimum value for an object of type char
// CHAR_MAX   -> Maximum value for an object of type char
// MB_LEN_MAX -> Maximum number of bytes in a multibyte character, for any locale
// SHRT_MIN   -> Minimum value for an object of type short int
// SHRT_MAX   -> Maximum value for an object of type short int
// USHRT_MAX  -> Maximum value for an object of type unsigned short int
// INT_MIN    -> Minimum value for an object of type int
// INT_MAX    -> Maximum value for an object of type int
// UINT_MAX   -> Maximum value for an object of type unsigned int
// LONG_MIN   -> Minimum value for an object of type long int
// LONG_MAX   -> Maximum value for an object of type long int
// ULONG_MAX  -> Maximum value for an object of type unsigned long int
// LLONG_MIN  -> Minimum value for an object of type long long int
// LLONG_MAX  -> Maximum value for an object of type long long int
// ULLONG_MAX -> Maximum value for an object of type unsigned long long int
```

</details>

<details><summary>clocale</summary>

[clocale](http://www.cplusplus.com/reference/clocale/)

```cpp
// Return name of current locale:
setlocale(LC_ALL, NULL);

setlocale(LC_ALL, "C");
// setlocale(<category>, <locale>);

// category:
// LC_ALL -> The entire locale.
// LC_COLLATE -> Affects the behavior of strcoll and strxfrm.
// LC_CTYPE -> Affects character handling functions (all functions of <cctype>, except isdigit and isxdigit), and the multibyte and wide character functions.
// LC_MONETARY -> Affects monetary formatting information returned by localeconv.
// LC_NUMERIC -> Affects the decimal-point character in formatted input/output operations and string formatting functions, as well as non-monetary information returned by localeconv.
// LC_TIME -> Affects the behavior of strftime.

// locale:
// "C" -> Minimal "C" locale
// "" -> Environment's default locale

struct lconv * lc;
lc = localeconv();
printf("Local Currency Symbol: %s\n",lc->currency_symbol);
```

```bash
Local Currency Symbol: $
```

</details>

<details><summary>cmath</summary>

[cmath](http://www.cplusplus.com/reference/cmath/)

```cpp
// Trigonometric functions
cos()
sin()
tan()
acos()
asin()
atan()
atan2(x, y)

// Hyperbolic functions
cosh()
sinh()
tanh()
acosh()
asinh()
atanh()

// Exponential and logarithmic functions
exp()
frexp()
ldexp()
log()
log10()
modf()
exp2()
expm1()
ilogb()
log1p()
log2()
logb()
scalbn()
scalbln()

// Power functions
pow()
sqrt()
cbrt()
hypot()

// Error and gamma functions
erf()
erfc()
tgamma()
lgamma()

// Rounding and remainder functions
cell()
floor()
fmod()
trunc()
round()
lround()
llround()
rint()
lrint()
llrint()
nearbyint()
remainder()
remquo()

// Floating-point manipulation functions
copysign(x, y)  // ->  Returns a value with the magnitude of x and the sign of y.
nan()
nextafter()
nexttoward()

// Minimum, maximum, difference functions
fdim()
fmax()
fmin()

// Other functions
fabs()
abs()
fma() // -> Multiply-add

// Classification macro / functions
fpclassify()
isfinite()
isinf()
isnan()
isnormal()
signbit()

// Comparison macro / functions
isgreater(x, y)
isgreaterequal(x, y)
isless(x, y)
islessqual(x, y)
islessgreater(x, y)
isunordered(x, y)
```

</details>

<details><summary>csignal</summary>

```c++
// Integral type of an object that can be accessed as an atomic entity,
// even in the presence of asynchronous signals.
sig_atomic_t signaled = 0;

void my_handler(int param) {
  signaled = 1;
}

int main () {
  void (*prev_handler)(int);

  prev_handler = signal(SIGINT, my_handler);
  // prev_handler = signal(SIGINT, SIG_DFL); // Default handler
  // prev_handler = signal(SIGINT, SIG_IGN); // Ignore signal
  // SIGABRT -> (Signal Abort) Abnormal termination, such as is initiated by the abort function.
  // SIGFPE -> Signal Floating-Point Exception
  // SIGILL -> Signal Illegal Instruction
  // SIGINT -> CTRL+C
  // SIGSEGV -> Signal Segmentation Violation
  // SIGTERM -> Termination request sent to program.

  // Generates a signal
  raise(SIGINT);
  
  printf ("signaled is %d.\n",signaled);

  return 0;
}
```

</details>

<details><summary>cargs</summary>

```c++
void PrintFloats (int n, ...) {
  int i;
  double val;
  printf ("Printing floats:");
  va_list vl;
  va_start(vl,n);
  for (i=0;i<n;i++) {
    val=va_arg(vl,double);
    printf (" [%.2f]",val);
  }
  va_end(vl);
  printf ("\n");
}

int main () {
  PrintFloats (3,3.14159,2.71828,1.41421);
  return 0;
}
```

```bash
Printing floats: [3.14] [2.72] [1.41]
```

</details>

<details><summary>cstdbool</summary>

```c++
true  // -> 1
false // -> 0
```

</details>

<details><summary>cstddef</summary>

```c++
// NULL
int* p = NULL;

// offsetof
struct S {
    char c;
    double d;
};
offsetof(S, c)

// size_t
std::array<std::size_t, 10> a;
for (std::size_t i = 0; i != a.size(); ++i) {
  a[i] = i;
}

// ptrdiff_t
// nullptr_t
// max_align_t
// byte
```

</details>

<details><summary>cstdint</summary>

```c++
int8_t
int16_t
int32_t
int64_t

uint8_t
uint16_t
uint32_t
uint64_t

INT8_{MIN, MAX}
INT16_{MIN, MAX}
INT32_{MIN, MAX}
INT64_{MIN, MAX}

UINT8_{MIN, MAX}
UINT16_{MIN, MAX}
UINT32_{MIN, MAX}
UINT64_{MIN, MAX}

SIZE_MAX // maximum of std::size_t
```

</details>

<details><summary>cstdio</summary>

**Operations on files**

<details><summary>remove</summary>

* [Remove file](http://www.cplusplus.com/reference/cstdio/remove/)

```c++
if (remove( "myfile.txt" ) != 0) {
  perror( "Error deleting file" );
} else {
  puts( "File successfully deleted" );
}
```

</details>

<details><summary>rename</summary>

* [Rename file](http://www.cplusplus.com/reference/cstdio/rename/)

```c++
result= rename("oldname.txt", "newname.txt");
if (result == 0) {
  puts("File successfully renamed");
} else {
  perror("Error renaming file");
}
```

</details>

<details><summary>tmpfile</summary>

* [Open a temporary file](http://www.cplusplus.com/reference/cstdio/tmpfile/)

```c++
FILE * pFile;
pFile = tmpfile();
```

</details>

<details><summary>tmpnam</summary>

* [Generate temporary filename](http://www.cplusplus.com/reference/cstdio/tmpnam/)
* Prints during compile time: *warning: the use of `tmpnam' is dangerous, better use `mkstemp'*

```c++
char buffer [L_tmpnam];
tmpnam(buffer);
```

```bash
/tmp/fileP7OWys
```

</details>

**File access**

<details><summary>fclose</summary>

* Close file

```c++
FILE* pFile;
pFile = fopen("myfile.txt","wt");
fprintf(pFile, "fclose example");
fclose(pFile);
```

</details>


<details><summary>fflush</summary>

* Flush stream

```c++
FILE* pFile;
pFile = fopen("example.txt","r+");
fputs("test", pFile);
fflush(pFile);
```

</details>

<details><summary>fopen</summary>

* [Open file](http://www.cplusplus.com/reference/cstdio/fopen/)

```c++
FILE* pFile;
pFile = fopen("myfile.txt", "w");
// mode:
// r  -> read mode
// w  -> write mode
// a  -> append mode
// r+ -> read/write mode
// w+ -> read/write mode, overwrite if file already exists
// a+ -> read/write mode, all output goes to end of file

if (pFile!=NULL) {
  fputs("fopen example", pFile);
  fclose(pFile);
}
```

</details>

<details><summary>fropen</summary>

* [Reopen stream with different file or mode](http://www.cplusplus.com/reference/cstdio/freopen/)

```c++
freopen("myfile.txt", "w", stdout);
printf("This sentence is redirected to a file.");
fclose(stdout);
```

</details>

<details><summary>setbuf</summary>

* [Set stream buffer](http://www.cplusplus.com/reference/cstdio/setbuf/)

```c++
char buffer[BUFSIZ];
FILE *pFile1, *pFile2;

pFile1= fopen("myfile1.txt", "w");
pFile2= fopen("myfile2.txt", "a");

setbuf(pFile1, buffer);
fputs("This is sent to a buffered stream", pFile1);
fflush(pFile1);

setbuf(pFile2, NULL);
fputs("This is sent to an unbuffered stream", pFile2);

fclose(pFile1);
fclose(pFile2);
```

</details>

<details><summary>setvbuf</summary>

* [Change stream buffering](http://www.cplusplus.com/reference/cstdio/setvbuf/)

```c++
FILE *pFile;
pFile=fopen("myfile.txt", "w");
setvbuf(pFile, NULL, _IOFBF, 1024);
// <stream>, <buffer>, <mode>, <size>

// buffer:
//  * User allocated buffer. Shall be at least size bytes long.
//  * If set to a null pointer, the function automatically allocates a buffer.

// mode:
//  * _IOFBF Full buffering
//  * _IOLBF Line buffering
//  * _IONBF No buffering

// size:
//  * in bytes

// File operations here

fclose (pFile);
```

</details>

**Formatted input/output**

<details><summary>array</summary>

#### Initialize

```c++
std::array<int, 5> myarray = { 2, 16, 77, 34, 50 };
```

#### Iterate

```c++
for (auto it = myarray.begin(); it != myarray.end(); ++it) {
  std::cout << ' ' << *it;
}
```

```bash
2 16 77 34 50
```

#### Iterate reversed

```c++
for (auto it = myarray.rbegin(); it != myarray.rend(); ++rit) {
  std::cout << ' ' << *rit;
}
```

```bash
50 34 77 16 2
```

#### Fill with values

```c++
myarray.fill(5);
```

```bash
5 5 5 5 5 5
```

#### Access data

```c++
// Without bounds check
for (int i=0; i<10; i++) {
  myarray[i]=i;
}

// With bounds check
// Throws out_of_range exception
for (int i=0; i<10; i++) {
  myarray.at(i) = i+1;
}

for (int& x : myarray) {
  std::cout << ' ' << x;
}

myarray.first();
myarray.back();
myarray.front() = 100;

// Access raw associated data:
myarray.data()
```

#### Swap two arrays

```c++
first.swap(second);
// must be same type and length
```

</details>

### Containers

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
