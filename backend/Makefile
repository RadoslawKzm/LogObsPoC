.PHONY: lint lint-check check-venv

VENV = ./venv
ISORT = $(VENV)/bin/isort
RUFF = $(VENV)/bin/ruff
FLAKE8 = $(VENV)/bin/flake8

check-venv:
	@if [ ! -d $(VENV) ]; then \
		echo "Error: Virtual environment '$(VENV)' not found!"; \
		echo "Please create it with: python -m venv $(VENV)"; \
		exit 1; \
	fi

# lint runs isort (fix), ruff (fix), and flake8 (check)
lint: check-venv
	$(ISORT) .
	$(RUFF) check . --fix
	#$(FLAKE8) .

# lint-check runs ruff check, flake8 check, and isort check-only (no fixes)
lint-check: check-venv
	$(RUFF) check .
	$(FLAKE8) .
	$(ISORT) --check-only .
