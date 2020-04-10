#!/usr/bin/env python3

import dns.resolver
import dns.query
import dns.zone
import random
import time

tld_file = "effective_tld_names.dat.sane"
tld_ns_file = "effective_tld_names.dat.sane.ns"
ns_state_file = "get_ns.state"

def next_domain(in_file,start_at=0):
        with open(tld_file, 'r') as f:
            lines = f.read().splitlines()
            lines = lines[start_at:]
            for line in lines:
                yield line

def get_ns(domain):
    all_ns = set()
    try:
        responses = dns.resolver.query(domain,'NS')
    except:
        return []
    return [str(ns.target) for ns in responses]


def get_zone(nameserver,domain,lifetime=5):
    try:
        axfr = dns.query.xfr(nameserver, domain, lifetime=5)
    except:
        return []
    try:
        return list(dns.zone.from_xfr(axfr))
    except:
        return []


def get_state(file_name):
    try:
        with open(file_name, 'r') as f:
            return int(f.read().strip())
    except:
        return 0

# set FLUSH to 1-N to set on every Nth iterations files and debug msg are flushed

FLUSH = True
ns_state = get_state(ns_state_file)
print(f"[debug:ns_state] Found state: {ns_state}")
lines = next_domain(tld_file, ns_state)

with open(ns_state_file, 'w') as ns_state_fd:
    with open(tld_ns_file, 'a') as fd:
        for ns_state, domain in enumerate(lines):
            ns_list = get_ns(domain)
            ns_list_comma = ",".join(ns_list)
            ns_entry = f"{domain},{ns_list_comma}\n"

            fd.write(ns_entry)
            ns_state_fd.seek(0)
            ns_state_fd.write(str(ns_state))

            if not ns_state % FLUSH:
                print(f"[status] doing: {ns_state}")
                fd.flush()
                ns_state_fd.flush()

        print(f"[done] {ns_state+1} domains queried")
