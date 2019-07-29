
# Network Setup

*/etc/network/interfaces*

```bash
auto eth0
iface eth0 inet static
  address 192.168.6.1
  netmask 255.255.255.0

auto wlan0
iface wlan0 inet static
  hostapd /etc/hostapd/hostapd.conf
  post-up service dnsmasq restart
  address 192.168.4.1
  netmask 255.255.255.0

auto wlan1
iface wlan1 inet dhcp
  post-up iptables-restore < /etc/iptables/rules.v4
  wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
```

Prevent Networkmanager from managing the interface

*/etc/NetworkManager/NetworkManager.conf*

```bash
# ...

[keyfile]
unmanaged-devices=c6:f9:24:1d:65:f3
```

## DHCP

*/etc/dnsmasq.conf*

```bash
# To disable DNS
port=0

# To enable DNS
# port=0
server=8.8.8.8

dhcp-range=192.168.0.50,192.168.0.150,12h
```

## Resolvconf
*/etc/resolvconf/resolv.conf.d/base*
```bash
nameserver 8.8.8.8
nameserver 8.8.4.4
```
Update:
```bash
sudo resolvconf -u
```

## systemd-resolved

Disable:
```bash
sudo systemctl disable systemd-resolved.service
```

Test DNS Server:
```bash
host www.google.com 192.168.3.1
```

## WPA Supplicant

```bash
network={
	ssid="My-Wifi"
	psk="my-password"
}
```

## IP Tables
```bash
sudo iptables -A FORWARD -i <src> -o <dst> -j ACCEPT
sudo iptables -A FORWARD -i <dst> -o <src> -m state --state ESTABLISHED,RELATED -j ACCEPT
sudo iptables -t nat -A POSTROUTING -o <src> -j MASQUERADE
```

## Hostapd

```bash
interface=wlan1
ssid=<ssid>
country_code=DE
hw_mode=g
channel=1
wpa=2
wpa_passphrase=<wpa-passphrase>

## Key management algorithms ##
wpa_key_mgmt=WPA-PSK
 
## Set cipher suites (encryption algorithms) ##
## TKIP = Temporal Key Integrity Protocol
## CCMP = AES in Counter mode with CBC-MAC
wpa_pairwise=TKIP
rsn_pairwise=CCMP
 
## Shared Key Authentication ##
auth_algs=1
 
## Accept all MAC address ###
macaddr_acl=0
```

# SSH
*~/.ssh/config*
```bash
Host jetson
  HostName 192.168.178.38
  User jetson
```

# Inputrc

*~/.inputrc*

```bash
## arrow up
"\e[A":history-search-backward
## arrow down
"\e[B":history-search-forward
```

## Build wifi-driver for Jetson Nano

Download [Driver](https://www.tp-link.com/de/support/download/archer-t4u/v3/).

```bash
make clean
ARCH=arm64 make -j4
sudo cp 88xbu.ko /lib/modules/<kernel-version>/kernel/drivers/net/wireless
sudo depmod -a
sudo modprobe 88x2bu.ko
```
# Source
* [cyberciti setting-wireless-access-point](https://www.cyberciti.biz/faq/debian-ubuntu-linux-setting-wireless-access-point/)
