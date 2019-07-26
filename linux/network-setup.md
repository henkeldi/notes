
# Network Setup

*/etc/network/interfaces*

```bash
auto wlan0
iface wlan0 inet static
	post-up /usr/sbin/hostapd -B /etc/hostapd/hostapd.conf
	post-up service dnsmasq restart
    address 192.168.0.1
    netmask 255.255.255.0

allow-hotplug wlan1
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

dhcp-range=192.168.0.50,192.168.0.150,12h
```

## WPA Supplicant

```bash
network={
	ssid="My-Wifi"
	psk="my-password"
}
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
