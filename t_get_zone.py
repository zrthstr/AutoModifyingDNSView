#!/usr/bin/env python3

import sys
import dns.resolver
import dns.query
import dns.zone

#from multiprocessing.pool import ThreadPool as Pool
import threading

ns_in = "ns.out"
zone_out = "zone.out"

#pool_size = 30
#pool = Pool(pool_size)
#dnsResolver = dns.resolver.Resolver()
#dnsResolver.timeout = 4
#dnsResolver.lifetime = 4
#dnsResolver.nameservers = ['8.8.8.8','8.8.4.4','1.1.1.1','1.0.0.1']

res = []

def fetch_ZONE(domain, ns):
    #res.append("dddd")
    domain = domain.strip()
    try:
        dnsAnswer = dns.query.xfr(ns, domain)
    except dns.query.TransferError:
        print("TransferError", domain)
    #try:

    # foo =  [ str(entry)+"."+domain for entry in list(dns.zone.from_xfr(axfr))]
    try:
        line = domain + ":" + "\n".join([str(rdata) for rdata in dnsAnswer  ])
    except dns.query.TransferError:
        print("TransferError", domain)
        line = "fail"
    except dns.exception.FormError:
        print("dns.exception.FormError", domain)
        line = "fail"
    except ConnectionResetError:
        print("ConnectionResetError", domain)
        line = "fail"
    print("line", line)

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

threads = []

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
            #pool.daemon = True
            t = threading.Thread(target=fetch_ZONE, args=(domain,ns))
            #pool.apply_async(fetch_ZONE, (domain, ns))
            threads.append(t)
            t.start()


t.join()
#print("above cliose")
#pool.close()
#print("above join")
#pool.join()
#print("XXX" * 300 ,"below join")
### TODO dedup res on domain basis
out = "\n".join(res)
print("out,res::",out, res)
with open(zone_out,'w') as f:
    f.write(out)
