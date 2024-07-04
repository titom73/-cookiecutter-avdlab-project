# AVD/Containerlab Project template

## Overview

Git repository to easily generate a project based on Arista AVD and Containerlab for lab purpose:

- `project`: name of the project.
- `oob_subnet`: Subnet to use for Out of Band management in Containerlab (default: `192.168.1.0/24`)
- `eos_name`: Name of the cEOS container (default: `arista/ceos`)
- `eos_version`: Version of cEOS to use (default: `4.30.3M`)
- `avd_version`: Version of [AVD](https://github.com/aristanetworks/avd) to use in the project (default: `4.8.0`)


## Getting Started

```bash
# Install cookiecutter (if not already installed)
pipx install cookiecutter jinja2-time

# Create your project (custom git server)
cookiecutter https://git.as73.inetsix.net/labs/cookiecutter-avdlab-project.git

# Create your project (github)
cookiecutter gh:titom73/cookiecutter-avdlab-project.git
```

## Requirements

- containerlab installed
- Ansible (can be installed via project requirements)
- [Arista Validated Design](https://avd.arista.com) (can be installed via project requirements)
- Arista [ANTA framework](https://anta.arista.com) (can be installed via project requirements)
- [EOS Dowloader CLI](https://github.com/titom73/eos-downloader/) (can be installed via project requirements)

## Contribution guide

Contributions are welcome. Please refer to the [contribution guide](./CONTRIBUTING.md)

## Licence

The project is published under [Apache-2.0](./LICENCE)