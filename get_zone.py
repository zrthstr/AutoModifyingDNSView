#!/usr/bin/env python3

def get_zone(nameserver,domain,lifetime=5):
    try:
        axfr = dns.query.xfr(nameserver, domain, lifetime=lifetime)
    except:
        return []
    try:
        return [ str(entry)+"."+domain for entry in list(dns.zone.from_xfr(axfr))]
    except:
        return []

#!/usr/bin/env python3

import sys
import dns.resolver
import dns.query
import dns.zone
from multiprocessing.pool import ThreadPool as Pool

ns_in = "ns.out"
zone_out = "zone.out"

pool_size = 5
pool = Pool(pool_size)
dnsResolver = dns.resolver.Resolver()
dnsResolver.timeout = 4
dnsResolver.lifetime = 4
#dnsResolver.nameservers = ['8.8.8.8','8.8.4.4','1.1.1.1','1.0.0.1']

res = []

def fetch_ZONE(domain, ns):
    #res.append("dddd")
    domain = domain.strip()

    dnsAnswer = dns.query.xfr(ns, domain)
    #print("XXXXXXXXXXXXX",dnsAnswer)
    #try:

    line = domain + ":" + "\n".join([str(rdata) for rdata in dnsAnswer ])

    #print(f"ne = line = {line}")
    res.append(line)

    #res.append([str(rdata) for rdate in dnsAnswer ])
    #except dns.resolver.NXDOMAIN:
    #    print ("[e] No records exists for", domain)
    #except dns.resolver.Timeout:
    #    print ("[e] Timeout in querying",domain)

maxline = 9999999999
if len(sys.argv) > 1:
    maxline = int(sys.argv[1])

with open(ns_in,'r') as fd1:
    for count, line in enumerate(fd1):
        if count > maxline:
            print(f"[i] maxline reached")
            break
        if not ',' in line:
            continue
        domain, *nslist = line.split(',')
        if not len(nslist):
            continue
        for ns in nslist:
            print(f"testing: {domain} {ns}")
            pool.apply_async(fetch_ZONE, (domain, ns))


pool.close()
pool.join()
out = "\n".join(res)
print(out, res)
with open(ns_in,'w') as f:
    f.write(out)
