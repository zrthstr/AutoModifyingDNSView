TLD_LIST = effective_tld_names.dat
TLD_LIST_CLEAN = $(TLD_LIST).clean
TLD_LIST_SANE = $(TLD_LIST).sane
TLD_LIST_STAT = effective_tld_names.stat
TLD_LIST_NS = effective_tld_names.dat.sane.ns

install_py_dep:
	pip3 install -r requirements.txt

update_tld_file:
	rm -rf /effective_tld_names.dat
	curl https://publicsuffix.org/list/effective_tld_names.dat -o $(TLD_LIST)

filter_tld_file:
	cat $(TLD_LIST) | sed 's/[\t ]//g' |	grep -v '!' |grep -v '//' | sed 's/*.//g' | grep -v '^$$' | sort | uniq > $(TLD_LIST_CLEAN)

censore_tld_file:
	cat $(TLD_LIST_CLEAN) | grep -v '^mil' > $(TLD_LIST_SANE)

count_sane_tld_file:
	date >> $(TLD_LIST_STAT)
	wc -l $(TLD_LIST) $(TLD_LIST_CLEAN) $(TLD_LIST_SANE) >> $(TLD_LIST_STAT)


clean_ns:
	rm $(TLD_LIST_NS)
	touch $(TLD_LIST_NS)

get_ns:
	python3 get_ns.py

get_zone:
	python3 get_zone.py
