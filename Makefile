SHELL=/bin/bash
FILES=pyng/core.py pyng/checksum.py bin/pyng
PYTHON=/usr/bin/env python

build:
	$(PYTHON) setup.py build

install: build
	sudo $(PYTHON) setup.py install \
		--record installed-files.txt \
		--single-version-externally-managed

uninstall:
	@if [ -e "installed-files.txt" ]; then \
		while read path; do \
			echo $${path}; \
			sudo rm -rf $${path}; \
		done < "installed-files.txt"; \
	fi

test:
	$(PYTHON) -m pep8 $(FILES) --show-source

tox:
	tox --skip-missing-interpreters --develop

clean:
	git clean -xdf
