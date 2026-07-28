SHELL := /bin/bash

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: setup install run

setup: $(PYTHON)

$(PYTHON):
	python3 -m venv $(VENV)

install: setup
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run: install
	. $(VENV)/bin/activate && exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
