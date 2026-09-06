.PHONY: check-fast check test test-archify portability links hooks-install audit-upstreams

check-fast:
	python3 scripts/update-provenance.py --check
	python3 scripts/validate.py

test:
	python3 -m unittest discover -s tests -v

portability:
	python3 scripts/check-portability.py

links:
	python3 scripts/link-installed.py --check

audit-upstreams:
	python3 scripts/audit-upstreams.py

check: check-fast test portability links

hooks-install:
	python3 scripts/install-git-hooks.py

# Fetches the recorded upstream test workspace; never changes installed links.
ARCHIFY_TEST_ARGS ?=
test-archify:
	python3 scripts/test_archify.py $(ARCHIFY_TEST_ARGS)
