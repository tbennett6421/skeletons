# Showing information

Show `MAC address` mapping to `interfaces`
```
show ethernet-switching table
```

Show interface `port status` and `type`
```
show interfaces terse
```

Show interface details including `STP status`, `port status`, `VLAN tags`
```
show ethernet-switching interfaces
```

Show the spanning tree interface
```
show spanning-tree interface
```

# Using wildcards

Wildcards can only be used in `[edit]` mode. Square brackets are used to specify a start/end when using `range`
```
# Delete the entire switch stacks descriptions on all interfaces
wildcard range delete interface ge-[0-1]/[0-1]/[0-47] description

# show all vlan members configured on ports above 40
wildcard range show interfaces ge-[0-1]/0/[40-47] unit 0 family ethernet-switching vlan members

# Configure a series of ports as trunk ports
wildcard range set interfaces ge-[0-1]/0/[40-44] description "ESXi DS Trunk"
wildcard range set interfaces ge-[0-1]/0/[40-44] unit 0 family ethernet-switching port-mode trunk
wildcard range set interfaces ge-[0-1]/0/[40-44] unit 0 family ethernet-switching vlan members all
wildcard range set interfaces ge-[0-1]/0/[40-44] unit 0 family ethernet-switching native-vlan-id default
 ```


