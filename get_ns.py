#!/usr/bin/env python3

import sys
import dns.resolver
from multiprocessing.pool import ThreadPool as Pool

tld_file = "effective_tld_names.dat.sane"
ns_out = "ns.out"

pool_size = 25
pool = Pool(pool_size)
dnsResolver = dns.resolver.Resolver()
dnsResolver.timeout = 3
dnsResolver.lifetime = 3
dnsResolver.nameservers = ['8.8.8.8','8.8.4.4','1.1.1.1','1.0.0.1']

res = []

def fetch_NS(domain):
    try:
        domain = domain.strip()
        dnsAnswer = dnsResolver.query(domain, "NS")

        line = domain + "," + ",".join([str(rdata) for rdata in dnsAnswer ])
        res.append(line)
        #res.append([str(rdata) for rdate in dnsAnswer ])

    except dns.resolver.NXDOMAIN:
        print ("[e] No records exists for", domain)
    except dns.resolver.Timeout:
        print ("[e] Timeout in querying",domain)

maxline = 9999999999
if len(sys.argv) > 1:
    maxline = int(sys.argv[1])

print(f"maxline {maxline}")

with open(tld_file,'r') as fd1:
    for count, domain in enumerate(fd1):
        #print(f"cpint {count}")
        if count > maxline:
            print(f"[i] maxline reached")
            break
        pool.apply_async(fetch_NS, (domain,))

pool.close()
pool.join()
out = "\n".join(res)
with open(ns_out,'w') as f:
    f.write(out)
