#!/usr/bin/env python3

import dns.resolver
from multiprocessing.pool import ThreadPool as Pool

tld_file = "effective_tld_names.dat.sane"

pool_size = 4
pool = Pool(pool_size)
dnsResolver = dns.resolver.Resolver()
dnsResolver.timeout = 3
dnsResolver.lifetime = 3
#dnsResolver.nameservers = ['8.8.8.8','8.8.4.4','1.1.1.1','1.0.0.1']
dnsResolver.nameservers = ['8.8.8.8','8.8.4.4','1.1.1.1','1.0.0.1']

res = []

def fetch_dig_no_blast_results(no_blast_domains):
    try:
        no_blast_domains = no_blast_domains.strip()
        dnsAnswer = dnsResolver.query(no_blast_domains)
        print(f".... dnsAnswer {dnsAnswer}")
        for rdata in dnsAnswer:
            print ("[+]",no_blast_domains, "resolved to",str(rdata))
            res.append(rdata)
            print(res)
    except dns.resolver.NXDOMAIN:
        print ("[e] No records exists for", no_blast_domains)
    except dns.resolver.Timeout:
        print ("[e] Timeout in querying",no_blast_domains)

with open(tld_file,'r') as fd1:
    for no_blast_domains in fd1:
        #print("__", no_blast_domains)
        #no_blast_domains = no_blast_domains.strip()
        pool.apply_async(fetch_dig_no_blast_results, (no_blast_domains,))

pool.close()
pool.join()

print(res)
