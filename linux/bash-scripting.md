
# Bash scripting

Redirect Streams

```python
#!/usr/bin/env python3
data = input("This will come from STDIN: ")
print("Now we write to STDOUT: " + data)
raise ValueError("Now generate an error to STDERR")
```

```bash
./streams_err.py < new_file.txt 2> error_file.txt
```

Get word frequency:

```bash
cat spider.txt | tr ' ' '\n' | sort | uniq -c | sort -nr | head
```

```python
#!/usr/bin/env python3
import sys
for line in sys.stdin:
    print(line.strip().capitalize())
```

```bash
cat file.txt | capitalize.py
```

## If Statements

```bash
if grep "127.0.0.1" /etc/hosts; then
    echo "Everythin ok"
else
    echo "ERROR! 127.0.0.1 is not in /etc/hosts"
fi
```

check if variable is empty

```bash
if test -n "$PATH"; then echo "Your path is not empty"; fi
```

or

```bash
if [ -n "$PATH" ]; then echo "Your path is not empty"; fi
```

* [Bash Scripting Tutorial](https://ryanstutorials.net/bash-scripting-tutorial/)
* [Bash Scripting Tutorial for Beginners](https://linuxconfig.org/bash-scripting-tutorial-for-beginners)
* [Shellscript.sh](https://www.shellscript.sh)

## While Loops

```bash
#!/bin/bash

n=1
while [ $n -le 5 ]; do
    echo "Iteration number $n"
    ((n+=1))
done
```

Retry to execute a command

```bash
#!/bin/bash
n=0
command=$1
while ! $command && [ $n -le 5 ]; do
    sleep $n
    ((n=n+1))
    echo "Retry #$n"
done;
```

```bash
retry.sh some_program.py
```

## For Loops

```bash
for fruit in peach orange apple; do
    echo "I like $fruit!"
done
```

Rename files

```bash
for file in *.HTM; do
    name=$(basename "$file" .HTM)
    echo mv "$file" "$name.html"
done
```

## Advanced Command Interaction

```bash
tail /var/log/syslog | cut -d' ' -f5-
```

# Source

* [Google IT Automation with Python Professional Certificate](https://www.coursera.org/professional-certificates/google-it-automation)
