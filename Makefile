.PHONY: check-fast check test portability links hooks-install audit-upstreams

check-fast:
	python3 scripts/update-provenance.py --check
	python3 scripts/validate.py

test:
	python3 -m unittest discover -s tests -v

portability:
	bash scripts/check-portability.sh

links:
	python3 scripts/link-installed.py --check

audit-upstreams:
	python3 scripts/audit-upstreams.py

check: check-fast test portability links

hooks-install:
	bash scripts/install-git-hooks
