.PHONY: clean-pyc clean-build clean-test clean

RESOURCE_DIR = designer
COMPILED_DIR = gui/generated
UI_FILES = main_window.ui
MAIN = rawdisk-ui
PYUIC = pyuic5

COMPILED_UI = $(UI_FILES:%.ui=$(COMPILED_DIR)/ui_%.py)

clean: clean-build clean-pyc clean-app clean-test

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

clean-test:
	rm -rf .tox/
	rm -rf .coverage
	rm -rf htmlcov/

clean-app:
	rm -rf ${MAIN}.app

lint:
	flake8 .

app : clean ui
	pyinstaller --noconsole --windowed ${MAIN}.py
	mv dist/${MAIN}.app .

ui : $(COMPILED_UI)

$(COMPILED_DIR)/ui_%.py : $(RESOURCE_DIR)/%.ui
	$(PYUIC) $< -o $@