# Working with pcaps

## Capturing packets
todo

## Viewing pcap data
todo

## Combining pcaps
mergecap can combine several pcaps into one, generally you can use this to reassemble pcaps split via tcpdump rotating file writer, or split pcaps in order to facilitate data exchange.

```shell
sudo apt install wireshark-common
mergecap -w merged.pcap data/*.pcap*
```

## Splitting pcaps
You may be interested in hunting a specific conversation or are only interested in specific sources/destinations

Generally speaking its not fun to wait for 10G+ packet captures to load, so why not extract out what we are interested in looking at

Depending on the level of detail needed, you can write a subset of packet capture data to a new packet capture, or dump the resultant tcpdump data to disk for further analysis

### Extracting packets with SYN flag only
```sh
# Write subset to pcap
tcpdump -r source.pcap 'tcp[13]=2' -w synpackets.pcap

# Write output to disk and parse manually
tcpdump -nn -r source.pcap 'tcp[13]=2' > synpackets.tcpdump.output
```

### Extract SYN/ACK packets
```sh
# Write subset to pcap
tcpdump -r source.pcap 'tcp[13]=18' -w SApackets.pcap

# Write output to disk and parse manually
tcpdump -nn -r source.pcap 'tcp[13]=18' > SA.tcpdump.output
```

### Extract SYN or SYN/ACK packets
```sh
# Write subset to pcap
tcpdump -r source.pcap 'tcp[13]=18' or 'tcp[13]=2' > tcpstep1-2.pcap

# Write output to disk and parse manually
tcpdump -nn -r source.pcap 'tcp[13]=18' or 'tcp[13]=2' > tcpstep1-2.tcpdump.output
```

### Extracting packets from a bad source to a destination network
```sh
# Write subset to pcap
tcpdump -r source.pcap '(src host 8.8.8.8) and (dst net 192.168.1.0/24)' -w bad-traffic.pcap

# Write output to disk and parse manually
tcpdump -nn -r source.pcap '(src host 8.8.8.8) and (dst net 192.168.1.0/24)' > bad-traffic.tcpdump.output
```

### Extract a specific bad interaction between two hosts
```sh
# Write subset to pcap
tcpdump -r source.pcap '(host 192.168.1.60) and (host 74.110.23.18) and (port 58636)' -w bad-convo.pcap

# Write output to disk and parse manually
tcpdump -nn -r source.pcap '(host 192.168.1.60) and (host 74.110.23.18) and (port 58636)' > bad-convo.tcpdump.output
```

### Hunt for active rfc1918 hosts having tcp connections
```sh
# Write subset to pcap
tcpdump -r source.pcap '(tcp[13]=0x12 or tcp[13]=0x02) and (net 192.168.0.0/16 or net 10.0.0.0/8 or net 172.16.0.0/12)' -w rfc1918.pcap

# Write output to disk and parse manually
tcpdump -nn -r source.pcap '(tcp[13]=0x12 or tcp[13]=0x02) and (net 192.168.0.0/16 or net 10.0.0.0/8 or net 172.16.0.0/12)' > rfc1918.tcpdump.output
```
