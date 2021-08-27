test:
	PYTHONPATH=.:home/bin pytest -v tests

install_configs:
	python3.7 install/setup_system_links.py
	python3.7 install/setup_alacritty_machine_specific_config.py

test_continously:
	fd '\.py$$' install/ tests/ | entr -c make test
