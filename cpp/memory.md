
# Memory

* Cache information

```bash
$ lscpu | grep cache
L1d cache:                       128 KiB
L1i cache:                       128 KiB
L2 cache:                        1 MiB
L3 cache:                        6 MiB
Vulnerability L1tf:              Mitigation; PTE Inversion; VMX conditional cache flushes, SMT disabled
```

* [Timings for various operations](http://norvig.com/21-days.html#answers)

* Stack size

```bash
$ ulimit -s
8192
```