# cEOS Customisation

## Configure `SYSMAC` and `SERIAL`

Configure a file with this content:

```bash
SERIALNUMBER=TITOM73DC1LEAF1
SYSTEMMACADDR=00:1c:73:00:01:13
```

And in your Containerlab topology file:

```yaml
topology:
  nodes:
    s1-spine1:
      kind: ceos
      mgmt-ipv4: "192.168.74.11"
      startup-config: ...
      binds:
        - s1-spine1.cfg:/mnt/flash/ceos-config:ro
      env:
        TMODE: lacp
      labels:
        graph-level: 1
        graph-icon: router
```

## Use HW physical layout

```yaml
topology:
  nodes:
    s1-spine1:
      kind: ceos
      mgmt-ipv4: "192.168.74.11"
      startup-config: ...
      binds:
        - DCS-7050SX3-48YC8.json:/mnt/flash/EosIntfMapping.json:ro
      env:
        TMODE: lacp
      labels:
        graph-level: 1
        graph-icon: router
```

A list of HW layouts is available under [`eos-intf-mapping`](../eos-intf-mapping/)

## Mimic HW in Cloudvision

First, set environment variables in containerlab topology:

```yaml
# For single routing engine
topology:
  nodes:
    s1-spine1:
      kind: ceos
      env:
        MODEL_NAME: DCS-7050SX3-48YC8
```

For a chassis:

```yaml
# For chassis with dual routing engine
topology:
  nodes:
    s1-spine1:
      kind: ceos
      env:
      env:
        CHASSIS_MODEL_NAME: CCS-755-CH
        CHASSIS_SUPERVISOR_1: CCS-750-SUP25
        CHASSIS_SUPERVISOR_2: CCS-750-SUP25
        CHASSIS_LINECARD_1: CCS-750X-48TP-LC
        CHASSIS_LINECARD_2: CCS-750X-48TP-LC
        CHASSIS_LINECARD_3: CCS-750X-48TP-LC
        CHASSIS_LINECARD_4: CCS-750X-48TP-LC
        CHASSIS_LINECARD_5: CCS-750X-48TP-LC
```

Then use this `ceos` configuration:

```eos
aaa authorization exec default local
aaa authentication policy local allow-nopassword-remote-login
username admin privilege 15 role network-admin nopassword
username mtache privilege 15 role network-admin nopassword

hostname campus-{{ .ShortName }}

{{- if .Env.CLAB_MGMT_VRF }}
vrf instance {{ .Env.CLAB_MGMT_VRF }}

{{end}}
{{ if .MgmtIPv4Gateway }}ip route {{ if .Env.CLAB_MGMT_VRF }}vrf {{ .Env.CLAB_MGMT_VRF }} {{end}}0.0.0.0/0 {{ .MgmtIPv4Gateway }}{{end}}
{{ if .MgmtIPv6Gateway }}ipv6 route {{ if .Env.CLAB_MGMT_VRF }}vrf {{ .Env.CLAB_MGMT_VRF }} {{end}}::0/0 {{ .MgmtIPv6Gateway }}{{end}}


interface {{ .MgmtIntf }}
{{ if .Env.CLAB_MGMT_VRF }} vrf {{ .Env.CLAB_MGMT_VRF }}{{end}}
{{ if .MgmtIPv4Address }}ip address {{ .MgmtIPv4Address }}/{{.MgmtIPv4PrefixLength}}{{end}}
{{ if .MgmtIPv6Address }}ipv6 address {{ .MgmtIPv6Address }}/{{.MgmtIPv6PrefixLength}}{{end}}

daemon TerminAttr
   exec /usr/bin/TerminAttr -cvaddr=apiserver.cv-staging.corp.arista.io:443 -cvauth=token-secure,/mnt/flash/cv-onboarding-token -cvvrf={{ .Env.CLAB_MGMT_VRF }} -smashexcludes=ale,flexCounter,hardware,kni,pulse,strata -ingestexclude=/Sysdb/cell/1/agent,/Sysdb/cell/2/agent -taillogs
   no shutdown

ip name-server vrf MGMT 8.8.8.8

event-handler ConfigureHardwareModel
   trigger on-boot
   action bash
      python -m Acons Sysdb << EOF
      cd /ar/Sysdb/hardware/entmib
      if (model := os.getenv('MODEL_NAME')):
         _.fixedSystem.modelName = model
      elif (model := os.getenv('CHASSIS_MODEL_NAME')):
         _.chassis = (1,0,'Chassis')
         _.chassis.modelName = model
         for var, value in os.environ.items():
            if var.startswith('CHASSIS'):
               keys = var.split('_')
               if keys[1] == "SUPERVISOR":
                  i = int(keys[2])
                  _.chassis.cardSlot.newMember(100002000+i, i, 'Supervisor')
                  _.chassis.cardSlot[i].card = (100002100+i, i, 'Supervisor')
                  _.chassis.cardSlot[i].card.modelName = value
               elif keys[1] == "LINECARD":
                  i = int(keys[2]) + 2
                  _.chassis.cardSlot.newMember(100002000+i, i, 'Linecard')
                  _.chassis.cardSlot[i].card = (100002100+i, i, 'Linecard')
                  _.chassis.cardSlot[i].card.modelName = value

      print(f"Hardare model has been set to {model}")
      EOF
!
```
