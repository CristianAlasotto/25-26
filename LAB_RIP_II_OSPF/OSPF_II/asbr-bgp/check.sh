#!/bin/sh
set -eu

show() {
  router="$1"
  command="$2"
  printf '\n### %s: %s\n' "$router" "$command"
  kathara exec "$router" -- vtysh -c "$command"
}

show bb3 "show ip bgp summary"
show bb3 "show ip bgp 50.0.0.0/16"
show as100r1 "show ip bgp summary"
show bb1 "show ip ospf database external"
show bb1 "show ip route 50.0.0.0/16"
show r2 "show ip ospf database summary"
show r2 "show ip ospf database asbr-summary"
show r2 "show ip ospf database external"
show r2 "show ip route"

printf '\n### Connectivity to the external prefix\n'
kathara exec bb1 -- ping -c 3 50.0.0.1
kathara exec r2 -- ping -c 3 50.0.0.1
kathara exec r2 -- traceroute -n 50.0.0.1
