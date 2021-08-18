# TODO I should be able to move the home/bin/tests to tests/bin
test:
	PYTHONPATH=home/bin pytest -v home/bin/tests
	PYTHONPATH=. pytest -v tests

install_configs:
	python3 install/setup_system_links.py
	python3 install/setup_alacritty_machine_specific_config.py
