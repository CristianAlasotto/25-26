#!/usr/bin/env python3
"""Read-only consistency checks for all OSPF II Kathara scenarios."""

from __future__ import annotations

import ipaddress
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCENARIOS = (ROOT, ROOT / "backbone-rip", ROOT / "asbr-bgp")

BASE_AREAS = {
    "bb0": {0: "0.0.0.0", 1: "0.0.0.0"},
    "bb1": {0: "0.0.0.0", 1: "0.0.0.0", 2: "1.1.1.1", 3: "2.2.2.2"},
    "bb2": {0: "0.0.0.0", 1: "0.0.0.0", 2: "3.3.3.3", 3: "2.2.2.2"},
    "bb3": {0: "0.0.0.0", 1: "0.0.0.0"},
    "bb4": {0: "0.0.0.0", 1: "0.0.0.0"},
    "r1": {0: "1.1.1.1", 1: "1.1.1.1"},
    "r2": {0: "1.1.1.1", 1: "1.1.1.1"},
    "r3": {0: "2.2.2.2", 1: "2.2.2.2", 2: "2.2.2.2"},
    "r4": {0: "3.3.3.3", 1: "3.3.3.3"},
    "r5": {0: "3.3.3.3", 1: "3.3.3.3", 2: "3.3.3.3"},
    "r6": {0: "3.3.3.3", 1: "3.3.3.3"},
}


def parse_lab(path: Path):
    text = path.read_text()
    links: dict[str, dict[int, str]] = {}
    images: dict[str, str] = {}
    for router, index, domain in re.findall(r'^(\w+)\[(\d+)\]="?([^"\n]+)"?$', text, re.M):
        links.setdefault(router, {})[int(index)] = domain
    for router, image in re.findall(r'^(\w+)\[image\]="([^"]+)"$', text, re.M):
        images[router] = image
    return links, images


def parse_startup(path: Path):
    found = {}
    for address, index in re.findall(
        r'^ip address add (\S+) dev eth(\d+)$', path.read_text(), re.M
    ):
        found[int(index)] = ipaddress.ip_interface(address)
    return found


def parse_daemons(path: Path):
    return dict(re.findall(r'^(\w+)=(yes|no)$', path.read_text(), re.M))


def ospf_areas(path: Path, interfaces):
    rules = [
        (ipaddress.ip_network(prefix), area)
        for prefix, area in re.findall(
            r'^\s*network (\S+) area (\S+)$', path.read_text(), re.M
        )
    ]
    result = {}
    for index, interface in interfaces.items():
        matches = {area for network, area in rules if interface.ip in network}
        if len(matches) > 1:
            raise AssertionError(f"{path}: eth{index} matches multiple OSPF areas {matches}")
        result[index] = next(iter(matches), None)
    return result


def expected_areas(name: str, router: str):
    result = dict(BASE_AREAS.get(router, {}))
    if name == "backbone-rip":
        if router in {"bb0", "bb3", "bb4"}:
            return {index: None for index in result}
        if router in {"bb1", "bb2"}:
            result[0] = None
            result[1] = None
    if router == "as100r1":
        return {0: None}
    if name == "asbr-bgp" and router == "bb3":
        result[2] = None
    return result


def expected_daemons(name: str, router: str):
    if name == "backbone-rip":
        return {
            "ospfd": "yes" if router not in {"bb0", "bb3", "bb4"} else "no",
            "ripd": "yes" if router.startswith("bb") else "no",
            "bgpd": "no",
        }
    if name == "asbr-bgp":
        return {
            "ospfd": "no" if router == "as100r1" else "yes",
            "ripd": "no",
            "bgpd": "yes" if router in {"bb3", "as100r1"} else "no",
        }
    return {"ospfd": "yes", "ripd": "no", "bgpd": "no"}


def validate(scenario: Path):
    name = "base" if scenario == ROOT else scenario.name
    links, images = parse_lab(scenario / "lab.conf")
    errors = []
    endpoints = {}
    all_networks = set()
    all_ips = set()

    for router, ports in links.items():
        if images.get(router) != "kathara/frr":
            errors.append(f"{router}: image is not kathara/frr")
        startup_path = scenario / f"{router}.startup"
        frr_path = scenario / router / "etc/frr/frr.conf"
        daemon_path = scenario / router / "etc/frr/daemons"
        if not all(p.exists() for p in (startup_path, frr_path, daemon_path)):
            errors.append(f"{router}: startup/FRR file missing")
            continue
        interfaces = parse_startup(startup_path)
        if set(interfaces) != set(ports):
            errors.append(
                f"{router}: lab eth={sorted(ports)}, startup eth={sorted(interfaces)}"
            )
        for index, domain in ports.items():
            if index not in interfaces:
                continue
            interface = interfaces[index]
            if interface.ip in all_ips:
                errors.append(f"duplicate IP {interface.ip}")
            all_ips.add(interface.ip)
            all_networks.add(interface.network)
            endpoints.setdefault(domain, []).append((router, index, interface))

        actual_areas = ospf_areas(frr_path, interfaces)
        wanted_areas = expected_areas(name, router)
        if actual_areas != wanted_areas:
            errors.append(f"{router}: OSPF areas {actual_areas}, expected {wanted_areas}")

        daemons = parse_daemons(daemon_path)
        for daemon, wanted in expected_daemons(name, router).items():
            if daemons.get(daemon) != wanted:
                errors.append(f"{router}: {daemon}={daemons.get(daemon)}, expected {wanted}")
        if daemons.get("zebra") != "yes":
            errors.append(f"{router}: zebra must be yes")

    for domain, members in endpoints.items():
        networks = {interface.network for _, _, interface in members}
        if len(networks) != 1:
            errors.append(f"domain {domain}: inconsistent subnets {networks}")
        network = next(iter(networks))
        if network.prefixlen == 30 and len(members) != 2:
            errors.append(f"domain {domain}: /30 has {len(members)} endpoints")

    networks = sorted(all_networks, key=lambda n: (int(n.network_address), n.prefixlen))
    for pos, left in enumerate(networks):
        for right in networks[pos + 1 :]:
            if left != right and left.overlaps(right):
                errors.append(f"overlapping subnets {left} and {right}")

    if name == "base":
        for router in links:
            text = (scenario / router / "etc/frr/frr.conf").read_text()
            for area in set(BASE_AREAS[router].values()) - {"0.0.0.0"}:
                if f"area {area} stub" not in text:
                    errors.append(f"{router}: missing coherent stub declaration for {area}")

    if errors:
        return [f"[{name}] {error}" for error in errors]
    print(f"OK {name}: {len(links)} routers, {len(endpoints)} collision domains")
    return []


def main():
    errors = []
    for scenario in SCENARIOS:
        errors.extend(validate(scenario))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
