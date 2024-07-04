# Containerlab configuration

## Node representation

Containerlab can leverage tags for better representation when using `containerlab graph` or graphite.

```yaml
nodes:
    spine01:
        group: spine
    leaf01:
        group: leaf
    server01:
        group: server
```

Because group names can be completely custom, containerlab supports sorOrder definition:

```yaml
sortOrder: ['10', '9', 'superspine', '8', 'dc-gw', '7', '6', 'spine', '5', '4', 'leaf', 'border-leaf', 'router', 'server', '2', '1'],
```

> [!NOTE]
> More information on [containerlab website](https://containerlab.dev/cmd/graph/#layout-and-sorting)

## Node definition

### Generic Linux host

Linux with bonding to remote host and 802.1q vlan 1002 configured.

```yaml
topology:
  kinds:
    linux:
      # image: titom73/multitool:latest # Old image path
      image: git.as73.inetsix.net/docker/multitool:latest
nodes:
    linux_example01:
      mgmt-ipv4: 10.74.0.216
      kind: linux
      exec:
        - vconfig add team0 1002
        - ifconfig team0.1002 10.100.2.23 netmask 255.255.255.0
        - ip link set team0.1002 up
        - ip route del default
        - ip route add default via 10.100.2.254
        - sysctl -w net.ipv4.ip-forward=0
      env:
        TMODE: lacp
      group: server
```

### Freeradius Host

```bash
nodes:
  radius:
    image: titom73/freeradius:latest
    mgmt_ipv4: 172.16.0.2
    kind: linux
    binds:
    - radius_authorize:/etc/raddb/mods-config/files/authorize
links:
  - endpoints: ["leaf1:eth2", "radius:eth1"]
```
