"""Local filters for cookiecutter project."""

import ipaddress
from cookiecutter.utils import simple_filter


@simple_filter
def generate_mgmt_ip(network, hostid: int = 1):
    net = ipaddress.ip_network(network)
    return next(net.hosts()) + hostid


@simple_filter
def generate_ip_with_subnet(network, hostid: int = 1):
    net = ipaddress.ip_network(network)
    _, net_bits = network.split("/")
    host = next(net.hosts()) + hostid
    return str(host) + "/" + net_bits
