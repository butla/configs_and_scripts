# TODO I should be able to move the home/bin/tests to tests/bin
test:
	PYTHONPATH=home/bin pytest -v home/bin/tests
	PYTHONPATH=. pytest -v tests

install_links:
	python3.7 install/setup_system_links.py
