#!/bin/sh
set -eu

show() {
  router="$1"
  command="$2"
  printf '\n### %s: %s\n' "$router" "$command"
  kathara exec "$router" -- vtysh -c "$command"
}

show bb0 "show ip ospf neighbor"
show bb1 "show ip ospf neighbor"
show bb1 "show ip ospf database router"
show bb1 "show ip ospf database summary"
show r2 "show ip ospf neighbor"
show r2 "show ip ospf route"
show r2 "show ip ospf database summary"
show r3 "show ip ospf route"
show r5 "show ip ospf route"

printf '\n### bb0 -> r2 (200.0.0.2)\n'
kathara exec bb0 -- traceroute -n 200.0.0.2

printf '\n### r2 -> bb0 (10.0.2.3)\n'
kathara exec r2 -- traceroute -n 10.0.2.3
