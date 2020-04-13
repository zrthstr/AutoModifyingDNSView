TLD_LIST = effective_tld_names.dat
TLD_LIST_CLEAN = $(TLD_LIST).clean
TLD_LIST_SANE = $(TLD_LIST).sane
TLD_LIST_STAT = effective_tld_names.stat
NS_OUT = ns.out
ZONES_OUT = zone.out

install_py_dep:
	pip3 install -r requirements.txt

update_tld_file:
	rm -rf $(TLD_LIST)
	curl https://publicsuffix.org/list/effective_tld_names.dat -o $(TLD_LIST)
	cat $(TLD_LIST) | sed 's/[\t ]//g' |	grep -v '!' |grep -v '//' | sed 's/*.//g' | grep -v '^$$' | sort | uniq > $(TLD_LIST_CLEAN)
	cat $(TLD_LIST_CLEAN) | grep -v '^mil' > $(TLD_LIST_SANE)
	rm $(TLD_LIST) $(TLD_LIST_CLEAN) 

#count_sane_tld_file:
#	date >> $(TLD_LIST_STAT)
#	wc -l $(TLD_LIST) $(TLD_LIST_CLEAN) $(TLD_LIST_SANE) >> $(TLD_LIST_STAT)

clean_ns:
	rm $(NS_OUT)
	touch $(NS_OUT)

get_ns: clean_ns
	python3 get_ns.py

clean_zone:
	rm $(ZONES_OUT)
	touch $(ZONES_OUT)

get_zone: clean_zone
	echo get_zone
	python3 get_zone.py
