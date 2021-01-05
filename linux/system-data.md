
# System Data

## Name of the operating system

```bash
$ cat /etc/os-release
NAME="Ubuntu"
VERSION="20.04.1 LTS (Focal Fossa)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 20.04.1 LTS"
VERSION_ID="20.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=focal
UBUNTU_CODENAME=focal
```

## Kernel version

```bash
$ cat /proc/version
Linux version 5.4.0-58-generic (buildd@lcy01-amd64-004) (gcc version 9.3.0 (Ubuntu 9.3.0-17ubuntu1~20.04)) #64-Ubuntu SMP Wed Dec 9 08:16:25 UTC 2020
```

## Memory Utilization

```bash
$ cat /proc/meminfo
MemTotal:       16341792 kB
MemFree:          984212 kB
MemAvailable:    3276228 kB
Buffers:          203020 kB
[...]
```

## Total processes

```bash
$ cat /proc/stat
[...]
processes 28684
[...]
```

## Running processes

```bash
$ cat /proc/stat
[...]
procs_running 2
[...]
```

## Up time

```bash
$ cat /proc/uptime
38552.52 102314.56
```

## Process info

```bash
$ cat /proc/[PID]/status
Name:	rcu_sched
Umask:	0000
State:	I (idle)
Tgid:	11
Ngid:	0
Pid:	11
PPid:	2
TracerPid:	0
Uid:	0	0	0	0
Gid:	0	0	0	0
FDSize:	64
Groups:	 
NStgid:	11
NSpid:	11
NSpgid:	0
NSsid:	0
Threads:	1
SigQ:	0/63597
SigPnd:	0000000000000000
ShdPnd:	0000000000000000
SigBlk:	0000000000000000
SigIgn:	ffffffffffffffff
SigCgt:	0000000000000000
CapInh:	0000000000000000
CapPrm:	0000003fffffffff
CapEff:	0000003fffffffff
CapBnd:	0000003fffffffff
CapAmb:	0000000000000000
NoNewPrivs:	0
Seccomp:	0
Speculation_Store_Bypass:	thread vulnerable
Cpus_allowed:	f
Cpus_allowed_list:	0-3
Mems_allowed:	00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000001
Mems_allowed_list:	0
voluntary_ctxt_switches:	26956
nonvoluntary_ctxt_switches:	12
```

## UID to username

```bash
$ cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
[...]
```

## CPU utilization

```bash
$ cat /proc/[PID]/stat
11 (rcu_sched) I 2 0 0 0 -1 2129984 0 0 0 0 0 36 0 0 20 0 1 0 14 0 0 18446744073709551615 0 0 0 0 0 0 0 2147483647 0 0 0 0 17 2 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Command used to launch a process

```bash
$ cat /proc/[pid]/cmdline
/usr/libexec/gvfs-gphoto2-volume-monitor
```
