#!/uar/bin/env python3

import dns.resolver
import dns.query
import dns.zone
import random
import time

tld_file = "effective_tld_names.dat.sane"

def get_random_line(in_file, stop_in_lines=0, stop_in_sec=0):
    count = 0
    time_start = time.time()
    time_end = time_start + stop_in_sec
    with open(tld_file, 'r') as f:
        lines = f.read().splitlines()
        while stop_in_lines == 0 or count < stop_in_lines:
            if time_end == time_start or time_end > time.time():
                myline = random.choice(lines)
                count +=1
                yield myline
            else:
                print("[-] Timeout hit.")
                break 
        if stop_in_lines == count:
            print("[-] Maxline hit.")



def get_ns(domain):
    all_ns = set()
    try:
        responses = dns.resolver.query(domain,'NS')
    except:
        return [False]
    return [ns.target for ns in responses]


def get_zone(nameserver,domain,lifetime=5):
    try:
        axfr = dns.query.xfr(nameserver, domain, lifetime=5)
    except:
        return [False]
    try:
        zone = dns.zone.from_xfr(axfr)
    except:
        return [False]


#lines = get_random_line(tld_file, stop_in_lines=10, stop_in_sec )
lines = get_random_line(tld_file, stop_in_sec=2 )

for domain in lines:
    for ns in get_ns(domain):
        for zone in get_zone(ns, domain):
            #save_zone(zone, ns, domain)
            print(zone, ns, domain)
            # is one zone for a singe domain suffcient?
        else:
            print(f"[.] No Zone for domain: {domain} by NS: {ns} .")
    else:
        print(f"[-] No NS-record found for domain: {domain} .")
else:
    print("[end] No more line in tld pipline.")

