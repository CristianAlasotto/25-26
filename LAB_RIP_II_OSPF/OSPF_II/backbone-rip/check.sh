#!/bin/sh
set -eu

for router in bb0 bb1 bb2 bb3 bb4; do
  printf '\n### %s: RIP routes\n' "$router"
  kathara exec "$router" -- vtysh -c "show ip rip"
done

for router in r2 r3 r5; do
  printf '\n### %s: OSPF routes and database\n' "$router"
  kathara exec "$router" -- vtysh -c "show ip ospf route"
  kathara exec "$router" -- vtysh -c "show ip ospf database"
done
