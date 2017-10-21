# bash needed for pipefail
SHELL := /bin/bash

test: test_lint

test_lint:
	mkdir -p build
	set -o pipefail; flake8 | sed "s#^\./##" > build/flake8.txt || (cat build/flake8.txt && exit 1)
