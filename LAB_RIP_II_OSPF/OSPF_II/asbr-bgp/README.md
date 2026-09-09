# ASBR + BGP, stub no-summary and E2

This independent scenario extends the official multi-area topology with
`as100r1` in AS100, connected to `bb3` in AS10 over 140.0.0.0/30.

`as100r1` owns 50.0.0.1/16 on loopback and advertises 50.0.0.0/16 by eBGP.
`bb3` redistributes BGP into OSPF as E2 metric 20. The ABRs configure the
peripheral areas as stub no-summary, while internal routers use `stub`.
Consequently backbone routers see the Type 5 and `O E2` route, whereas
internal stub routers see only the Type 3 default and still reach 50.0.0.1.

Start and check:

    kathara lstart
    ./check.sh
    kathara lclean
