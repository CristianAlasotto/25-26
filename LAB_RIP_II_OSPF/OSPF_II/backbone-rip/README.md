# Backbone RIP alternative

This independent scenario replaces OSPF area 0 with RIP v2 while retaining
OSPF in the peripheral areas.

The peripheral areas are deliberately normal areas, not OSPF stub areas.
The former ABRs are now redistribution boundary routers/ASBRs: they announce
OSPF and connected peripheral routes into RIP and redistribute RIP routes into
OSPF as E2 routes. A true OSPF stub cannot accept those Type 5 LSAs, and without
OSPF area 0 no router can perform the original ABR Type 3-summary function.

Start and check:

    kathara lstart
    ./check.sh
    kathara lclean
