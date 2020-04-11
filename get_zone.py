#!/usr/bin/env python3

import dns.resolver
import dns.query
import dns.zone
import random

tld_ns_file = "effective_tld_names.dat.sane.ns"
zone_state_file = "get_zone.state"
zone_out = "zones.out"

def next_domain(in_file,start_at=0):
        with open(in_file, 'r') as f:
            lines = f.read().splitlines()
            lines = lines[start_at:]
            for line in lines:
                yield line

def get_zone(nameserver,domain,lifetime=5):
    try:
        axfr = dns.query.xfr(nameserver, domain, lifetime=lifetime)
    except:
        return []
    try:
        return [ str(entry)+"."+domain for entry in list(dns.zone.from_xfr(axfr))]
    except:
        return []


def get_state(file_name):
    try:
        with open(file_name, 'r') as f:
            return int(f.read().strip())
    except:
        return 0

# set FLUSH to 1-N to set on every Nth iterations files and debug msg are flushed
FLUSH = 10
zone_state = get_state(zone_state_file)
print(f"[start] Found state: {zone_state}")
lines = next_domain(tld_ns_file, zone_state)

with open(zone_state_file, 'w') as ns_state_fd:
    with open(zone_out, 'a') as fd:
        for count, line in enumerate(lines):
            domain, *nsl = line.split(',')
            zone_sum = set()
            for ns in nsl:
                zone = get_zone(ns, domain)
                if zone != []:
                    zone_sum.update(zone)
            if zone_sum != set():
                entry = "{},{}\n".format(domain, ",".join(zone_sum))
                fd.write(entry)

            ns_state_fd.seek(0)
            ns_state_fd.write(str(count + zone_state))

            if not count % FLUSH:
                fd.flush()
                ns_state_fd.flush()
                print(f"[info] {count+1} domains queried")
        print(f"[done] {zone_state+1} domains queried")
