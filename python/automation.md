
# Automation

## Check Disk Usage

```python
import shutil

def check_disk_usage(disk):
    du = shutil.disk_usage(disk)
    free = du.free / du.total * 100
    return free > 20
check_disk_usage('/')
```

## Check CPU Usage

```python
import psutil

def check_cpu_usage():
    usage = psutil.cpu_percent(1)
    return usage < 75
```

## Check localhost

```python
import socket

def check_localhost():
    localhost = socket.gethostbyname('localhost')
    return localhost == "127.0.0.1"
```

## Check connectivity

```python
import requests

def check_connectivity():
    request = requests.get("http://www.google.com")
    return request.status_code == 200
```

## Reading and writing files

[Link](https://docs.python.org/3/library/functions.html#open)

### Remove file

```python
import os

os.remove("file.txt")
```

### Rename file

```python
os.rename("original.txt", "new.txt")
```

### Check if file exists

```python
os.path.exists("file.txt")
```

### Get size of a file

```python
os.path.getsize("file.txt")
```

### Last modfied

```python
import datetime
timestamp = os.path.getmtime("file.txt")
datetime.datetime.fromtimestamp(timestamp)
```

### Get absolut path

```python
os.path.abspath("file.txt")
```

## Directories

### Get current working directory

```python
os.cwd()
```

### Change current working directory

```python
os.chdir("new_dir")
```

### Create dir

```python
os.mkdir("my_dir")
```

### Remove dir

```python
os.rmdir("my_dir")
```

### Get all files in dir

```python
os.listdir("my_dir")
```

## CSV

### Read

```python
import csv
with open("csv_file.txt") as f:
    csv_f = csv.reader(f)
    for row in csv_f:
        name, phone, role = row
```

### Write

```python
with open("csv_file.txt", "w") as f:
    writer = csv.writer(f)
    writer.writerows([["bla", "123"], ["blubb", "456"]])
```

### Read from dict

```python
with open("csv_file.txt") as f:
    reader = csv.DictReader(f)
    for row in reader:
        row["name"]
```

### Writing from dict

```python
with open("csv_file.txt", "w") as f:
    keys = ["name", "department"]
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    writer.writerows([{"name": "bob", "department": "dep1"}])
```

## Regex

* [regex101.com/](https://regex101.com/)
* [regex howto](https://docs.python.org/3/howto/regex.html)
* [re lib](https://docs.python.org/3/library/re.html)
* [greedy vs non-greedy](https://docs.python.org/3/howto/regex.html#greedy-versus-non-greedy)
* [Regex Cross­word](https://regexcrossword.com/)

`grep`, `sed`, `awk`

```python
import re
```

```python
result = re.search(r"aza", "plaza")
```

```python
result = re.search(r"p.eng", "Pangaea", re.IGNORECASE)
```

```python
result = re.search(r"[^a-zA-Z]", "This is a sentence with spaces.")
```

```python
result = re.findall(r"cat|dog", "I like both dogs and cats.")
```

```python
re.search(r"Py.*n", "Pygmalion")
```

* Match everything that begins with A and ends with a:

```python
re.search(r"^A.*a$", "Azerbaijan")
```

* Split on sentence:

```python
re.split(r"[.?!]", "One sentence. Another one? And the last one!")
```

* Split on sentence but add chars we split on:

```python
re.split(r"([.?!])", "One sentence. Another one? And the last one!")
```

* Substitute
```python
re.sub(r"[\w.%+-]+@[\w.-]+", "[REDACTED]", "Received an email for go_nuts95@my.example.com")
```

Better save than sorry

* Reorder matches

```python
re.sub(r"^([\w .-]*), ([\w .-]*)$", r"\2 \1", "Lovelace, Ada")
```

## Grep

```bash
grep  thon /usr/share/dict/words
```

* Ignore case

```bash
grep -i python /usr/share/dict/words
```

* Beginswith

```bash
grep ^fruit /usr/share/dict/words
```

* Endswith

```bash
grep cat$ /usr/share/dict/words
```

## Processes

* Access arguments

```python
sys.argv
```
* Access environment

```python
os.environ.get("PATH", "")
```

* Get exit value of the last command:

```bash
echo $?
```

```python
import subprocess
result = subprocess.run(["ls", "this_file_does_not_exist"])
result.returncode
# 2
```

Obtain output of system command

```python
result = subprocess.run(["host", "8.8.8.8"], capture_output=True)
result.returncode
# 0
result.stdout.decode("utf-8")
# '8.8.8.8.in-addr.arpa domain name pointer dns.google.\n'

result = subprocess.run(["rm", "doesnt_exist"], capture_output=True)
result.returncode
# 1
result.stderr.decode("utf-8")
# "rm: cannot remove 'doesnt_exist': No such file or directory\n"
```

* Pass modified environment

```python
my_env = os.environ.copy()
my_env["PATH"] = os.pathsep.join("/opt/myapp/", my_env["PATH"])
result = subprocess.run(["myapp"], env=my_env)

# result = subprocess.run(["myapp"], env=my_env, timeout=..., cwd=...)
```

## Testing

* [Monitoring Distributed Systems](https://landing.google.com/sre/sre-book/chapters/monitoring-distributed-systems/)
* [Testing reliability](https://landing.google.com/sre/sre-book/chapters/testing-reliability/)
* [Performance Testing](https://testing.googleblog.com/2007/10/performance-testing.html)
* [Smoke Testing](https://www.guru99.com/smoke-testing.html)
* [Exploratory Testing](https://www.guru99.com/exploratory-testing.html)
* [Test first is fun](https://testing.googleblog.com/2008/09/test-first-is-fun_08.html)

```python
#!/usr/bin/env python3
import unittest

from emails import find_email

class EmailsTest(unittest.TestCase):

  def test_basic(self):
    testcase = [None, "Bree", "Campbell"]
    expected = "breee@abc.edu"
    self.assertEqual(find_email(testcase), expected)

  def test_one_name(self):
    testcase = [None, "John"]
    expected = "Missing parameters"
    self.assertEqual(find_email(testcase), expected)

  def test_two_name(self):
    testcase = [None, "Roy","Cooper"]
    expected = "No email address found"
    self.assertEqual(find_email(testcase), expected)

if __name__ == '__main__':
  unittest.main()
```

## Exceptions

* [Exception Handling Techniques](https://doughellmann.com/blog/2009/06/19/python-exception-handling-techniques/)

# Source

* [Google IT Automation with Python Professional Certificate](https://www.coursera.org/professional-certificates/google-it-automation)
