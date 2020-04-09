TLD_LIST = effective_tld_names.dat
TLD_LIST_CLEAN = $(TLD_LIST).clean
TLD_LIST_SANE = $(TLD_LIST).sane

test:
	echo ABCEDFG >> data.list

update_tld_file:
	rm -rf /effective_tld_names.dat
	curl -O $(TLD_LIST) https://publicsuffix.org/list/effective_tld_names.dat

filter_tld_file:
	cat $(TLD_LIST) | sed 's/[\t ]//g' | grep -v '//' | sed 's/*.//g' | grep -v '^$$' | sort | uniq > $(TLD_LIST_CLEAN)

censore_tld_file:
	cat $(TLD_LIST_CLEAN) | grep -v '^mil' > TLD_LIST_SANE
