
# Valgrind

## Installation

```bash
sudo apt-get install valgrind
```

## Usage

```bash
valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes --log-file=/home/workspace/valgrind-out.txt /home/workspace/a.out
```
